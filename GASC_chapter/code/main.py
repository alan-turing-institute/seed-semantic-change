from utils import *
import sys



"""
langs = ["AG", "LA"]
#langs = ["LA"]
langs = ["AG"]

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
        genres_all = ["NAIVE"]
        #for genre in genres:
        #    genres_all.append(genre)
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

        
        #get_models_stats(lang)

        
        genres = ["narrative","technical"]
        
        for genre in genres_all:
            print(genre.upper())
            for target in target_words[lang].keys():
                if target == "mus":
                    check_target_in_models(target,genre,lang)
            print("\n")
        

    if lang == "LA":
        bins = [1,2]
        genre = "NAIVE"
        for bin in bins:
            train_model(bin,genre,lang)


#LA_to_TR_input()
#AG_to_TR_input()
 

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


fit_to_gamma_get_changed_words("LA","NAIVE")

#corpus_transformer("christian","LA")
#LA_to_TR_input("christian")
#LA_to_TR_input("NOT-christian")
#train_model("1","christian","LA")
#train_model("2","christian","LA")
#train_model("1","NOT-christian","LA")
#train_model("2","NOT-christian","LA")

#AG_to_TR_input("narrative")

list_models_for_alignment("/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/NAIVE","AG")

"""

lang = "AG"
genres = ["narrative","technical","NAIVE"]
#for genre in genres:
#    corpus_transformer_binary(genre,lang)

lang = "AG_BINARY"

#for bin in ["1", "2"]:
#    for genre in genres + ["NOT-narrative","NOT-technical"]:
#        train_model(bin,genre,lang)

#for directory in ["../trained_models/AG_BINARY/NOT-technical/", "../trained_models/AG_BINARY/technical/", "../trained_models/AG_BINARY/NOT-narrative/", "../trained_models/AG_BINARY/narrative/", "../trained_models/AG_BINARY/NAIVE/"]:
#    list_models_for_alignment(directory,lang)

fit_to_gamma_get_changed_words("AG_BINARY","NOT-narrative")