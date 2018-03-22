import os
import configparser
import re
from beta2utf import convertBeta
os.system("clear && printf '\e[3J'")
os.chdir(os.path.dirname(os.path.realpath(__file__)))

print('Training')
config = configparser.ConfigParser()
config.read('config.ini')
treetagger = config['paths']['treetagger']
os.system("{tt_folder}/train-tree-tagger {curr_folder}/TreeTaggerData/lexicon_lemma_utf.txt {curr_folder}/TreeTaggerData/openclass.txt {curr_folder}/TreeTaggerData/training_set_utf.txt {curr_folder}/TreeTaggerData/ancient_greek_utf_l.dat".format(tt_folder=treetagger, curr_folder=os.path.dirname(os.path.realpath(__file__))))

os.system("{tt_folder}/train-tree-tagger {curr_folder}/TreeTaggerData/lexicon_lemma.txt {curr_folder}/TreeTaggerData/openclass.txt {curr_folder}/TreeTaggerData/training_set.txt {curr_folder}/TreeTaggerData/ancient_greek_l.dat".format(tt_folder=treetagger, curr_folder=os.path.dirname(os.path.realpath(__file__))))