import re
import os
import sys
import configparser
from lxml import etree as document
from utf2beta import convertUTF
from beta2utf import convertBeta
from grkLemmata import greekLemmata

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")

config = configparser.ConfigParser()
config.read('config.ini')

proiel = config['paths']['proiel']
perseus = config['paths']['perseus_tb']

dictionary = {}

start_dict = open('grkFrm.py', 'r').read()
print('Bear with me a sec...')
newDict = start_dict.replace('greekForms = {\n','')
newDict = newDict.replace(',\n','\n')
newDict = re.sub(", 'a': \['.*?'\]", "", newDict)
newDict = re.sub("{'l': '(.*?)'}", r"\1", newDict)
newDict = re.sub("\[(.*?)\]", r"\1", newDict)
newDict = newDict.replace(', ', '\t')
newDict = newDict.replace('":', '\t')
newDict = newDict.replace('"', '')
newDict = newDict.replace(',', '')
newDict = newDict.replace('\n}','')
#newDict = re.sub('\t((nlsj)?\d+)', lambda x : '\t'+greekLemmata[x.group(1)]['pos']+'\t'+x.group(1), newDict)
newDict = re.sub('\t((nlsj)?\d+)', lambda x : '\t'+greekLemmata[x.group(1)]['pos']+'%'+greekLemmata[x.group(1)]['lemma'], newDict)
newDictLines = newDict.split("\n")
for line in newDictLines:
	components = line.split("\t")
	w = {}
	for y in components[1:]:
		w.setdefault(y.split('%')[0],set()).add(y.split('%')[1])
	dictionary[components[0]]=w

print('Lexicon imported')
print('Now for integration with treebank data')


converted = ''


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
}

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
	parse = document.parse(file)
	words = parse.xpath('//token')
	for word in words:
		try:
			newLine = ''
			form = convertUTF(word.get('form'))
			pos = proiel_pos.get(word.get('part-of-speech'),'unknown')
			lemma = word.get('lemma')
			newLine = '\t'.join([form, pos,lemma])
			#if word.get('presentation-after') != " ":
			#	newLine+='\n{mark}\t{mark}'.format(mark=word.get('presentation-after').strip())
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
			lemma=word.get('lemma')
			if len(postag) > 0:
				pos = perseus_pos[word.get('postag')[0]]
			else:
				pos = 'unknown'
			converted='%s\t%s\t%s'%(converted,pos,lemma)
	converted=converted.strip()
	del parse, words
if os.path.isfile('TreeTaggerData/training_set_lemma.txt'):
	converted=open('TreeTaggerData/training_set_lemma.txt','r').read()
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

	open('TreeTaggerData/training_set_lemma.txt','w').write(converted)

lines = converted.split("\n")
for line in lines:
	form = line.split("\t")[0]
	pos = line.split("\t")[1]
	lemma = line.split("\t")[2]
	dictionary.setdefault(form,{}).setdefault(pos,set()).add(lemma)
	
dictionary['.']={'SENT':{'.'}}
dictionary[';']={'SENT':{';'}}
dictionary[':']={'SENT':{':'}}
dictionary['?']={'SENT':{'?'}}
dictionary[',']={'SENT':{','}}
dictionary['unknown']={'unknown':{'unknown'}}

dictiostring = ''
for key,value in dictionary.items():
	dictiostring += key
	dictiostring += '\t'
	dictiostring += '\t'.join(['%s\t%s'%(value, '/'.join([x for x in dictionary[key][value]])) for value in dictionary[key]])
	dictiostring += '\n'

open('TreeTaggerData/lexicon_lemma.txt','w').write(dictiostring.strip())

dictiostring = ''
dictioUTF = {}
for key,value in dictionary.items():
	dictioUTF.setdefault(convertBeta(key),value)
	
for key,value in dictioUTF.items():
	dictiostring += key
	dictiostring += '\t'
	dictiostring += '\t'.join(['%s\t%s'%(value, '/'.join([x for x in dictioUTF[key][value]])) for value in dictioUTF[key]])
	dictiostring += '\n'

open('TreeTaggerData/lexicon_lemma_utf.txt','w').write(dictiostring.strip())
print('All done! Yay!')