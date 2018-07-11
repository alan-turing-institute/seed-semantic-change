# Time-dependent model for meaning change    

This repository contains the main code to train the model and output the inferred meanings over time.    


## Quick start    

1. Edit the GOPATH in your ~/.bash_profile file to point to the local directory where this GitHub repository seed-semantic-change sits (e.g., export GOPATH=/path/to/seed-semantic-change). You can also simply type 

export GOPATH=/path/to/seed-semantic-change

on the terminal. To check that the path is updated, type: 

go env

2. cd /path/to/seed-semantic-change/src/dynamic-senses     

3. mkdir ./greek_input/target_corpora 

only if the directory does not exist already

4. mkdir	./greek_input/output       

only if the directory does not exist already
 
5. For a full explanation of the parameters, see https://github.com/alan-turing-institute/seed-semantic-change/blob/master/src/README.webarchive 

Edit parameter file

greek_parameters.id.txt

in /path/to/seed-semantic-change/src/dynamic-senses

as follows:

a) if you want to create a new corpus:

text_corpus	./greek_input/corpus_id.txt 
for the input with ids (stays the same)
and

text_corpus	./greek_input/full_corpus_ids.txt 
for the input with characters (stays the same) NEVER CHANGE THIS!

target_words	./greek_input/targets_id.txt
for the list of target words (depends on the target words)

bin_corpus_store	./greek_input/corpus_id.bin
where the corpus bin will be saved (stays the same)

full_corpus_path	./greek_input/corpus_id.bin
where the corpus bin will be taken for training the model (stays the same)
it's the same as bin_corpus_store

full_heldout_path	./greek_input/corpus_id.bin
where the corpus bin will be taken for computing the log-likelihood (depends on the data on which to evaluate the likelihood)

window_size	5
size of window

word_corpus_path	./greek_input/target_corpora/
path to word-specific corpora (stays the same)

output_path	./greek_input/output/
output directory

start_time	-800
the earliest date in the corpus; it's -800 for the Ancient Greek corpus

end_time	400
the latest date in the corpus; it's 400 for the Ancient Greek corpus

time_interval	100
size of time interval

target_words	./greek_input/targets_id.txt
bin_corpus_store	./greek_input/corpus_id.bin
window_size	5
full_corpus_path	./greek_input/corpus_id.bin
word_corpus_path	./greek_input/target_corpora/
output_path	./greek_input/output/
kappaF	10.0
kappaK	4.0
a0	7.0
b0	3.0
num_top	5
iterations	10000
start_time	-800
end_time	400
time_interval	100
min_doc_per_word	0
max_docs_per_slice	2000


5. go run *.go -parameter_file=greek_parameters_id.txt  -create_corpus -store=true  

replace -parameter_file=NAME_OF_PARAMETER_FILE with
-parameter_file=./PATH_TO_PARAMETER_FILE/NAME_OF_PARAMETER_FILE

6. go run *.go -parameter_file=greek_parameters_id.txt  -store=true      

The results for each target word are stored in dynamic-senses/greek_input/output/      

 
Note: steps 3 and 4 mean that you need to create (even empty) directories for the word_corpus_path and output_path indicated in the parameter file. If these folders do not exist, step 6 will raise an error.    

## Git commands

To move from the master branch to the branch where the genre topic model is, cd into the directory seed-semantic-change, then:

git branch   
git checkout genre_topic_model

To go back to the master branch, type

git checkout master. 

To check whether you're in the master or other branch, type:

git branch

Depending on whether you're in the master or in a branch, the corresponding code will run.
