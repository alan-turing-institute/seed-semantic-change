# Semantic change modelling from Ancient Greek texts

This code was created as part of the seed-funded project "Computational models of meaning change in natural language texts" (SF042) funded by The Alan Turing Institute, PI: Barbara McGillivray, project team: Dr Simon Hengchen, Dr Valerio Perrone, Prof Jim Smith, Dr Alessandro Vatri, and Mr Marco Palma.

## Folder description

### GASC chapter

This folder contains the code for the book chapter Perrone, V., Hengchen, S., Palma, M., Vatri, A., Smith, J. Q. and McGillivray, B. (forthcoming). In Nina Tahmasebi, Lars Borin, Adam Jatowt, Yang Xu, Simon Hengchen (eds). _Computational Approaches to Semantic Change._ Berlin: Language Science Press. Preprint: https://arxiv.org/pdf/2101.09069.pdf.

### Evaluation
This folder contains the Python3 code that runs the evalution of the model.

### Model_design
This folder contains some notes on the genre-topic model, an extension of SCAN that leverages genre meta-data.

### src
This folder contains the main Go code for the semantic-change model and the results.



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

Expert annotation for kosmos: https://github.com/alan-turing-institute/seed-semantic-change/blob/master/corpus_scripts_output/senses_59339_142.txt

Output of SCAN: 

On Ancient Greek: seed-semantic-change-master/src/dynamic-senses/greek_input/all_results/kosmos_simon_k15, etc.

On Latin: seed-semantic-change/src/dynamic-senses/latin_input/SCAN

Output of GASC: 

On Ancient Greek: seed-semantic-change-master/src/dynamic-senses/greek_input/all_results/genre_topic_output

On Latin:
