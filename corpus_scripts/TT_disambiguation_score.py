import os
import sys
import lxml.etree as document
from utf2beta import convertUTF
from beta2utf import convertBeta
from grkFrm import greekForms 
from grkLemmata import greekLemmata
import configparser
import re
import pandas as pd
from cltk.stem.lemma import LemmaReplacer
import pickle

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
proiel = config['paths']['proiel']
treetagger = config['paths']['treetagger']
tt_root='TreeTaggerData/disamb_test'
af = '%s/annotated'%tt_root
tt_input = '%s/tt_input'%tt_root
tt_output = '%s/tagged'%tt_root
disamb = '%s/disambiguated'%tt_root

files = ['%s/hdt.xml'%proiel, '%s/greek-nt.xml'%proiel]
result_file = open('%s/results.txt'%tt_root, 'w+')

def dbl_output(*args):
	global result_file
	if len(args) == 0:
		print()
		result_file.write('\n')
	else:
		print(args[0])
		result_file.write('%s\n'%args[0])

def decoTitle(title):
	row =(len(title)+4)*'#'
	dbl_output(row)
	dbl_output('# %s #'%title)
	dbl_output(row)
	dbl_output()

#################################
# step 1: annotate proiel files #
#################################

def cleanWords(word):
	word = re.sub('[^a-z\(\)\\\/\*\|=\+\'0-9\"]*', '', word)

	#turn graves into acutes, lowercase betacode, remove clitic accent, escape diacritics
	wordForm = word.replace("2", "").replace("3", "")
	word = word.replace('\\', '/').lower()
	word = re.sub(r"\*([aehiouw])([\(\)/=]+)",r"*\2\1", word) #parole registrate maiuscole: *DIACRlettere; parole minuscole: *parola normale, quindi * + e)/ etc.
	word = re.sub(r"([\(\)/=]+)(\*)([aehiouw])",r"\2\1\3", word)
	word = re.sub(r"\|([/\(\)])",r"\g<1>|", word)
	howmanyAccents = len(re.findall("[/=]", word))
	if howmanyAccents > 1:
		word=word[::-1].replace("/", "", 1)[::-1]
	return word
	
def lookup(word):
	word = cleanWords(word)
	try:
		entry=greekForms[word]
	#no match			
	except KeyError:
		word = word.replace("+", "")
		word = re.sub(r"\*([\(\)/=]+)([aehiouw])",r"*\2\1", word)
		word2 = word.replace("'", "")
		notFound = False
		try:
			entry=greekForms[word]
		except KeyError:
			notFound = True
		else:
			return {'is_unknown':False, 'entry':entry}
		if notFound == True:
			word = word.replace("*", "")		
			try:
				entry=greekForms[word]
			except KeyError:
				word = re.sub('^c(?=u[nmg])','s', word)
				try:
					entry=greekForms[word]
				except KeyError:
					word = word.replace("'", "")
					try:
						entry=greekForms[word]
					except KeyError:
						word = re.sub("\)$", "'",word)
						try:
							entry=greekForms[word]
						except KeyError:
							word = re.sub("'$", "",word)
							try:
								entry=greekForms[word]
							except KeyError:
								word = re.sub("^\(", "",word)
								try:
									entry=greekForms[word]
								except KeyError:
									word = re.sub("\)$", "",word)
									try:
										entry=greekForms[word]
									except KeyError:
										word = re.sub("'", "",word)
										try:
											entry=greekForms[word]
										except KeyError:
											return {'is_unknown':True}
										else:
											return {'is_unknown':False, 'entry':entry}
									else:
										return {'is_unknown':False, 'entry':entry}
								else:
									return {'is_unknown':False, 'entry':entry}
							else:
								return {'is_unknown':False, 'entry':entry}
						else:
							return {'is_unknown':False, 'entry':entry}
					else:
						return {'is_unknown':False, 'entry':entry}
				else:
					return {'is_unknown':False, 'entry':entry}
			else:
					return {'is_unknown':False, 'entry':entry}
	else:
		return {'is_unknown':False, 'entry':entry}

def process(lemmata, word):	
	for lemma in lemmata:
	#each lemma is a dictionary; 'l' = entry, 'a' is a list
		newLemma = document.SubElement(word, "lemma")
		newLemma.set('id',lemma['l'])
		newLemma.set('entry',greekLemmata[lemma['l']]['lemma'])
		newLemma.set('POS',greekLemmata[lemma['l']]['pos'])
		for analysis in lemma['a']:
			newAnalysis = document.SubElement(newLemma, "analysis")
			newAnalysis.set('morph', analysis)
			del newAnalysis
		del newLemma

def annotate():
	for file in files:
		parse = document.parse(file)
		words = parse.xpath('//token')
		total = len(words)
		for idx, word in enumerate(words):
			progPercent = str(int(idx*100/total))
			sys.stdout.write("\r\033[K\tAnnotating %s. Progress: %s%%"%(os.path.basename(file), progPercent))
			sys.stdout.flush()
			#get word form
			try:
				form = convertUTF(word.get('form'))
			except:
				continue
			isunknown = False
			#lookup in dictionary
			if lookup(form)['is_unknown'] == True:
				document.SubElement(word, "lemma").set("id", "unknown")
			else:
				process(lookup(form)['entry'], word)
		parse.write('%s/%s'%(af, os.path.basename(file)), xml_declaration = True, encoding='UTF-8', pretty_print=True)

#annotate()

######################################################
# step 2: convert proiel files into TreeTagger input #
######################################################

def convert_proiel(file):
	converted = ''
	parse = document.parse(file)
	words = parse.xpath('//token')
	for word in words:
		try:
			newLine = ''
			form = convertUTF(word.get('form'))
			newLine = form
			if word.get('presentation-after') != " ":
				newLine+='\n%s'%word.get('presentation-after').strip()
		except:
			continue
		converted += '%s\n'%newLine
	converted=converted.strip()
	open('%s/%s'%(tt_input,os.path.basename(file).replace('xml','txt')), 'w').write(converted)
	del parse, words

def convert():
	print('Converting annotated files')
	for file in [x.replace(proiel,af) for x in files]:
		print('\t%s'%os.path.basename(file))
		convert_proiel(file)

#convert()

################################
# step 3: TreeTag proiel files #
################################

def treetag():
	for filename in [x.replace(proiel,'').replace('xml','txt') for x in files]:
		print('TreeTagging files')
		os.system("{tt_folder}/tree-tagger {curr_folder}/TreeTaggerData/ancient_greek.dat \"{tt_source}/{filename}\" \"{tt_output}/{filename}\" -token".format(tt_folder=treetagger, tt_source=tt_input, tt_output=tt_output, curr_folder=os.path.dirname(os.path.realpath(__file__)), filename=filename))

#treetag()

###############################################
# step 4: disambiguate annotated proiel files #
###############################################
def disambiguate():

	frequencies = pickle.load(open("lemma_frequency.p", "rb" ))
	def TT_dis(node,TT_POS):
		possible_lemmas=node.xpath('lemma[@POS="%s"]'%TT_POS)
		freq_score = []
		for lemma in possible_lemmas:
			freq_score.append((frequencies[lemma.get('id')],lemma.get('id')))
		sorted_scores = sorted(freq_score, key=lambda tup: tup[0], reverse=True)
		toAdd = node.xpath('lemma[@POS="%s"][@id="%s"]'%(TT_POS,sorted_scores[0][1]))
		toAdd.set('disambiguated', str(round(1/len(node.xpath('lemma[@POS="%s"]'%TT_POS)),2)))
		toAdd.set('TreeTagger', 'true')
		toRemove = node.xpath('lemma')
		[node.remove(x) for x in toRemove]
		node.append(toAdd)
		
	for idx,file in enumerate(files):
		file = file.replace(proiel,af)
		curr_text = document.parse(file)
		print("Disambiguating %s"%os.path.basename(file))
		init_tokens = str(len(curr_text.xpath('//token[@form]')))
		init_lemmas = str(len(curr_text.xpath('//lemma')))
		sys.stdout.write("\r\033[\tTokens: %s, lemmas: %s"%(init_tokens, init_lemmas))
		sys.stdout.flush()
		TT_doc = open(file.replace('xml','txt').replace(af,tt_output), 'r')
		TT_lines=[x for x in TT_doc]
		nodes = curr_text.xpath('//token')
		word_count = 0
		for node in nodes:
			if node.get('form') == None:
				word_count+=1
			else:
				lemma_count = len(node.xpath('./lemma'))
				if lemma_count > 1:
					TT_POS = TT_lines[word_count].split('\t')[1].strip()
					try:
						TT_dis(node,TT_POS)
					except:
						if TT_POS == 'proper':
							TT_POS='noun'
						try:
							TT_dis(node,TT_POS)
						except:
							TT_POS='adjective'
							try:
								TT_dis(node,TT_POS)
							except:
								toAdd = node.xpath('lemma')[0]
								toAdd.set('disambiguated', str(round(1/lemma_count, 2)))
								toAdd.set('TreeTagger', 'false')
								toRemove = node.xpath('lemma')
								[node.remove(x) for x in toRemove]
								node.append(toAdd)
				else:
					node.xpath('./lemma')[0].set('TreeTagger', 'false')
					node.xpath('./lemma')[0].set('disambiguated', 'n/a')
				word_count+=1				
						
		finalXML = document.tostring(curr_text, pretty_print=True, encoding='unicode')
		
		f = open('%s/%s'%(disamb,os.path.basename(file)), 'w')
		f.write(finalXML)
		f.close()
		curr_text_check = document.parse('%s/%s'%(disamb,os.path.basename(file)))
		final_tokens = str(len(curr_text_check.xpath('//token[@form]')))
		final_lemmas = str(len(curr_text_check.xpath('//lemma')))
		sys.stdout.write("\r\033[\tWord tokens: %s, lemmas: %s\tFinal: %s, lemmas:%s\n"%(init_tokens, init_lemmas, final_tokens, final_lemmas))
		sys.stdout.flush()
		if init_tokens != final_tokens: input('Problem!')
		if final_lemmas != final_tokens: input('Problem!')
		del curr_text, curr_text_check

disambiguate()

#####################################################
# step 5: compare proiel lemmatization with new one #
#####################################################
def comparison():
	decoTitle('Accuracy of lemmatization')
	for idx,file in enumerate(files):
		dbl_output((8+len(os.path.basename(file))+2)*'·')
		dbl_output('· File: %s ·'%os.path.basename(file))
		dbl_output((8+len(os.path.basename(file))+2)*'·')
		dbl_output()
		file = file.replace(proiel,disamb)
		curr_text = document.parse(file)
		words = curr_text.xpath('//token[@form]')
		count_success = 0
		count_failure = 0
		counts_disamb = {}
		for word in words:
			original_lemma = word.get('lemma').split('#')[0].lower()
			tt_lemma = word.xpath('./lemma')[0].get('entry')
			if tt_lemma != None: tt_lemma = tt_lemma.lower()
			confidence = word.xpath('./lemma')[0].get('disambiguated')
			if original_lemma==tt_lemma:
				count_success += 1
				counts_disamb.setdefault(confidence,[0,0])
				counts_disamb[confidence][0]+=1
			else:
				if tt_lemma != None:
					tt_lemma = re.sub('ω$', 'ομαι', tt_lemma, re.UNICODE)
				if original_lemma==tt_lemma:
					count_success += 1
					counts_disamb.setdefault(confidence,[0,0])
					counts_disamb[confidence][0]+=1
				else:
					if tt_lemma != None:
						tt_lemma = re.sub('ομαι$', 'ω', tt_lemma, re.UNICODE)
					if original_lemma==tt_lemma:
						count_success += 1
						counts_disamb.setdefault(confidence,[0,0])
						counts_disamb[confidence][0]+=1
					else:
						count_failure += 1
						counts_disamb.setdefault(confidence,[0,0])
						counts_disamb[confidence][1]+=1
						#dbl_output(original_lemma,tt_lemma)
		dbl_output('Successes: %d'%count_success)
		dbl_output('Failures: %d'%count_failure)
		dbl_output('Accuracy: %s%%'%str(round(count_success*100/len(words),2)))
		indexes = []
		table = []
		for y in sorted([x for x in counts_disamb.keys()]):
			percentage = round(counts_disamb[y][0]*100/sum(counts_disamb[y]),2)
			table.append(['Accuracy per confidence %s'%y,counts_disamb[y][0], sum(counts_disamb[y]), percentage])
		table = pd.DataFrame(table, columns=['','count','total','percentage'])
		table = table.append(pd.DataFrame([['Total',table.iloc[:,1].sum(),table.iloc[:,2].sum(),round(table.iloc[:,1].sum()*100/table.iloc[:,2].sum(),2)]], columns=['','count','total','percentage']))
		table = table.set_index('')
		dbl_output(table)
		dbl_output()

comparison()

#####################################################
# step 6: compare proiel lemmatization with cltk #
#####################################################
decoTitle('Accuracy of CLTK lemmatizer')
lemmatizer = LemmaReplacer('greek')
for idx,file in enumerate(files):
	dbl_output((8+len(os.path.basename(file))+2)*'·')
	dbl_output('· File: %s ·'%os.path.basename(file))
	dbl_output((8+len(os.path.basename(file))+2)*'·')
	dbl_output()
	file = file.replace(proiel,disamb)
	curr_text = document.parse(file)
	words = curr_text.xpath('//token[@form]')
	count_success = 0
	count_failure = 0
	for word in words:
		original_lemma = word.get('lemma').split('#')[0].lower()
		form = word.get('form')
		id = word.get('id')
		cltk = lemmatizer.lemmatize(form)[0].lower()
		if cltk == original_lemma:
			count_success += 1
		else:
			cltk = re.sub('ω$', 'ομαι', cltk, re.UNICODE)
			if original_lemma==cltk:
				count_success += 1
			else:
				cltk = re.sub('ομαι$', 'ω', cltk, re.UNICODE)
				if original_lemma==cltk:
					count_success += 1
				else:
					count_failure += 1
	dbl_output('Successes: %d'%count_success)
	dbl_output('Failures: %d'%count_failure)
	dbl_output('Accuracy: %s%%'%str(round(count_success*100/len(words),2)))
	dbl_output()
result_file.close()
print('All done! It was a pleasure doing this stuff for you, m8!')