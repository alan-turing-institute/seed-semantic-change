### Bash script to compute likelihood on 50-word experiment


##### DO THESE ONCE FOR EACH PARAMETER SETTING

//create param file for each word

while read p;  do
sed "s/1083/$p/" params_copyfile.txt > params_$p.txt
done <greek_input/targets_50.txt

while read p;  do
sed "s/1083/$p/" params_copyfile_test.txt > params_test_$p.txt
done <greek_input/targets_50.txt


##### DO THESE ONCE

//create target  file for each word

cd greek_input;
while read p;  do
sed "s/1083/$p/" target_copyfile.txt > target_$p.txt
done <targets_50.txt

//create outputdir

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

