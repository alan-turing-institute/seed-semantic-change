import re
import os
from grkLemmata import greekLemmata
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")

dictionary = {}
dictionary['.']={'SENT'}
dictionary[';']={'SENT'}
dictionary[':']={'SENT'}
dictionary['?']={'SENT'}
dictionary[',']={','}
dictionary['unknown']={'unknown'}

def create_dictionary(word, pos):
	dictionary.setdefault(word,set()).add(pos)
	
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
newDict = re.sub('\t((nlsj)?\d+)', lambda x : '\t'+greekLemmata[x.group(1)]['pos'], newDict)
newDictLines = newDict.split("\n")

for line in newDictLines:
	components = line.split("\t")
	w = set()
	w.update([y for y in components[1:]])
	dictionary[components[0]]=w

print('Lexicon imported')
print('Now for integration with treebank data')

source=open('TreeTaggerData/training_set.txt','r').read()
lines = source.split("\n")
for line in lines:
	form = line.split("\t")[0]
	pos = line.split("\t")[1]
	create_dictionary(form,pos)

dictiostring = ''
for entry in dictionary.items():
	dictiostring += '%s\t%s\t-\n'%(entry[0],'\t-\t'.join([b for b in entry[1]]))
print('All done! Yay!')
open('TreeTaggerData/lexicon.txt','w').write(dictiostring.strip())