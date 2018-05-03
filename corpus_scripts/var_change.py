import os
import re
import configparser
import numpy as np
import pandas as pd
import sys
from openpyxl import load_workbook

os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))
config = configparser.ConfigParser()
config.read('config.ini')
dir = config['paths']['output']
resources = config['paths']['file_list']

wb = load_workbook('%s/word_senses.xlsx'%resources)
ws = wb.active
headers = ws[config['excel_range']['headers']]
h_sense = {cell.value : n for n, cell in enumerate(headers[0])}
data = ws['A2:E23']

word_senses = {}
for record in data:
	word = record[h_sense['TERM']].value
	sense_id = record[h_sense['SENSE LSJ']].value
	sense = record[h_sense['SENSE']].value
	word_senses.setdefault(sense_id, sense)

input_files = ['15281', '69419']

scores={}
for file in input_files:
	lf = open('%s/senses_%s.txt'%(dir,file), 'r')
	for line in lf:
		if re.search('[\-\d]', line[0]) == None:
			continue
		sense = line.split('\t')[-2]
		if sense =='w':
			continue
		genre = line.split('\t')[1]
		year = int(line.split('\t')[0])
		if year >= -800 and year <= -600:
			century = '-7'
		elif year > -600 and year <= -500:
			century = '-6'
		elif year > -500 and year <= -400:
			century = '-5'
		elif year > -400 and year <= -300:
			century = '-4'
		elif year > -300 and year <= -200:
			century = '-3'
		elif year > -200 and year <= -100:
			century = '-2'
		elif year > -100 and year <= -1:
			century = '-1'
		elif year >= 0 and year < 100:
			century = '1'
		elif year >= 100 and year < 200:
			century = '2'
		elif year >= 200 and year < 300:
			century = '3'
		elif year >= 300 and year < 400:
			century = '4'
		elif year >= 400 and year < 500:
			century = '5'
		scores.setdefault((sense,genre,century),0)
		scores[(sense,genre,century)]+=1

centuries=['-7','-6','-5','-4','-3','-2','-1','1','2','3','4','5']
genres = set()
for (sense,genre,century),score in scores.items():
	word=sense[:sense.find('-')]
	genres.add(genre)
	
# { sense0 {
	#scores for t0...tn: [] | scores for t0...tn for genre0: [] | scores for t0...tn for genre...n: []
# } }

word_scores = {}
for (sense,genre,century),score in scores.items():
	word_scores.setdefault(sense,{}).setdefault(century,{}).setdefault(genre,0)
	word_scores[sense][century][genre]+=score

for century in centuries:
	for genre in genres:
		for sense,data in word_scores.items():
			word_scores[sense].setdefault(century,{}).setdefault(genre,0)

for sense,data in word_scores.items():
	table = {} #col = [ ]
	for century in centuries:
		line = []
		for genre,score in data[century].items():
			line.append(score)
			table.setdefault(genre,[]).append(score)
		table.setdefault('score', []).append(sum(line))
	table=pd.DataFrame(data=table, index=centuries)
	print(sense)
	with pd.option_context('expand_frame_repr', False):
		print(table)
		
#change points
#conditions
# (1) ∀t(x) if s(a) of w(b) is first attested in G(α), ..., G(ω) 
# (2) & G(α) or ... or G(ω) is attested at t(y) : y < x  
# (3) & w(b) is attested in G(α) or ... or G(ω) at t(y) : y < x
# (2) implicata da (3): 2 = F => 3 = F; 2 = T ¬=> 3 = T; 3 = T => 2 = T; 3 = F ¬=> 2 = F; siccome (2) & (3) devono essere T, basta che sia soddisfatta 3

#Cosa voglio:
#tabella = parola
#		|prima attestazione	|	generi
#————————————————————————————————————————————————————————
#senso1	|	secolo			|	[genere(a) ... genere(n)]



change_scores = {}
for (sense,genre,century),score in scores.items():
	word=sense[:sense.find('-')]
	change_scores.setdefault(century,{}).setdefault(century,{}).setdefault(genre,0)
	change_scores[sense][century][genre]+=score
