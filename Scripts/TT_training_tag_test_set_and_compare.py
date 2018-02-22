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
POS_list = {} #number of forms tagged as N by TreeBanker
POS_list_benchmark = {} #number of forms annotated as N in the treebank
POS_list_correct = {} #number of forms correctly tagged as N
for idx, x in enumerate(range(0,len(a_lines))):
	output.write('%s\t%s\t%s\n'%(a_lines[idx].strip(),c_lines[idx].strip(),a_lines[idx] == c_lines[idx]))
	POS_a=a_lines[idx].strip().split('\t')[1]
	POS_c=c_lines[idx].strip().split('\t')[1]
	POS_list.setdefault(POS_a,0)
	POS_list[POS_a]+=1
	POS_list_benchmark.setdefault(POS_c,0)
	POS_list_benchmark[POS_c]+=1
	POS_list_correct.setdefault(POS_a,0)
	if a_lines[idx] == c_lines[idx]:
		trues+=1
		POS_list_correct[POS_a]+=1
percent_true = round(trues*100/len(a_lines),2)
print('\n\nMatch: %d%%'%percent_true)
output.write('\n\nMatch: %d%%'%percent_true)


#Precision = (number of forms correctly tagged as N)/(number of forms tagged as N)
#Recall = (number of forms correctly tagged as N)/(number of Ns in the gold standard)
#F-score = 2*(precision*recall)/(precision +recall)

for POS,count in POS_list.items():
	tagged_as_N=count
	correctly_tagged=POS_list_correct.get(POS,0)
	count_in_gold_standard=POS_list_benchmark.get(POS,0)
	try:
		precision = correctly_tagged/tagged_as_N
	except:
		precision = 'N/A'
	try:
		recall = correctly_tagged/count_in_gold_standard
	except:
		recall = 'N/A'
	try:
		Fscore = 2*(precision*recall)/(precision+recall)
	except:
		Fscore = 'N/A'
	output_string = '\n\n'
	output_string += 30*'#'
	output_string +=('\n# %s%s#'%(POS,(27-len(POS))*' '))
	output_string +=('\n'+30*'#')
	output_string +=('\n\tnumber of forms tagged as %s: %d'%(POS, tagged_as_N))
	output_string +=('\n\tnumber of forms annotated as %s in treebank: %d'%(POS, count_in_gold_standard))
	output_string +=('\n\tnumber of forms correctly tagged: %d'%correctly_tagged)
	output_string +=('\n\tPrecision:\t%s'%precision)
	output_string +=('\n\tRecall:\t\t%s'%recall)
	output_string +=('\n\tF-score:\t%s'%Fscore)
	print(output_string)
	output.write(output_string)
output.close()