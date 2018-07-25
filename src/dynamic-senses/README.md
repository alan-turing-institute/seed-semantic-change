### Bash script to compute likelihood on 50-word experiment

Open the files params_copyfile.txt and params_copyfile_test.txt and edit them in the same way with the values of the parameters you are interested in. Save them with the same names.

Copy and paste each un-commented line on the terminal.

##### DO THESE ONCE FOR EACH PARAMETER SETTING

//create param file for each word in the targets_50.txt file.

while read p;  do
sed "s/1083/$p/" params_copyfile.txt > params_$p.txt
done <greek_input/targets_50.txt

// By default, the new 50 parameter files are stored in /dynamic-senses. If you want to store them in a different folder (called "likelihood_params") within /dynamic-senses, create it and then do this:

while read p;  do
sed "s/1083/$p/" params_copyfile.txt > likelihood_params/params_$p.txt
done <greek_input/targets_50.txt

// NB for one word, no parameter file is created.

while read p;  do
sed "s/1083/$p/" params_copyfile_test.txt > params_test_$p.txt
done <greek_input/targets_50.txt

// By default, the new 50 parameter files are stored in /dynamic-senses. If you want to store them in a different folder (called "likelihood_params") within /dynamic-senses, do this:

while read p;  do
sed "s/1083/$p/" params_copyfile_test.txt >  likelihood_params/params_test_$p.txt
done <greek_input/targets_50.txt

##### DO THESE ONCE, independently of the parameters

//create target file for each word:

cd greek_input;
while read p;  do
sed "s/1083/$p/" target_copyfile.txt > target_$p.txt
done <targets_50.txt

// By default, the new 50 target files are stored in /greek-input. If you want to store them in a different folder (called "likelihood_targets") within /greek-input, create it and then do this:

cd greek_input;
while read p;  do
sed "s/1083/$p/" target_copyfile.txt > likelihood_targets/target_$p.txt
done <targets_50.txt

// NB for one word, no file is created.

// create directories:

mkdir subcorpora
cd subcorpora
mkdir training

// for each target word create one target_corpora directory and one output directory:

cd ..;
cd ..;
while read p;  do
mkdir ./greek_input/subcorpora/training/$p'_target_corpora'
done <greek_input/targets_50.txt

while read p;  do
mkdir ./greek_input/subcorpora/training/$p'_output'
done <greek_input/targets_50.txt


##### CREATE TRAIN CORPUS FOR EACH WORD


while read p;  do
go run *.go -parameter_file=./params_$p.txt  -create_corpus  -store=true;
done <greek_input/targets_50.txt

// If your parameter files are in a folder called "likelihood_params" within /dynamic-senses, do this:

while read p;  do
go run *.go -parameter_file=./likelihood_params/params_$p.txt  -create_corpus  -store=true;
done <greek_input/targets_50.txt

STOP HERE!!!

##### CREATE TEST CORPUS FOR EACH WORD

while read p;  do
go run *.go -parameter_file=./params_test_$p.txt  -create_corpus  -store=true;
done <greek_input/targets_50.txt

________________


##### Clean target corpora (needed for loglikelihood)

rm -r ./greek_input/subcorpora/training/\*_target_corpora/\*        
rm -r ./greek_input/subcorpora/training/\*_output/\*      


##### RUN CODE FOR EACH WORD (most expensive part)

while read p;  do
go run *.go -parameter_file=./params_$p.txt  -store=true;
done <greek_input/targets_50.txt


##### Output file with aggregated_likelihood:

./aggregate_likelihood.R

