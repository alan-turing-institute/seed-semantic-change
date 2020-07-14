Folders for evaluation and sense labelling (the ones with OK are those with the final list of stopwords removed):

- SCAN_BCAC_OK: probabilities for each iteration for 2 time points (before Christ - after Christ).
- SCAN_dT1_minus2_OK: probabilities for each iteration from -2 (3rd century BC) to 10 (10th century AC) with dT = 1.
- SCAN_dT3_minus2_OK: probabilities for each iteration from -2 (3rd century BC) to 21 (21st century AC) with dT = 3.

In addition:

- SCAN_BCAC_kappaF1000_OK: probabilities for each iteration for 2 time points (before Christ - after Christ) with parameter kappaF = 1000. The set of parameters here is the same as in SCAN_BCAC, but all the other outputs have kappaF = 100. You can decide whether to use this instead of SCAN_BCAC_OK (which instead has the same set of parameters as in the other results for Latin SCAN and GASC).


-------------------------------------------------------------------

OLD folders (to be put in the OLD folder; these contains some stopwords as "vel" and "quin"):

- SCAN_BCAC: it contains the output with probabilities for each iteration for 2 time points (before Christ - after Christ).
- SCAN_dT3: it contains the output with probabilities for each iteration from -3 to 21 with dT = 3.
- SCAN_dT1: it contains the output with probabilities for each iteration from -3 to 10 with dT = 1.
- SCAN_dT1_minus2: it contains the output with probabilities for each iteration from -2 (3rd century BC) to 10 (10th century AC) with dT = 1.
- SCAN_dT3_minus2: it contains the output with probabilities for each iteration from -2 (3rd century BC) to 21 (21st century AC) with dT = 3.
