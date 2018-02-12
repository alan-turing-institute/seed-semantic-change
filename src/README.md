# Time-dependent model for meaning change    

This repository contains the main code to train the model and output the inferred meanings over time.    


## Quick start    

1. Edit the GOPATH in your ~/.bash_profile file (e.g., export GOPATH=/path/to/seed-semantic-change/code)    
2. cd dynamic-senses    
3. go run *.go -parameter_file=greek_parameters_id.txt  -store=true    

The results for each target word are stored in dynamic-senses/greek_input/output/
