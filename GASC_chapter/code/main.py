from utils import *

genres = ["narrative","technical"]

# Creating data files
for genre in genres:
    print("Creating corpora for...",genre)
    corpus_transformer(genre)

# Training models
genres = ["NOT-"+genre for genre in genres]
for genre in genres:
    earliest = -700
    last = 400
    slice_length = 100
    bins = []
    for i in range(earliest,last+slice_length,slice_length):
        bins.append(i)
    
    pool = Pool(8)
    pool.starmap(train_model,zip(bins,repeat(genre)))
    pool.close()
    pool.join()

get_models_stats()
for target in target_words.keys():
    check_target_in_models(target)
