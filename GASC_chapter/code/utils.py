import gensim
import os
import sys
import pandas as pd
from multiprocessing import Pool
from itertools import repeat
import random
import numpy as np

path_data_in = os.path.join("..","..","corpus_scripts_output") # corpus_scripts_output/full_corpus_forms.txt
corpus_path = os.path.join(path_data_in,"full_corpus_forms.txt")
path_models_out = os.path.join("..","trained_models")
path_data_out = os.path.join("..","training_models")
path_evaluation_out = os.path.join("..","evaluation_out") 

paths = [path_data_out, path_evaluation_out, path_models_out]
for path in paths:
	if os.path.exists(path) == False:
		os.mkdir(path)

# "Comedy" = 0 "Essays" = 1 "Letters" = 2 "Narrative" = 3 "Oratory" = 4 "Philosophy" = 5 "Poetry" = 6 "Religion" = 7 "Technical" = 8 "Tragedy" = 9
genres_id = {0: "comedy", 
		1: "essays",
		2: "letters",
		3: "narrative",
		4: "oratory",
		5: "philosophy",
		6: "poetry",
		7: "religion",
		8: "technical",
		9: "tragedy"
		}

target_words = {'harmonia': ['!αρμονίας', 'ἁρμονία', 'ἁρμονίαι', 'ἁρμονίαις', 'ἁρμονίαισι', 'ἁρμονίαισιν', 'ἁρμονίαν', 'ἁρμονίας', 'ἁρμονίᾳ', 'ἁρμονίη', 'ἁρμονίηι', 'ἁρμονίην', 'ἁρμονίης', 'ἁρμονίῃ', 'ἁρμονίῃσιν', 'ἁρμονιάων', 'ἁρμονιῶν'], 'kosmos': ['κόσμε', 'κόσμοι', 'κόσμοιο', 'κόσμοις', 'κόσμοισι', 'κόσμον', 'κόσμος', 'κόσμου', 'κόσμους', 'κόσμω', 'κόσμωι', 'κόσμων', 'κόσμῳ'], 'mus': ['μύας', 'μύες', 'μύεσι', 'μύεσσιν', 'μύς', 'μύων', 'μῦ', 'μῦν', 'μῦς', 'μυί', 'μυός', 'μυοῖν', 'μυσί', 'μυσίν', 'μυῶν']}


def smart_procrustes_align_gensim(base_embed, other_embed, words=None):
	""" 
	Code by Ryan Heuser
	Procrustes align two gensim word2vec models (to allow for comparison between same word across models).
	Code ported from HistWords <https://github.com/williamleif/histwords> by William Hamilton <wleif@stanford.edu>.
		(With help from William. Thank you!)

	First, intersect the vocabularies (see `intersection_align_gensim` documentation).
	Then do the alignment on the other_embed model.
	Replace the other_embed model's syn0 and syn0norm numpy matrices with the aligned version.
	Return other_embed.

	If `words` is set, intersect the two models' vocabulary with the vocabulary in words (see `intersection_align_gensim` documentation).
	"""
	
	# patch by Richard So [https://twitter.com/richardjeanso) (thanks!) to update this code for new version of gensim
	base_embed.init_sims()
	other_embed.init_sims()

	# make sure vocabulary and indices are aligned
	in_base_embed, in_other_embed = intersection_align_gensim(base_embed, other_embed, words=words)

	# get the embedding matrices
	base_vecs = in_base_embed.syn0norm
	other_vecs = in_other_embed.syn0norm

	# just a matrix dot product with numpy
	m = other_vecs.T.dot(base_vecs) 
	# SVD method from numpy
	u, _, v = np.linalg.svd(m)
	# another matrix operation
	ortho = u.dot(v) 
	# Replace original array with modified one
	# i.e. multiplying the embedding matrix (syn0norm)by "ortho"
	other_embed.syn0norm = other_embed.syn0 = (other_embed.syn0norm).dot(ortho)
	return other_embed
	
def intersection_align_gensim(m1,m2, words=None):
	"""
	Intersect two gensim word2vec models, m1 and m2.
	Only the shared vocabulary between them is kept.
	If 'words' is set (as list or set), then the vocabulary is intersected with this list as well.
	Indices are re-organized from 0..N in order of descending frequency (=sum of counts from both m1 and m2).
	These indices correspond to the new syn0 and syn0norm objects in both gensim models:
		-- so that Row 0 of m1.syn0 will be for the same word as Row 0 of m2.syn0
		-- you can find the index of any word on the .index2word list: model.index2word.index(word) => 2
	The .vocab dictionary is also updated for each model, preserving the count but updating the index.
	"""

	# Get the vocab for each model
	vocab_m1 = set(m1.vocab.keys())
	vocab_m2 = set(m2.vocab.keys())

	# Find the common vocabulary
	common_vocab = vocab_m1&vocab_m2
	if words: common_vocab&=set(words)

	# If no alignment necessary because vocab is identical...
	if not vocab_m1-common_vocab and not vocab_m2-common_vocab:
		return (m1,m2)

	# Otherwise sort by frequency (summed for both)
	common_vocab = list(common_vocab)
	common_vocab.sort(key=lambda w: m1.vocab[w].count + m2.vocab[w].count,reverse=True)

	# Then for each model...
	for m in [m1,m2]:
		# Replace old syn0norm array with new one (with common vocab)
		indices = [m.vocab[w].index for w in common_vocab]
		old_arr = m.syn0norm
		new_arr = np.array([old_arr[index] for index in indices])
		m.syn0norm = m.syn0 = new_arr

		# Replace old vocab dictionary with new one (with common vocab)
		# and old index2word with new one
		m.index2word = common_vocab
		old_vocab = m.vocab
		new_vocab = {}
		for new_index,word in enumerate(common_vocab):
			old_vocab_obj=old_vocab[word]
			new_vocab[word] = gensim.models.word2vec.Vocab(index=new_index, count=old_vocab_obj.count)
		m.vocab = new_vocab

	return (m1,m2)


def train_model(slice,genre):
	"""
	Quite simply it trains models
	"""
	filename = "BIN_"+str(slice)+"_"+genre+".gensim"
	corpus_file = os.path.join(path_data_out,filename)
	model_file = os.path.join(path_models_out,filename.replace(".gensim",".w2v"))

	if os.stat(corpus_file).st_size < 10:
		return 
	if os.path.exists(model_file):
		return
	model = gensim.models.Word2Vec(corpus_file=corpus_file, min_count=10, sg=1 ,size=300, workers=3, seed=1830, iter=5)
	model.save(model_file)
	print("Trained",model_file,"\n")


def corpus_transformer(genre_sep,slice_length=100):
	"""
	Will transform the main corpus file into gensim files
	genre_sep is either 'technical', 'narrative', or None
	"""

	if genre_sep not in ["technical", "narrative",None]:
		sys.exit("genre_sep is",genre_sep,"not a valid value")
	
	
	print("Reading corpus at",corpus_path)

	corpus = pd.read_csv(corpus_path, sep='\t',names=["year","genre","sentence"])
	
	#print(corpus.head())

	ids_blacklist = []
	for key,val in genres_id.items():
		if val == genre_sep:
			id_OK = key
		else:
			ids_blacklist.append(key)
	
	years = list(corpus.year.unique())

	#sorted_df = corpus.sort_values(by="genre")
	#df_genre = df[corpus[""]

	earliest = sorted(years)[0]
	last = sorted(years)[-1]
	bins = []
	for i in range(earliest,last+slice_length,slice_length):
		bins.append(i)
	#print(bins)

	for bin in bins:
		fileout = os.path.join(path_data_out,"BIN_"+str(bin)+"_NOT-"+genres_id[id_OK]+".gensim")
		if os.path.exists(fileout) == False:
			sub_corpus = corpus[(corpus['year'] >= bin) & (corpus['year'] < bin + slice_length) & (corpus['genre'] != id_OK )]
			with open(fileout,"w") as f:
				for index, row in sub_corpus.iterrows():
					f.write(row["sentence"].lower()+"\n")
		
		fileout = os.path.join(path_data_out,"BIN_"+str(bin)+"_"+genres_id[id_OK]+".gensim")
		if os.path.exists(fileout) == False:
			sub_corpus = corpus[(corpus['year'] >= bin) & (corpus['year'] < bin + slice_length) & (corpus['genre'] == id_OK )]
			with open(fileout,"w") as f:
				for index, row in sub_corpus.iterrows():
					f.write(row["sentence"].lower()+"\n")

def get_models_stats():
	"""
	Loads all models and prints out some descriptive stats
	"""
	models = [os.path.join(path_models_out,model) for model in os.listdir(path_models_out)]
	for model in sorted(models):
		print(model)
		m = gensim.models.Word2Vec.load(model)
		vocab = len(m.wv.vocab)
		voc_list = list(m.wv.vocab.keys())
		print(vocab,"words in vocabulary")
		if vocab > 100:
			for i in range(0,5): # we try 5 pairs of words
				pair = random.sample(range(0,vocab), 2)
				print("cosine between",voc_list[pair[0]],voc_list[pair[1]],m.similarity(voc_list[pair[0]],voc_list[pair[1]]))
		

			
		else:
			print("model does not have more than 100 words in vocab")
		
		print("\n")

def check_target_in_models(target,genre):
	"""
	for target word we check if it exists in the model
	"genre" is narrative or technical, so not the "NOT" versions
	"""
	models = [os.path.join(path_models_out,model) for model in os.listdir(path_models_out) if genre in model]
	
	for model in sorted(models):
		#print(model)
		m = gensim.models.Word2Vec.load(model)
		present = False
		for form in target_words[target]:
			if form in m.wv.vocab:
				present = True
		if present == True:
			print(target,"is present in",model)
	