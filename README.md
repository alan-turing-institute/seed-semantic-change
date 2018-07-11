# Semantic change modelling from Ancient Greek texts

This code was created as part of the seed-funded project "Computational models of meaning change in natural language texts" (SF042) funded by The Alan Turing Institute, PI: Barbara McGillivray, project team: Dr Simon Hengchen, Mr Valerio Perrone, Prof Jim Smith, Dr Alessandro Vatri.

## Folder description

### Evaluation
This folder contains the Python3 code that runs the evalution of the model.

### Model_design
This folder contains some notes on the genre-topic model, an extension of SCAN that leverages genre meta-data.

### src
This folder contains the main Go code for the semantic-change model and the results.

To move from the master branch to the branch where the genre topic model is, cd into the directory seed-semantic-change, then:

git branch
git checkout genre_topic_model

To go back to the master branch, type

git checkout master. 

To check whether you're in the master or other branch, type:

git branch

Depending on whether you're in the master or in a branch, the corresponding code will run.


Genre ids:

"Comedy" = 0
"Essays" = 1
"Letters" = 2
"Narrative" = 3
"Oratory" = 4
"Philosophy" = 5
"Poetry" = 6
"Religion" = 7
"Technical" = 8
"Tragedy" = 9
