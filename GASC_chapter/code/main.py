from utils import *

genres = ["narrative","technical"]
for genre in genres:
    print("Creating corpora for...",genre)
    corpus_transformer(genre)