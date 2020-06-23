# Code and data for chapter publication

This folder contains the code and data needed for the publication in the "Language variation" series of "Language Science Press".

## Input

gold_standard_binary_Latin.txt: list of changed and non-changed Latin words, from SemEval task 1 data, subtask 1.


## Code

baseline_evaluation.py:

code for processing output files from GASC/SCAN; given a list of words, this returns a binary score (0 for non-changed and 1 for changed).

