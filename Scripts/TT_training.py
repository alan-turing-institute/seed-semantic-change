import os
import configparser
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("python3 %s/TT_training_create_openclass.py" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/TT_training_prepare_set.py" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/TT_training_create_lexicon.py" % (os.path.dirname(os.path.realpath(__file__))))
config = configparser.ConfigParser()
config.read('config.ini')
treetagger = config['paths']['treetagger']
os.system("{tt_folder}/train-tree-tagger {curr_folder}/TreeTaggerData/lexicon.txt {curr_folder}/TreeTaggerData/openclass.txt {curr_folder}/TreeTaggerData/training_set.txt {curr_folder}/TreeTaggerData/ancient_greek.txt".format(tt_folder=treetagger, curr_folder=os.path.dirname(os.path.realpath(__file__))))