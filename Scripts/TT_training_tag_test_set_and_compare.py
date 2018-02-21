import os
import configparser
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
treetagger = config['paths']['treetagger']

#Tagging test set

print('Tagging test set')
os.system("{tt_folder}/tree-tagger {curr_folder}/TreeTaggerData/ancient_greek.dat {curr_folder}/TreeTaggerData/test_set.txt {curr_folder}/TreeTaggerData/test_set_tagged.txt -token".format(tt_folder=treetagger, curr_folder=os.path.dirname(os.path.realpath(__file__))))

a_lines=[x for x in open('TreeTaggerData/test_set_tagged.txt', 'r')]
c_lines=[x for x in open('TreeTaggerData/test_set_benchmark.txt', 'r')]
open('TreeTaggerData/test_set_results.txt', 'w')
output = open('TreeTaggerData/test_set_results.txt', 'a')
trues = 0
for idx, x in enumerate(range(0,len(a_lines))):
	output.write('%s\t%s\t%s\n'%(a_lines[idx].strip(),c_lines[idx].strip(),a_lines[idx] == c_lines[idx]))
	if a_lines[idx] == c_lines[idx]: trues+=1
percent_true = round(trues*100/len(a_lines),2)
print('Match: %d%%'%percent_true)
output.write('Match: %d%%'%percent_true)
output.close()