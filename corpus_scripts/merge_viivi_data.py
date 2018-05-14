import os
import sys
from lxml import etree
from openpyxl import load_workbook
import configparser

os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()
config.read('config.ini')

file_list = config['paths']['file_list']
annotated = config['paths']['annotated']
viivi = config['paths']['annotated_by_viivi']

wb2 = load_workbook('%s/file_list.xlsx'%file_list)
ws2 = wb2.active
headers = ws2[config['excel_range']['headers']]
h_file = {cell.value : n for n, cell in enumerate(headers[0])}
files = ws2[config['excel_range']['range']]

kosmos = 59339

for file in files:
	destination = '%s/%s'%(annotated,file[h_file['Tokenized file']].value)
	source = '%s/%s'%(viivi,file[h_file['Tokenized file']].value)
	date = file[h_file['Date']].value
	parse_s = etree.parse(source)
	
	#preliminary checks
	#kosmos_hits = len(parse_s.xpath('//word[lemma/@id="%s"]'%kosmos))
	#anno_hits = len(parse_s.xpath('//word[lemma/@sense!=""]'))
	#if kosmos_hits < anno_hits:
	#	print('; '.join([x.get('entry') for x in parse_s.xpath('//word/lemma[@sense!="" and @id!="%s"]'%kosmos)]))
	
	#preliminary processing: add my name to annotations before I add Viivi's
	#parse_d = etree.parse(destination)
	#anno_hits = parse_d.xpath('//word/lemma[@sense!=""]')
	#for hit in anno_hits:
	#	hit.set('annotator', 'Alessandro Vatri')
	#parse_d.write(destination, xml_declaration = True, encoding='UTF-8', pretty_print=True)
	
	kosmos_hits = parse_s.xpath('//word/lemma[@id="%s" and @sense!=""]'%kosmos)
	if len(kosmos_hits) > 0:
		#load file to merge thing in
		parse_d = etree.parse(destination)
		print('Processing %s; date: %s, hits: %d'%(file[h_file['Tokenized file']].value, date, len(kosmos_hits)))
		for hit in kosmos_hits:
			hit_location = (hit.getparent().getparent().get('id'), hit.getparent().get('id'))
			des_location = parse_d.xpath('//sentence[@id="%s"]/word[@id="%s"]/lemma[@id="%s"]'%(hit_location[0],hit_location[1],kosmos))
			if len(des_location) != 1:
				print('Doh!\n\tOffending file: %s\n\tOffending location: s %s, w %s'%(destination,hit_location[0],hit_location[1]))
				sys.exit()
			else:
				des_location=des_location[0]
				des_location.set('sense', hit.get('sense'))
				des_location.set('notes', hit.get('notes'))
				des_location.set('annotator', 'Viivi Lähteenoja')
		parse_d.write(destination, xml_declaration = True, encoding='UTF-8', pretty_print=True)