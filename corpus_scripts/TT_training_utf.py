import os
import configparser
import re
from beta2utf import convertBeta
os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if input('Convert lexicon? [y/n] ') == 'y':
	print('Converting lexicon')
	if os.path.isfile('%s/TreeTaggerData/lexicon_utf.txt'%os.path.dirname(os.path.realpath(__file__))): os.remove('%s/TreeTaggerData/lexicon_utf.txt'%os.path.dirname(os.path.realpath(__file__)))
	lexicon = open('%s/TreeTaggerData/lexicon.txt'%os.path.dirname(os.path.realpath(__file__)), 'r')
	lexicon_utf = open('%s/TreeTaggerData/lexicon_utf.txt'%os.path.dirname(os.path.realpath(__file__)), 'a')
	lines = [x for x in lexicon]
	for line in lines:
		lemma = line.split('\t')[0]
		parses = line.split('\t')[1:]
		lexicon_utf.write('%s\t%s'%(convertBeta(lemma), '\t'.join(parses)))
	lexicon_utf.close

if input('Convert training set? [y/n] ') == 'y':
	print('Converting training set')
	if os.path.isfile('%s/TreeTaggerData/training_set_utf.txt'%os.path.dirname(os.path.realpath(__file__))): os.remove('%s/TreeTaggerData/training_set_utf.txt'%os.path.dirname(os.path.realpath(__file__)))
	lexicon = open('%s/TreeTaggerData/training_set.txt'%os.path.dirname(os.path.realpath(__file__)), 'r')
	lexicon_utf = open('%s/TreeTaggerData/training_set_utf.txt'%os.path.dirname(os.path.realpath(__file__)), 'a')
	lines = [x for x in lexicon]
	for line in lines:
		lemma = line.split('\t')[0]
		parses = line.split('\t')[1:]
		lexicon_utf.write('%s\t%s'%(convertBeta(lemma), '\t'.join(parses)))
	lexicon_utf.close

print('Training')
config = configparser.ConfigParser()
config.read('config.ini')
treetagger = config['paths']['treetagger']
os.system("{tt_folder}/train-tree-tagger {curr_folder}/TreeTaggerData/lexicon_utf.txt {curr_folder}/TreeTaggerData/openclass.txt {curr_folder}/TreeTaggerData/training_set_utf.txt {curr_folder}/TreeTaggerData/ancient_greek_utf.dat".format(tt_folder=treetagger, curr_folder=os.path.dirname(os.path.realpath(__file__))))