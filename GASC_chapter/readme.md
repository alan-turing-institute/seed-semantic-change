# Code and data for chapter publication

This folder contains the code and data needed for the publication in the "Language variation" series of "Language Science Press".

## Input

gold_standard_binary_Latin.txt: list of changed and non-changed Latin words, from SemEval task 1 data, subtask 1.

## Latin_corpus

Processed LatinISE corpus, with added genre annotation by Alessandro Vatri. The genres are: Comedy, Essays, Law, Letters, Narrative, Oratory, Philosophy, Poetry, Christian, Technical, Tragedy.
The stopword list is this one: https://github.com/cltk/cltk/blob/master/cltk/stop/latin.py

All Christian writings (including letters and poems) have been assigned to the genre 'Christian'. This excludes philosophical but not strictly speaking theological/ecclesiological treatises composed by Christian writers. Collections spanning many centuries (anthologia latina, inscriptions etc) are assigned to a dummy century (100).

## Latin_SCAN_output

Output from SCAN models for Latin on two time periods.

## baseline_evaluation_output

Output of the baseline evaluation of SCAN on Latin data on two time points.

## Code

baseline_evaluation.py:

code for processing output files from GASC/SCAN; given a list of words, this calculates precision, recall and F1 score against the gold standard (0 for non-changed and 1 for changed).

baseline_evaluation_2.py:

Same as baseline_evaluation.py, but it also prints which (if any) sense has disappeared or appeared between the two time periods.


utils.py:

Has all the functions to preprocess data and train SGNS (AG and LA). TR training is more complicated and not currently in this repo.

main.py:

Script that launches functions in utils.py
