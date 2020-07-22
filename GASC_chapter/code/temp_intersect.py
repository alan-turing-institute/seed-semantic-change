import gensim
import os
import sys
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool
from itertools import repeat
import random
import numpy as np
import scipy.stats as stats
from scipy import spatial
import subprocess

# SGNS
basedir = "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/"

genres = ["narrative", "NOT-narrative", "technical", "NOT-technical"]
#genres = ["narrative"]
#vocab_genres = {}
setlist = []
for genre in tqdm(genres):
	#vocab_genres[genre] = {} 
	if genre == "narrative":
		trained_models = {2: "BIN_-500_narrative.w2v",
						3: "BIN_-400_narrative.w2v",
						4: "BIN_-300_narrative.w2v",
						6: "BIN_-100_narrative.w2v",
						7: "BIN_0_narrative.w2v",
						8: "BIN_100_narrative.w2v",
						9: "BIN_200_narrative.w2v",
						10: "BIN_300_narrative.w2v",	
			}
	if genre == "NOT-narrative":
		trained_models = {0: "BIN_-700_NOT-narrative.w2v",
						2: "BIN_-500_NOT-narrative.w2v",
						3: "BIN_-400_NOT-narrative.w2v",
						4: "BIN_-300_NOT-narrative.w2v",
						5: "BIN_-200_NOT-narrative.w2v",
						6: "BIN_-100_NOT-narrative.w2v",
						7: "BIN_0_NOT-narrative.w2v",
						8: "BIN_100_NOT-narrative.w2v",
						9: "BIN_200_NOT-narrative.w2v",
						10: "BIN_300_NOT-narrative.w2v",
						11: "BIN_400_NOT-narrative.w2v",	
			}

	if genre == "technical":
		trained_models = {2: "BIN_-500_technical.w2v",
						3: "BIN_-400_technical.w2v",
						4: "BIN_-300_technical.w2v",
						5: "BIN_-200_technical.w2v",
						6: "BIN_-100_technical.w2v",
						7: "BIN_0_technical.w2v",
						8: "BIN_100_technical.w2v",
						9: "BIN_200_technical.w2v",
						10: "BIN_300_technical.w2v",	
			}

	if genre == "NOT-technical":
		trained_models = {0: "BIN_-700_NOT-technical.w2v",
						2: "BIN_-500_NOT-technical.w2v",
						3: "BIN_-400_NOT-technical.w2v",
						4: "BIN_-300_NOT-technical.w2v",
						5: "BIN_-200_NOT-technical.w2v",
						6: "BIN_-100_NOT-technical.w2v",
						7: "BIN_0_NOT-technical.w2v",
						8: "BIN_100_NOT-technical.w2v",
						9: "BIN_200_NOT-technical.w2v",
						10: "BIN_300_NOT-technical.w2v",
						11: "BIN_400_NOT-technical.w2v"	
			}

	for bin in trained_models:
		m = gensim.models.KeyedVectors.load(basedir+genre+"/"+trained_models[bin])
		#vocab_genres[genre][bin] = [w for w in m.wv.vocab]
		setlist.append(set([w for w in m.wv.vocab])) 

#setlist = []# [vocab_genres[genre].values for genre in vocab_genres.keys()]
#for genre in genres:
#    for bin in trained_models[]

print(len(setlist))
final_vocab = set.intersection(*setlist)
print(len(final_vocab))
import random

#test = [final_vocab[index] for index in indices]
#print(test)
print(list(final_vocab))


