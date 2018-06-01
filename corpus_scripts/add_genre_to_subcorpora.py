import os
import configparser
import re
import sys

os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read('config.ini')
dir = config['paths']['output']
corpus = open('%s/full_corpus_ids.txt'%dir, 'r').read()
folders = ['training','test']
for subdir in folders:
	for filename in os.listdir('%s/subcorpora/%s'%(dir,subdir)):
		if filename[-4:] == '.txt':
			print('Processing','%s/%s'%(subdir,filename))
			file = open('%s/%s'%('%s/subcorpora/%s'%(dir,subdir),filename), 'r')
			currFile = []
			for line in file:
				date = line.split()[0]
				text = line.split()[1].strip()
				#find correspondence in corpus
				genre = re.search('%s\t(.*?)\t%s'%(date,text), corpus)
				try:
					genre = genre.group(1)
				except:
					print(line)
				currFile.append('%s\t%s\t%s'%(date,genre,text))
			open('%s/subcorpora/%s/with_genre/%s.txt'%(dir,subdir,filename), 'w').write('\n'.join([x for x in currFile]))
print('All done!')