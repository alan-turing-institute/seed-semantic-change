#and list of lemmas by frequency
import os
import re
from lxml import etree
from openpyxl import load_workbook
import configparser
import sys
import operator
from stop_cltk import STOPS_LIST_ID
import pickle

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
fc = config['paths']['final_corpus']
resources = config['paths']['file_list']
output = config['paths']['output']
wb2 = load_workbook('%s/file_list.xlsx'%resources)
ws2 = wb2.active
headers = ws2[config['excel_range']['headers']]
h = {cell.value : n for n, cell in enumerate(headers[0])}
files = ws2[config['excel_range']['range']]
lemmas = {}
for idx,record in enumerate(files):
	file = '%s/%s'%(fc,record[h['Tokenized file']].value)
	sys.stdout.write("\r\033[KProcessing %s"%record[h['Tokenized file']].value)
	sys.stdout.flush()
	curr_text = etree.parse(file)
	words = curr_text.xpath('//word')
	for word in words:
		lemmata = word.xpath('./lemma')
		for lemma_item in lemmata:
			lemmaid = str(lemma_item.get('id'))
			lemmas.setdefault(lemmaid, 0)
			lemmas[lemmaid]+=1
		
#sorted_list = sorted(lemmas.items(), key=operator.itemgetter(1), reverse=True)
pickle.dump(lemmas, open("lemma_frequency.p", "wb" ))

print('\n###########\n#All done!#\n###########\n')