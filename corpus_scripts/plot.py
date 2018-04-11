import os
import re
import configparser
import matplotlib.pyplot as plot
import matplotlib.colors as colors
import numpy
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
colour={}
colours={hex for name, hex in colors.cnames.items()}

for file in input_files:
	lf = open('%s/senses_%s.txt'%(dir,file), 'r')
	for line in lf:
		if re.search('[\-\d]', line[0]) == None:
			continue
		sense = line.split('\t')[-2]
		if sense =='w':
			continue
		genre = line.split('\t')[2]
		century = line.split('\t')[0]
		scores.setdefault((sense,genre,century),0)
		scores[(sense,genre,century)]+=1
		try:
			colour[sense]
		except:
			colour[sense]=colours.pop()

#by genre
print('Generating plots per genre')
genres = {}
for (sense,genre,century),score in scores.items():
	word=sense[:sense.find('-')]
	genres.setdefault(genre,{}).setdefault(word,{}).setdefault(sense,{}).setdefault(century,score)
#a plot per genre
for genre,words in genres.items():
	colLabels=[str(x) for x in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5]]
	Ncols=numpy.arange(len(colLabels))
	fig,ax=plot.subplots()
	ax.set_xlabel('Centuries')
	ax.set_ylabel('Raw frequency')
	ax.set_xticks(Ncols)
	ax.set_xticklabels(colLabels)
	ax.set_title(genre)
	width = 0.2
	colPositions = []
	if len(words.items()) == 1: colPositions.append(Ncols)
	elif len(words.items()) == 2:
		colPositions.append([x-width/2 for x in Ncols])
		colPositions.append([x+width/2 for x in Ncols])
	elif len(words.items()) == 3:
		colPositions.append([x-width for x in Ncols])
		colPositions.append(Ncols)
		colPositions.append([x+width for x in Ncols])
	for word_idx,(word,senses) in enumerate(words.items()):
		scores_plot_totals = [0 for x in colLabels]
		for sense_idx,(sense,centuries) in enumerate(senses.items()):
 			scores_plot = []
 			for x in colLabels:
 				scores_plot.append(centuries.get(x, 0))
 			ax.bar(colPositions[word_idx],scores_plot, width,bottom=scores_plot_totals,color=colour[sense],label='%s: %s'%(word,word_senses[sense]))
 			scores_plot_totals=[scores_plot_totals[idx]+x for idx,x in enumerate(scores_plot)]
	ax.legend(loc='best', fontsize='x-small')
	plot.savefig('%s/plots/%s.png'%(dir,genre), format='png')

#by time
print('Generating plots per century')
centuries = {}
for (sense,genre,century),score in scores.items():
	word=sense[:sense.find('-')]
	centuries.setdefault(century,{}).setdefault(word,{}).setdefault(sense,{}).setdefault(genre,score)	

colLabels=[str(x) for x,t in genres.items()]
for century,words in centuries.items():
	Ncols=numpy.arange(len(colLabels))
	fig,ax=plot.subplots()
	ax.set_xticks(Ncols)
	ax.set_xticklabels(colLabels,rotation='vertical')
	ax.set_xlabel('Genres')
	ax.set_ylabel('Raw frequency')
	if int(century)<0:
		century=century[1:]+' BC'
	else:
		century=century+' AD'
	ax.set_title(century)
	width = 0.2
	colPositions = []
	if len(words.items()) == 1: colPositions.append(Ncols)
	elif len(words.items()) == 2:
		colPositions.append([x-width/2 for x in Ncols])
		colPositions.append([x+width/2 for x in Ncols])
	elif len(words.items()) == 3:
		colPositions.append([x-width for x in Ncols])
		colPositions.append(Ncols)
		colPositions.append([x+width for x in Ncols])
	for word_idx,(word,senses) in enumerate(words.items()):
		scores_plot_totals = [0 for x in colLabels]
		for sense_idx,(sense,genres) in enumerate(senses.items()):
 			scores_plot = []
 			for x in colLabels:
 				scores_plot.append(genres.get(x, 0))
 			ax.bar(colPositions[word_idx],scores_plot, width,bottom=scores_plot_totals,color=colour[sense],label='%s: %s'%(word,word_senses[sense]))
 			scores_plot_totals=[scores_plot_totals[idx]+x for idx,x in enumerate(scores_plot)]
	ax.legend(loc='best', fontsize='x-small')
	plot.tight_layout()
	plot.savefig('%s/plots/%s.png'%(dir,century), format='png')