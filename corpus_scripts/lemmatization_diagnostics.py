import sys
from lxml import etree as document
from openpyxl import load_workbook
import configparser
import os
from stop_cltk import STOPS_LIST_ID
import re
from beta2utf import convertBeta

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
annotated = config['paths']['annotated']
resources = config['paths']['file_list']
dir = config['paths']['output']
TT = config['paths']['treetagger_output']

word_id = sys.argv[1]

wb2 = load_workbook('%s/file_list.xlsx'%resources)
ws2 = wb2.active
headers = ws2[config['excel_range']['headers']]
h_file = {cell.value : n for n, cell in enumerate(headers[0])}
files = ws2[config['excel_range']['range']]

fields = ['date', 'genre', 'author', 'work', 'tlg author', 'tlg work', 'sentence location', 'sentence id', 'sentence ids', 'sentence original', 'target id', 'sense id', 'disambiguation']
count = 0
countML = 0
countPS = 0
countTT = 0
countTT_sameline = 0
countTT_sameline_number = 0
sentences = set()
for idx,record in enumerate(files):
	file = '%s/%s'%(annotated,record[h_file['Tokenized file']].value)
	#fileTT = open('%s/%s'%(TT,record[h_file['Tokenized file']].value.replace('xml','txt')), 'r').read()
	date = str(record[h_file['Date']].value)
	genre = str(record[h_file['Genre']].value)
	author = str(record[h_file['Author']].value)
	tlg_work = str(record[h_file['TLG ID']].value)
	tlg_author = str(record[h_file['TLG Author']].value)
	work = str(record[h_file['Work']].value)
	sys.stdout.write("\r\033[KChecking %s"%os.path.basename(file))
	sys.stdout.flush()
	curr_text = open(file,'r').read()
	if curr_text.find('sense') == -1: continue
	del curr_text
	curr_text = document.parse(file)
	sys.stdout.write("\r\033[KExtracting data from %s"%os.path.basename(file))
	sys.stdout.flush()
	#how many times does mus compete?
	for x in curr_text.xpath('//word[lemma/@id="%s"]'%word_id):
		sentences.add(x.xpath('./parent::sentence')[0])
		if len(x.xpath('./lemma')) > 1:
			countML +=1
			if len(x.xpath('./lemma[@id="%s"]/preceding-sibling::*'%word_id))+1 > 1: countPS +=1
	#countTT+=len(re.findall('69419',fileTT))
	count+=len(curr_text.xpath('//word[lemma/@id="%s"]'%word_id))
	
	TT_doc = open('%s/%s'%(TT,record[h_file['Tokenized file']].value.replace('xml','txt')), 'r')
	TT_lines=[x for x in TT_doc]
	finalTxt = ''
	nodes = curr_text.xpath('//sentence|//word|//punct')
	word_count = 0
	for node in nodes:
		if node.tag == 'sentence':
			finalTxt += '\n'
			finalTxt += '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(date,genre,author,work,tlg_author,tlg_work,node.get('location'),node.get('id'))			
		elif node.tag == 'word':
			lemma_count = len(node.xpath('./lemma'))
			if lemma_count == 1:
				finalTxt+='*%s*'%node.xpath('lemma/@id')[0]
			elif lemma_count > 1:
				TT_POS = TT_lines[word_count].split('\t')[1].strip()
				try:
					finalTxt+='*%s*'%node.xpath('lemma[@POS="%s"]/@id'%TT_POS)[0]
				except:
					if TT_POS == 'proper':
						TT_POS='noun'
					try:
						finalTxt+='*%s*'%node.xpath('lemma[@POS="%s"]/@id'%TT_POS)[0]
					except:
						TT_POS='adjective'
						try:
							finalTxt+='*%s*'%node.xpath('lemma[@POS="%s"]/@id'%TT_POS)[0]
						except:
							finalTxt+='*%s*'%node.xpath('lemma/@id')[0]	
			word_count+=1				
		elif node.tag == 'punct':
			word_count+=1
	del TT_doc, TT_lines, nodes, lemma_count, TT_POS
	
	for stop in STOPS_LIST_ID:
		finalTxt = re.sub('\*%s\*'%stop, '', finalTxt)
	finalTxt = re.sub('.*?\t\n','',finalTxt)
	countTT += len(re.findall('.*?\*'+word_id+'\*.*?\n', finalTxt))
	countTT_sameline += len(re.findall('.*?(\*'+word_id+'\*.*?){2,}.*?\n', finalTxt))
	for hit in re.findall('.*?(\*'+word_id+'\*.*?){2,}.*?\n', finalTxt):
		countTT_sameline_number += len(re.findall('\*'+word_id+'\*', hit))
	
print()	
print('Total hits:', count, '\nSentence nodes:', len(sentences), '\nOther lemmatizations:', countML, '\nNot first lemma node in annotated text:', countPS, '\nAfter Treetagger:', countTT, '\nAfter Treetagger, sentences with multiple occurrences:', countTT_sameline, '\nAfter TT, number of hits in multi-hit sentences:', countTT_sameline_number)