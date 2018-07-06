# Time-dependent model for meaning change    

This repository contains the main code to train the model and output the inferred meanings over time.    


## Quick start    

1. Edit the GOPATH in your ~/.bash_profile file to point to the local directory where this GitHub repository seed-semantic0-change sits (e.g., export GOPATH=/path/to/seed-semantic-change/code) 

2. cd dynamic-senses     
3. mkdir ./greek_input/target_corpora    
4. mkdir	./greek_input/output       
5. go run *.go -parameter_file=greek_parameters_id.txt  -create_corpus -store=true        
6. go run *.go -parameter_file=greek_parameters_id.txt  -store=true      

The results for each target word are stored in dynamic-senses/greek_input/output/      

 
Note: steps 3 and 4 mean that you need to create (even empty) directories for the word_corpus_path and output_path indicated in the parameter file. If these folders do not exist, step 6 will raise an error.      
