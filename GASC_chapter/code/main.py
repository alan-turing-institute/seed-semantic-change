from utils import *
import sys

"""

"""
langs = ["AG", "LA"]
#langs = ["LA"]
#langs = ["AG"]

for lang in langs:
    print("Dealing with",lang)
    if lang == "AG":
        genres = ["narrative","technical"]
        # Creating data files
        #for genre in genres:
        #    print("Creating corpora for...",genre)
        #    corpus_transformer(genre,lang)

        # Training models
        genres_all = ["NOT-"+genre for genre in genres]
        for genre in genres:
            genres_all.append(genre)
        for genre in genres_all:
            earliest = -700
            last = 400
            slice_length = 100
            bins = []
            for i in range(earliest,last+slice_length,slice_length):
                bins.append(i)
            pool = Pool(8)
            pool.starmap(train_model,zip(bins,repeat(genre),repeat(lang)))
            pool.close()
            pool.join()

        """
        get_models_stats(lang)

        
        genres = ["narrative","technical"]
        
        for genre in genres_all:
            print(genre.upper())
            for target in target_words[lang].keys():
                if target == "mus":
                    check_target_in_models(target,genre,lang)
            print("\n")
        #"""

    if lang == "LA":
        bins = [1,2]
        genre = "NAIVE"
        for bin in bins:
            train_model(bin,genre,lang)


#LA_to_TR_input()
#AG_to_TR_input()
 
"""
directories = ["/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/narrative", 
            "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/NOT-narrative",
            "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/technical",
            "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/NOT-technical"]

for directory in directories:
#directory = "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/narrative"
    lang = "AG"
    print(directory,lang)
    list_models_for_alignment(directory,lang)


#list_models_for_alignment("/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/LA/NAIVE","LA")

"""
fit_to_gamma_get_changed_words("LA","NAIVE")

