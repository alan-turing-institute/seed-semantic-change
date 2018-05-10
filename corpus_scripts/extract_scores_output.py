import os
import re
import configparser
import numpy as np
import pandas as pd
import sys
from grkLemmata import greekLemmata
from lxml import etree as document
from openpyxl import load_workbook

def century(year): #change into 0 – 11
	year = int(year)
	if year >= -800 and year <= -600:
		return 0 #-7
	elif year > -600 and year <= -500:
		return 1 #-6
	elif year > -500 and year <= -400:
		return 2 #-5
	elif year > -400 and year <= -300:
		return 3 #-4
	elif year > -300 and year <= -200:
		return 4 #-3
	elif year > -200 and year <= -100:
		return 5 #-2
	elif year > -100 and year <= -1:
		return 6 #-1
	elif year >= 0 and year < 100:
		return 7 #1
	elif year >= 100 and year < 200:
		return 8 #2
	elif year >= 200 and year < 300:
		return 9 #3
	elif year >= 300 and year < 400:
		return 10 #4
	elif year >= 400 and year < 500:
		return 11 #5

os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))
config = configparser.ConfigParser()
config.read('config.ini')
dir = config['paths']['output']
file_list = config['paths']['file_list']
input = config['paths']['model_output']


carry_on = True
scores = {}

for currDir, dirs, files in os.walk(input):
	for word in dirs:
		scores.setdefault(word, {})
		file = open('%s/%s/output.dat'%(currDir,word), 'r')
		carry_on = True
		for line in file:
			if carry_on == True:
				try:
					line.split()[1][0:1]
				except IndexError:
					continue
				else:					
					if line.split()[1][0:1] == 'T':
						value = (int(re.search('T=(.*?),',line.split()[1]).group(1)),int(re.search('K=(.*?):',line.split()[1]).group(1)))
						score = float(line.split()[0])
						scores[word].setdefault(value, score)
						del value
					elif line.split()[1] == 'per' and line.split()[2] == 'time':
						carry_on = False

wb = load_workbook('%s/file_list.xlsx'%file_list)
ws = wb.active
headers = ws[config['excel_range']['headers']]
h = {cell.value : n for n, cell in enumerate(headers[0])}
files = ws[config['excel_range']['range']]
af = config['paths']['final_corpus']

genres = set()

for record in files:
	subgenre = record[h['Subgenre']].value
	genres.add(subgenre)
	file = '%s/%s'%(af,record[h['Tokenized file']].value)
	cent = century(record[h['Date']].value)
	sys.stdout.write("\r\033[KProcessing %s"%record[h['Tokenized file']].value)
	sys.stdout.flush()
	curr_text = document.parse(file)
	for word,score in scores.items():
		#print(word, len(curr_text.xpath('//word/lemma[@id="%s"]'%word)),subgenre,cent)
		ref=(cent,subgenre)
		scores[word].setdefault(ref,0)
		scores[word][ref] += len(curr_text.xpath('//word/lemma[@id="%s"]'%word))
# for word,score in scores.items():
# 	print(greekLemmata[word]['lemma'])
# 	print(score)
# 	print(30*'#','\n')

for word,score in scores.items():
	print(greekLemmata[word]['lemma'])
	print(score)
	print('\n\n\n')