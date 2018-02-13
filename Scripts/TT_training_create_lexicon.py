import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
source=open('TreeTaggerData/training_set.txt','r').read()
dictionary = {}
def create_dictionary(word, pos):
	dictionary.setdefault(word,set()).add(pos)
	
lines = source.split("\n")
for line in lines:
	form = line.split("\t")[0]
	pos = line.split("\t")[1]
	create_dictionary(form,pos)

dictionary['.']={'SENT'}
dictionary[';']={'SENT'}
dictionary[':']={'SENT'}
dictionary['?']={'SENT'}
dictionary[',']={','}

dictiostring = ''
for entry in dictionary.items():
	dictiostring += '%s\t%s\t-\n'%(entry[0],'\t-\t'.join([b for b in entry[1]]))
open('TreeTaggerData/lexicon.txt','w').write(dictiostring.strip())