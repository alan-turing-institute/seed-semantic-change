import re
import os
import sys
import configparser
from grkLemmata import greekLemmata

os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read('config.ini')

file_list = config['paths']['file_list']
af = config['paths']['final_corpus']
dir = config['paths']['output']

folders = ['training','test']
for subdir in folders:
	for filename in os.listdir('%s/subcorpora/new/%s'%(dir,subdir)):
		if filename[-4:] == '.txt':
			print('Processing','%s/%s'%(subdir,filename))
			file = open('%s/%s'%('%s/subcorpora/new/%s'%(dir,subdir),filename), 'r')
			currFile = []
			for line in file:
				date = line.split('\t')[0]
				text = line.split('\t')[2].strip()
				#find correspondence in corpus
				genre = line.split('\t')[1]
				currFile.append('%s\t%s'%(date,text))
			open('%s/subcorpora/new/no_genre/%s/%s'%(dir,subdir,filename), 'w').write('\n'.join([x for x in currFile]))
print('All done! What a joy!')



