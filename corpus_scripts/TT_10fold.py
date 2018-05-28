from lxml import etree as document
import os
import sys
import re
from grkFrm import greekForms
from utf2beta import convertUTF
import configparser
import pickle
from subprocess import DEVNULL, STDOUT, check_call
import numpy as np
import pandas as pd
from scipy import stats

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
proiel = config['paths']['proiel']
perseus = config['paths']['perseus_tb']
treetagger = config['paths']['treetagger']
o_dir='TreeTaggerData/10-fold'

converted = ''

# PROIEL REFERENCE
# 
#      <value tag="A-" summary="adjective"/>
#       <value tag="Df" summary="adverb"/>
#       <value tag="S-" summary="article"/>
#       <value tag="Ma" summary="cardinal numeral"/>
#       <value tag="Nb" summary="common noun"/>
#       <value tag="C-" summary="conjunction"/>
#       <value tag="Pd" summary="demonstrative pronoun"/>
#       <value tag="F-" summary="foreign word"/>
#       <value tag="Px" summary="indefinite pronoun"/>
#       <value tag="N-" summary="infinitive marker"/>
#       <value tag="I-" summary="interjection"/>
#       <value tag="Du" summary="interrogative adverb"/>
#       <value tag="Pi" summary="interrogative pronoun"/>
#       <value tag="Mo" summary="ordinal numeral"/>
#       <value tag="Pp" summary="personal pronoun"/>
#       <value tag="Pk" summary="personal reflexive pronoun"/>
#       <value tag="Ps" summary="possessive pronoun"/>
#       <value tag="Pt" summary="possessive reflexive pronoun"/>
#       <value tag="R-" summary="preposition"/>
#       <value tag="Ne" summary="proper noun"/>
#       <value tag="Py" summary="quantifier"/>
#       <value tag="Pc" summary="reciprocal pronoun"/>
#       <value tag="Dq" summary="relative adverb"/>
#       <value tag="Pr" summary="relative pronoun"/>
#       <value tag="G-" summary="subjunction"/>
#       <value tag="V-" summary="verb"/>
#       <value tag="X-" summary="unassigned"/>

proiel_pos = {
"A-":"adjective",
"Df":"adverb",
"S-":"article",
"Ma":"adjective",
"Nb":"noun",
"C-":"conjunction",
"Pd":"pronoun",
"F-":"noun",
"Px":"pronoun",
"N-":"verb",
"I-":"interjection",
"Du":"adverb",
"Pi":"pronoun",
"Mo":"adjective",
"Pp":"pronoun",
"Pk":"pronoun",
"Ps":"pronoun",
"Pt":"pronoun",
"R-":"preposition",
"Ne":"proper",
"Py":"adjective",
"Pc":"pronoun",
"Dq":"adverb",
"Pr":"pronoun",
"G-":"conjunction",
"V-":"verb",
"X-":"unknown"
#punctuation: in attribute presentation-after, must be ≠ " ", and must be stripped
}


#REFERENCE PERSEUS POSTAG
# 1: 	part of speech
# 			
# 				n	noun
# 				v	verb
# 				t	participle
# 				a	adjective
# 				d	adverb
# 				l	article
# 				g	particle
# 				c	conjunction
# 				r	preposition
# 				p	pronoun
# 				m	numeral
# 				i	interjection
# 				e	exclamation
# 				u	punctuation		#make it set to self

perseus_pos = {
"n":"noun",
"v":"verb",
"t":"verb",
"a":"adjective",
"d":"adverb",
"l":"article",
"g":"particle",
"c":"conjunction",
"r":"preposition",
"p":"pronoun",
"m":"adjective",
"i":"interjection",
"e":"interjection",
"u":"SENT",
"-":"unknown",
"x":"unknown"
}

def convert_proiel(file):
	global converted
	converted+='\n'
	parse = document.parse(file)
	words = parse.xpath('//token')
	for word in words:
		try:
			newLine = ''
			form = convertUTF(word.get('form'))
			pos = proiel_pos.get(word.get('part-of-speech'),'unknown')
			newLine = '\t'.join([form, pos])
			if word.get('presentation-after') != " ":
				newLine+='\n{mark}\tSENT'.format(mark=word.get('presentation-after').strip())
		except:
			continue
		converted += '%s\n'%newLine
	converted=converted.strip()
	del parse, words

def convert_perseus(file):
	global converted
	parse = document.parse(file)
	words = parse.xpath('//word[not(@artificial)]')
	for word in words:
		if word.get('artificial') == None:
			converted='%s\n%s'%(converted,convertUTF(word.get('form')))
			postag=word.get('postag')
			if len(postag) > 0:
				pos = perseus_pos[word.get('postag')[0]]
			else:
				pos = 'unknown'
			converted='%s\t%s'%(converted,pos)
	converted=converted.strip()
	del parse, words

if os.path.isfile("%s/converted.p"%o_dir):
	print('Loading full corpus')
	converted = pickle.load(open("%s/converted.p"%o_dir, "rb" ))
else:
	print('Converting Perseus files')
	for filename in os.listdir(perseus):
		print('\t%s'%filename)
		convert_perseus('%s/%s'%(perseus,filename))
	print('Converting PROIEL files')
	print('\thdt.xml')
	convert_proiel('%s/hdt.xml'%proiel)
	print('\tgreek-nt.xml')
	convert_proiel('%s/greek-nt.xml'%proiel)
	pickle.dump(converted, open("%s/converted.p"%o_dir, "wb" ))
	
all_sentences = set()
for idx,x in enumerate(re.split(".\tSENT|;\tSENT", converted)):
	all_sentences.add('~%s~'%idx+x+'.\tSENT')
sentences_per_fold = int(len(all_sentences)/10)
print('Generating 10 random folds [Fold size: %s]'%sentences_per_fold)
folds = {}
for n in range(9):
	for x in range(sentences_per_fold):
		folds.setdefault(n,[]).append(re.sub('~.*?~\n?','\n',all_sentences.pop()))
folds[9]=[re.sub('~.*?~\n?','\n',x) for x in all_sentences]

for (fold,sentences) in folds.items():
	open('%s/fold_%s.txt'%(o_dir,fold),'w').write(''.join(sentences).strip())
	
table = {}

for n in range(10):
	print('Training on all folds except %s'%n)	
	#generate training set
	training='%s/training/training_%s.txt'%(o_dir,n)
	training_set = []
	print('\tGenerating training set')
	if os.path.isfile(training): os.remove(training)
	for file in os.listdir(o_dir):
		if os.path.splitext(file)[1]=='.txt':
			index = int(file.split('.')[0].split('_')[1])
			if index != n:
				training_set.append(open('%s/%s'%(o_dir,file),'r').read())
	training = open(training, 'w+').write('\n'.join(training_set))
	print('\tGenerating TreeTagger parameters')
	check_call(['%s/train-tree-tagger'%treetagger, 'TreeTaggerData/lexicon.txt', 'TreeTaggerData/openclass.txt', 'TreeTaggerData/10-fold/training/training_%s.txt'%n,'TreeTaggerData/10-fold/params/ancient_greek_%s.dat'%n], stdout=DEVNULL, stderr=STDOUT)
	print('Testing on fold %s'%n)
	print('\tGenerating test file')
	test_fold = open('%s/fold_%s.txt'%(o_dir,n), 'r')
	test_file = '%s/test/test_%s.txt'%(o_dir,n)
	if os.path.isfile(test_file): os.remove(test_file)
	open(test_file, 'a+').write('\n'.join([line.split('\t')[0] for line in test_fold]))
	print('\tTagging test file with TreeTagger')
	check_call(['%s/tree-tagger'%treetagger, '%s/params/ancient_greek_%s.dat'%(o_dir,n),'%s/test/test_%s.txt'%(o_dir,n),'%s/test_tagged/test_%s.txt'%(o_dir,n), '-token', '-lemma'], stdout=DEVNULL, stderr=STDOUT)
	print('\tComparing tagging with benchmark')
	a_lines=[x for x in open('%s/test_tagged/test_%s.txt'%(o_dir,n), 'r')]
	c_lines=[x for x in open('%s/fold_%s.txt'%(o_dir,n), 'r')]
	output = '%s/results/test_fold_%s.txt'%(o_dir,n)
	if os.path.isfile(output): os.remove(output)
	output = open(output, 'a+')
	trues = 0
	POS_list = {} #number of forms tagged as N by TreeBanker
	POS_list_benchmark = {} #number of forms annotated as N in the treebank
	POS_list_correct = {} #number of forms correctly tagged as N
	for idx, x in enumerate(range(0,len(a_lines))):
		#output.write('%s\t%s\t%s\n'%(a_lines[idx].strip(),c_lines[idx].strip(),a_lines[idx] == c_lines[idx]))
		POS_a=a_lines[idx].strip().split('\t')[1]
		POS_c=c_lines[idx].strip().split('\t')[1]
		POS_list.setdefault(POS_a,0)
		POS_list[POS_a]+=1
		POS_list_benchmark.setdefault(POS_c,0)
		POS_list_benchmark[POS_c]+=1
		POS_list_correct.setdefault(POS_a,0)
		if a_lines[idx].strip().split('\t')[0:2] == c_lines[idx].strip().split('\t')[0:2]:
			trues+=1
			POS_list_correct[POS_a]+=1
	percent_true = round(trues*100/len(a_lines),2)
	output.write('======================== GENERAL RESULTS ========================')
	output.write('\n\nAccuracy: %d%%'%percent_true)
	table.setdefault('accuracy',[]).append(percent_true)

	#Precision = (number of forms correctly tagged as N)/(number of forms tagged as N)
	#Recall = (number of forms correctly tagged as N)/(number of Ns in the gold standard)
	#F-score = 2*(precision*recall)/(precision +recall)
	for POS,count in POS_list.items():
		tagged_as_N=count
		correctly_tagged=POS_list_correct.get(POS,0)
		count_in_gold_standard=POS_list_benchmark.get(POS,0)
		try:
			precision = correctly_tagged/tagged_as_N
		except:
			precision = 'N/A'
		try:
			recall = correctly_tagged/count_in_gold_standard
		except:
			recall = 'N/A'
		try:
			Fscore = 2*(precision*recall)/(precision+recall)
		except:
			Fscore = 'N/A'
		output_string = '\n\n'
		output_string += 30*'#'
		output_string +=('\n# %s%s#'%(POS,(27-len(POS))*' '))
		output_string +=('\n'+30*'#')
		output_string +=('\n\tnumber of forms tagged as %s: %d'%(POS, tagged_as_N))
		output_string +=('\n\tnumber of forms annotated as %s in treebank: %d'%(POS, count_in_gold_standard))
		output_string +=('\n\tnumber of forms correctly tagged: %d'%correctly_tagged)
		output_string +=('\n\tPrecision:\t%s'%precision)
		output_string +=('\n\tRecall:\t\t%s'%recall)
		output_string +=('\n\tF-score:\t%s'%Fscore)
		table.setdefault('%s:precision'%POS,[]).append(precision)
		table.setdefault('%s:recall'%POS,[]).append(recall)
		table.setdefault('%s:F-score'%POS,[]).append(Fscore)
		output.write(output_string)
	output.close()	
print('Calculating overall results')
pos = ['noun','proper','verb','adjective','pronoun','article','adverb','preposition','particle','conjunction','interjection','SENT','unknown']
f1=lambda x: x+':precision'
f2=lambda x: x+':recall'
f3=lambda x: x+':F-score'
t_fields = ['accuracy']+[f(x) for x in pos for f in (f1,f2,f3)]
table=pd.DataFrame(data=table, index=['Fold-%s'%x for x in range(10)])	
table=table[t_fields]
mean = []
stdev = []
sterr = []
cfint = []
for idx,field in enumerate(t_fields):
	curr_col = table.iloc[:,idx]
	mean.append(curr_col.mean())
	stdev.append(np.std(curr_col, ddof=1))
	sterr.append(stats.sem(curr_col))
	confint=stats.norm.interval(0.95,loc=curr_col.mean(),scale=stats.sem(curr_col))
	cfint.append('±'+str((confint[1]-confint[0])/2))
table2=pd.DataFrame([mean,stdev,sterr,cfint], columns=t_fields, index=['mean','STD','STE','95%-CI'])
output = '%s/results/results.csv'%o_dir
if os.path.isfile(output): os.remove(output)
with pd.option_context('expand_frame_repr', False):
	open(output, 'w+').write(re.sub(' {1,}',',',table.append(table2).to_string()))
print('All done')