import re
import os
from grkLemmata import greekLemmata

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")

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
newDict = re.sub('\t((nlsj)?\d+)', lambda x : '\t'+greekLemmata[x.group(1)]['pos']+'\t'+x.group(1), newDict)
open('TreeTaggerData/lexicon.txt', 'w').write(newDict)
print('All done')