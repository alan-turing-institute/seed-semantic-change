from utils import *
import sys

# change (1) / no-change (0)

with open("../input/gold_standard_binary_Latin.txt") as f:
		targets = [line.split("\t")[0] for line in f]
""" 
# SGNS
basedir = "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/LA/"

### NAIVE
model_1 = basedir+"NAIVE/BIN_1_NAIVE.w2v"
model_2 = basedir+"NAIVE/BIN_2_NAIVE.w2v"

m1 = gensim.models.KeyedVectors.load(model_1)
m2 = gensim.models.KeyedVectors.load(model_2)
other_embed = smart_procrustes_align_gensim(m1, m2, targets)
other_embed.save(model_2)

threshold = fit_to_gamma_get_changed_words("LA","NAIVE")
print("Threshold is",threshold)

changed = []
not_changed = []
for target in targets:
    cos = spatial.distance.cosine(m1.wv.get_vector(target),other_embed.wv.get_vector(target))
    if cos > threshold:
        #print(target,cos,threshold)
        changed.append(target)
    else:
        not_changed.append(target)

print("changed",changed)
print("not_changed",not_changed)


### changed ['adsumo', 'beatus', 'dolus', 'dux', 'humanitas', 'imperator', 'sacramentum', 'scriptura', 'simplex', 'titulus']
### not_changed ['acerbus', 'ancilla', 'civitas', 'cohors', 'consilium', 'consul', 'credo', 'dubius', 'fidelis', 'honor', 'hostis', 'itero', 'jus', 'licet', 'necessarius', 'nepos', 'nobilitas', 'oportet', 'poena', 'pontifex', 'potestas', 'regnum', 'salus', 'sanctus', 'sapientia', 'senatus', 'sensus', 'templum', 'virtus', 'voluntas']


### NOT-CHRISTIAN
model_1 = basedir+"NOT-christian/BIN_1_NOT-christian.w2v"
model_2 = basedir+"NOT-christian/BIN_2_NOT-christian.w2v"

m1 = gensim.models.KeyedVectors.load(model_1)
m2 = gensim.models.KeyedVectors.load(model_2)
other_embed = smart_procrustes_align_gensim(m1, m2, targets)
other_embed.save(model_2)


threshold = fit_to_gamma_get_changed_words("LA","NOT-christian")
print("Threshold is",threshold)

changed = []
not_changed = []
for target in targets:
    cos = spatial.distance.cosine(m1.wv.get_vector(target),other_embed.wv.get_vector(target))
    if cos > threshold:
        #print(target,cos,threshold)
        changed.append(target)
    else:
        not_changed.append(target)

print("changed",changed)
print("not_changed",not_changed)


### changed ['adsumo', 'beatus', 'imperator', 'nepos', 'sacramentum', 'sanctus', 'scriptura', 'titulus']
### not_changed ['acerbus', 'ancilla', 'civitas', 'cohors', 'consilium', 'consul', 'credo', 'dolus', 'dubius', 'dux', 'fidelis', 'honor', 'hostis', 'humanitas', 'itero', 'jus', 'licet', 'necessarius', 'nobilitas', 'oportet', 'poena', 'pontifex', 'potestas', 'regnum', 'salus', 'sapientia', 'senatus', 'sensus', 'simplex', 'templum', 'virtus', 'voluntas']

"""
# TR
basedir = "/home/gntsh/git/TemporalReferencing/matrices/"

for genre in ["NAIVE","LA-NOT-christian"]:
    if genre == "NAIVE":
        model = basedir+"test/tr/vectors.w2v"
    else:
        model = basedir+"LA-NOT-christian/tr/vectors.w2v"

    m = gensim.models.KeyedVectors.load_word2vec_format(model)

    changed = []
    not_changed = []

    cosines = []
    args_R = ""
    for target in targets:
        cosines.append(m.distance(target+"_0",target+"_1"))
        args_R += str(m.distance(target+"_0",target+"_1"))+" "

    Routput = subprocess.check_output("Rscript get_75quantile_threshold.Rscript "+args_R, shell=True).decode()
    Routput = Routput.replace("\n","")
    threshold = float(Routput.split()[1])
    print("Threshold for bin:",threshold)
    for index, cosine in enumerate(cosines):
        if cosine > threshold:
            changed.append(targets[index])
        else:
            not_changed.append(targets[index])
    print("changed",changed)
    print("not_changed",not_changed)

    ## NAIVE
    ### changed ['beatus', 'civitas', 'fidelis', 'imperator', 'pontifex', 'sacramentum', 'sanctus', 'simplex']
    ### not_changed ['acerbus', 'adsumo', 'ancilla', 'cohors', 'consilium', 'consul', 'credo', 'dolus', 'dubius', 'dux', 'honor', 'hostis', 'humanitas', 'itero', 'jus', 'licet', 'necessarius', 'nepos', 'nobilitas', 'oportet', 'poena', 'potestas', 'regnum', 'salus', 'sapientia', 'scriptura', 'senatus', 'sensus', 'templum', 'titulus', 'virtus', 'voluntas']

    ## NOT-christian
    ### changed ['beatus', 'civitas', 'fidelis', 'imperator', 'itero', 'pontifex', 'sacramentum', 'sanctus', 'simplex']
    ### not_changed ['acerbus', 'adsumo', 'ancilla', 'cohors', 'consilium', 'consul', 'credo', 'dolus', 'dubius', 'dux', 'honor', 'hostis', 'humanitas', 'jus', 'licet', 'necessarius', 'nepos', 'nobilitas', 'oportet', 'poena', 'potestas', 'regnum', 'salus', 'sapientia', 'scriptura', 'senatus', 'sensus', 'templum', 'titulus', 'virtus', 'voluntas']