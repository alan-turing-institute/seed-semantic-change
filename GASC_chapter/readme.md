# # Code and data for chapter publication

This folder contains the code and data needed for the publication in the "Language variation" series of "Language Science Press".

## Input

`gold_standard_binary_Latin.txt`: list of changed and non-changed Latin words, from SemEval task 1 data, subtask 1.

## Latin_corpus

Processed LatinISE corpus, with added genre annotation by Alessandro Vatri. The genres are: Comedy, Essays, Law, Letters, Narrative, Oratory, Philosophy, Poetry, Christian, Technical, Tragedy.
The stopword list is this one: https://github.com/cltk/cltk/blob/master/cltk/stop/latin.py

All Christian writings (including letters and poems) have been assigned to the genre 'Christian'. This excludes philosophical but not strictly speaking theological/ecclesiological treatises composed by Christian writers. Collections spanning many centuries (anthologia latina, inscriptions etc) are assigned to a dummy century (100).

## Latin_SCAN_output

Output from SCAN models for Latin on two time periods.

## baseline_evaluation_output

Output of the baseline evaluation of SCAN on Latin data on two time points.

## Code

`baseline_evaluation.py`:

code for processing output files from GASC/SCAN; given a list of words, this calculates precision, recall and F1 score against the gold standard (0 for non-changed and 1 for changed).

`baseline_evaluation_2.py`:

Same as baseline_evaluation.py, but it also prints which (if any) sense has disappeared or appeared between the two time periods.


`utils.py`:

Has all the functions to preprocess data and train SGNS (AG and LA). TR training is more complicated and not currently in this repo, we refer to https://github.com/Garrafao/TemporalReferencing. Note: some functions dealing with TR have a hardcoded path, but a find-and-replace (`/home/gntsh/git/TemporalReferencing/`) should be enough to adapt it to yours.

Functions are described in the file. `intersection_align_gensim` and `smart_procrustes_align_gensim` are updated versions of Ryan Heuser's gist: https://gist.github.com/quadrismegistus/09a93e219a6ffc4f216fb85235535faf

`main.py`:

Script that launches functions in utils.py. Modify as you wish depending on what you want to do.


`SGNS_align_eval_AG.py`:

Does the evaluation for SGNS (and TR) for Ancient Greek.


`SGNS_align_eval_AG_BINARY.py`:

Same as above, but for binary decisions. 


`SGNS_align_eval_LA.py`:

Does the evaluation for SGNS (and TR) for Latin.


`get_75quantile_threshold.Rscript`:

Is an R script that is run by the evaluation scripts above. It fits a gamma distribution.


pip install -r requirements.txt 
