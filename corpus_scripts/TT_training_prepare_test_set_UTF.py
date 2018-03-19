import os
import configparser
from lxml import etree as document
from utf2beta import convertUTF

os.chdir(os.path.dirname(os.path.realpath(__file__)))
config = configparser.ConfigParser()
config.read('config.ini')
treetagger = config['paths']['treetagger']
perseus = config['paths']['perseus_tb']

#Creating test set
#Transform files in lists of words

perseus_pos = {
"n":"noun",
"v":"verb",
"t":"verb",
"a":"adjective",
"d":"adverb",
"l":"article",
"g":"particle",
"c":"conjunction",
"r":"preposition",
"p":"pronoun",
"m":"adjective",
"i":"interjection",
"e":"interjection",
"u":"SENT",
"-":"unknown",
"x":"unknown"
}

test_set = ['tlg0007.tlg015.perseus-grc1.tb.xml','tlg0008.tlg001.perseus-grc1.13.tb.xml','tlg0011.tlg004.perseus-grc1.tb.xml','tlg0012.tlg002.perseus-grc1.tb.xml','tlg0020.tlg002.perseus-grc1.tb.xml','tlg0085.tlg002.perseus-grc2.tb.xml','tlg0540.tlg015.perseus-grc1.tb.xml']
open('TreeTaggerData/test_set_utf.txt','w')
open('TreeTaggerData/test_set_benchmark_utf.txt','w')
test_set_output=open('TreeTaggerData/test_set_utf.txt','a')
test_set_benchmark=open('TreeTaggerData/test_set_benchmark_utf.txt','a')
for filename in test_set:
	print('Converting %s'%filename)
	open('TreeTaggerData/TestSetFilesUTF/%s.txt'%filename[:-4],'w')
	test_set_file_output=open('TreeTaggerData/TestSetFilesUTF/%s.txt'%filename[:-4],'a')
	open('TreeTaggerData/TestSetFilesUTF/%s_benchmark.txt'%filename[:-4],'w')
	test_set_file_benchmark=open('TreeTaggerData/TestSetFilesUTF/%s_benchmark.txt'%filename[:-4],'a')
	parse = document.parse('%s/%s'%(perseus,filename))
	words = parse.xpath('//word')
	for word in words:
		if word.get('artificial') == None:
			test_set_output.write(word.get('form')+"\n")
			test_set_file_output.write(word.get('form')+"\n")
			postag=word.get('postag')
			if len(postag) > 0:
				pos = perseus_pos[word.get('postag')[0]]
			else:
				pos = 'unknown'
			test_set_benchmark.write('%s\t%s\n'%(word.get('form'),pos))
			test_set_file_benchmark.write('%s\t%s\n'%(word.get('form'),pos))
	test_set_file_output.close()
	test_set_file_benchmark.close()
test_set_output.close()
test_set_benchmark.close()
print('All done')