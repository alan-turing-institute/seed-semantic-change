import re
import os
import sys
from openpyxl import load_workbook
import configparser
from stop_cltk import STOPS_LIST

os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))
config = configparser.ConfigParser()
config.read('config.ini')

file_list = config['paths']['file_list']
af = config['paths']['annotated']
lf = config['paths']['as_lemmata']
filterStopWords=config['params']['filter_stop_words']

wb = load_workbook('%s/file_list.xlsx'%file_list)
ws = wb.active
files = ws['A2:Q803']

os.system("clear && printf '\e[3J'")

for record in files:
	file = '%s/%s'%(af,record[6].value)
	try:
		finalTxt = open(file, 'r').read().replace("\n", "").replace(" ", "")
		finalTxt = re.sub('.*?<body>(.*?)</body>.*', r'\1', finalTxt)
		finalTxt = re.sub('<punct.*?/>', '', finalTxt)
		finalTxt = re.sub('<sentenceid="(.*?)"location="(.*?)">', r'\1 (\2): ', finalTxt)
		finalTxt = re.sub('<word.*?entry="(.*?)".*?</word>', r'\1 ', finalTxt)
		finalTxt = re.sub('</sentence>', '\n', finalTxt)
		if filterStopWords == "True":
			for stop in STOPS_LIST:
				finalTxt = finalTxt.replace(' %s '%stop, ' ')
		open('%s/%s'%(lf,record[6].value.replace('xml', 'txt')),'w').write(finalTxt)
		print(record[6].value, 'done')
	except:
		pass