from lxml import etree as document
import os
import sys
import re
from grkFrm import greekForms
from utf2beta import convertUTF
import configparser

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
proiel = config['paths']['proiel']
perseus = config['paths']['perseus_tb']

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
"e":"interjection"
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
			newLine = '\t'.join([form, pos])
			if word.get('presentation-after') != " ":
				newLine+='\n{mark}\t{mark}'.format(mark=word.get('presentation-after').strip())
		except:
			continue
		converted += '%s\n'%newLine
	converted=converted.strip()
	del parse, words

def convert_perseus(file):
	global converted
	parse = open(file,'r').read()
	words=re.findall('.*?word id=".*?" form="(.*?)".*?postag="(.)', parse)
	for word in words:
		try:
			newLine = ''
			form = convertUTF(word[0])
			pos = perseus_pos.get(word[1],word[0])
			newLine = '\t'.join([form, pos])
		except:
			continue
		converted += '%s\n'%newLine
	converted=converted.strip()
	del parse, words

print('Converting Perseus files')
for filename in os.listdir(perseus):
	print('\t%s'%filename)
	convert_perseus('%s/%s'%(perseus,filename))
		
print('Converting PROIEL files')
print('\thdt.xml')
convert_proiel('%s/hdt.xml'%proiel)
print('\tgreek-nt.xml')
convert_proiel('%s/greek-nt.xml'%proiel)

open('TreeTaggerData/training_set.txt','w').write(converted)
print('All done')