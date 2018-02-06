import re
from grkLemmata import greekLemmata

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
open('TreeTagger Data/lexicon.txt', 'w').write(newDict)
print('All done')