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
genres_id = {}
genres_id["AG"] = {0: "comedy", 
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
genres_id["LA"] = {0: "comedy", 
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
genre_stats = {"AG":["technical","NOT-technical","narrative","NOT-narrative"],
			"LA":[] }

target_words = {}
target_words["AG"] = {'harmonia': ['!αρμονίας', 'ἁρμονία', 'ἁρμονίαι', 'ἁρμονίαις', 'ἁρμονίαισι', 'ἁρμονίαισιν', 'ἁρμονίαν', 'ἁρμονίας', 'ἁρμονίᾳ', 'ἁρμονίη', 'ἁρμονίηι', 'ἁρμονίην', 'ἁρμονίης', 'ἁρμονίῃ', 'ἁρμονίῃσιν', 'ἁρμονιάων', 'ἁρμονιῶν'], 
					'kosmos': ['κόσμε', 'κόσμοι', 'κόσμοιο', 'κόσμοις', 'κόσμοισι', 'κόσμον', 'κόσμος', 'κόσμου', 'κόσμους', 'κόσμω', 'κόσμωι', 'κόσμων', 'κόσμῳ'], 
					'mus': ['μύας', 'μύες', 'μύεσι', 'μύεσσιν', 'μύς', 'μύς' 'μύων', 'μῦ', 'μῦν', 'μῦς', 'μυί', 'μυός', 'μυοῖν', 'μυσί', 'μυσίν', 'μυῶν'],
					'parabole': ['παραβολή'],
					'paradeisos': ['παράδεισος'],
					}
target_words["LA"] = {}

import cProfile, pstats, io
def profile(fnc):

	"""A decorator that uses cProfile to profile a function"""

	def inner(*args, **kwargs):

		pr = cProfile.Profile()
		pr.enable()
		retval = fnc(*args, **kwargs)
		pr.disable()
		s = io.StringIO()
		sortby = 'cumulative'
		ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
		ps.print_stats()
		print(s.getvalue())
		return retval

	return inner



#@profile
def list_models_for_alignment(directory,lang):
	"""
	This will list models for a folder,
	select the latest,
	align latest-1 with it;
	align latest -2 with latest-1, etc
	"""
	
	if lang == "AG":
		targets = ["ἁρμονία", "κόσμος", "μῦς", "παραβολή", "παράδεισος"]
		models = [model for model in os.listdir(directory) if model.endswith(".w2v")]
		earliest = -700 #sorted(years)[0]
		last = 400 #sorted(years)[-1]
		slice_length = 100
		bins = []
		models_ordered = [] ## negative ints as strings don't play nice with sorted()
		"""
		for i in range(earliest,last+slice_length,slice_length):
			for model in models:
				if "BIN_"+str(i) in model:
					models_ordered.append(os.path.join(directory,model))
		"""
		#print(directory)
		#print(models)
		for model in models:
			#print(model)
			m = gensim.models.KeyedVectors.load(os.path.join(directory,model))
			x = 0
			for target in targets:
				if target in m.wv.vocab:

					x += 1
					if x == len(targets):
						print("model chosen for alignment",model)
						break

		models_ordered = [os.path.join(directory,model)]
		for model in sorted(models,reverse=True):
			if os.path.join(directory,model) not in models_ordered:
				models_ordered.append(os.path.join(directory,model))


		#print(models_ordered)
		#models_ordered.reverse()
		#print(models_ordered)
	
		print(len(models_ordered))
		#print(len(models_ordered))
		for index, item in enumerate(models_ordered):
			#print("index",index)
			try:
				#print("Aligning",item,"and",models_ordered[index+1])
				m1 = gensim.models.KeyedVectors.load(item)
				m2 = gensim.models.KeyedVectors.load(models_ordered[index+1])

				#print(m1)
				#print(m2)
				print(item,models_ordered[index+1])
				other_embed = smart_procrustes_align_gensim(m1, m2, targets)
				#other_embed = smart_procrustes_align_gensim(item, models_ordered[index+1])
				#print("other_embed retrieved")

				other_embed.save(models_ordered[index+1])
				#print("Save aligned model at",models_ordered[index+1])
			
			except IndexError:
				#print("index",index,"error")
				#return
				#continue
				if index == len(models_ordered)-1:
					return
	
	if lang == "LA":
		with open("../input/gold_standard_binary_Latin.txt") as f:
			targets = [line.split("\t")[0] for line in f]
		models = [os.path.join(directory,model) for model in os.listdir(directory) if model.endswith(".w2v")]
		print(models)
		m1 = gensim.models.KeyedVectors.load(models[0])
		m2 = gensim.models.KeyedVectors.load(models[1])
		other_embed = smart_procrustes_align_gensim(m1, m2, targets)
		other_embed.save(models[1])


def fit_to_gamma_get_changed_words(lang,genre):
	"""
	Calculates quantile threshold (change/no-change) 
	based on the implementation of TemporalTeller at SemEval-2020 Task 1: Unsupervised Lexical Semantic
	Change Detection with Temporal Reference
	Jinan Zhou, Jiaxin Li

	Takes a language and a genre as input
	"""

	dict_target_bins_vectors = target_words_to_CD_arrays_SGNS(lang,genre)
	
	words = list(dict_target_bins_vectors.keys())
	print(words)
	w_cosD = []
	
	#if lang == "LA": ## let's start with an easy binary case
	#	bins = [1,2]

		
	for w in tqdm(words):
		#print(w)
		vecs = list(dict_target_bins_vectors[w].values()) ## list of all vectors for this word
		#print("vectors for",w,vecs)
		cosD = [] ## list of all distances
		if w == "μῦς":
			print(w)
		for index, vec in enumerate(vecs):
			#print(w, index, vec)
				
			try:
				cos = spatial.distance.cosine(vec,vecs[index+1])
				#print(w,cos)
			except TypeError:
			#	print("typeerror")
				cos = None
			except IndexError:
				continue
			cosD.append(cos)
		
		w_cosD.append(cosD)
	
	for index, w in enumerate(words):
		print(w,len(w_cosD[index]),w_cosD[index])
	

	for bin in bins:
		bin_cosines = []
		for w in words:
			bin_cosines.append(w_cosD[w][bin])
		threshold = float(os.system("Rscript get_75quantile_threshold.Rscript "+bin_cosines))

		print("bin",bin,"threshold",threshold)

	# 2. for every index, get the value for all words
	# 3. feed that to Rscript

	#

	#print(words)
	#print(w_cosD)


	

def target_words_to_CD_arrays_SGNS(lang,genre):
	if lang == "AG":
		bins = [i for i in range(0,12)]
		
		targets = ["ἁρμονία", "κόσμος", "μῦς", "παραβολή", "παράδεισος"]
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

	if lang == "LA":
		bins = [1,2]
		with open("../input/gold_standard_binary_Latin.txt") as f:
			targets = [line.split("\t")[0] for line in f]

		if genre == "NAIVE":
			trained_models = {1: "BIN_1_NAIVE.w2v", 2: "BIN_2_NAIVE.w2v"}
	
	
	directory = "../trained_models/"+lang+"/"+genre+"/"

	dict_target_bins_vectors = {}
	
	#print("We have these bins:",bins)
	print("Getting vectors")
	for target in tqdm(targets):  ## take the vector from each time slice, THEN do cos
		if target == "μῦς":
			print(target)
		first = True
		dict_target_bins_vectors[target] = {}
		for bin in bins:
			#print(bin)
			if bin in trained_models.keys(): ## if we have a model for this period
				if target == "μῦς":
					print(directory+trained_models[bin])
				m1 = gensim.models.Word2Vec.load(directory+trained_models[bin])
				try:
					vec = m1.wv.get_vector(target)
					if target == "μῦς":
						print(bin,"has a vec")
					first = False
				except KeyError:
					if first == True:
						vec = None
					
				
			else:
				if first == True:
					vec = None

			dict_target_bins_vectors[target][bin] = vec

	return dict_target_bins_vectors  ## returns a dictionary that has target words as keys and then bins and then vectors


		

	



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
	
	#path_out = other_embed
	#base_embed = gensim.models.Word2Vec.load(base_embed)
	#other_embed = gensim.models.Word2Vec.load(other_embed)
	#print(type(base_embed))
	#print("models loaded")

	base_embed.init_sims()
	other_embed.init_sims()
	#print("init simmed")
	
	# make sure vocabulary and indices are aligned
	in_base_embed, in_other_embed = intersection_align_gensim(base_embed, other_embed, words)
	#print("vocab intersected")
	
	# get the embedding matrices
	base_vecs = in_base_embed.wv.syn0norm
	other_vecs = in_other_embed.wv.syn0norm
	


	# just a matrix dot product with numpy
	m = other_vecs.T.dot(base_vecs) 
	try:
		
		# SVD method from numpy
		u, _, v = np.linalg.svd(m)
	except np.linalg.LinAlgError:
		return other_embed

	# another matrix operation
	ortho = u.dot(v) 
	# Replace original array with modified one
	# i.e. multiplying the embedding matrix (syn0norm)by "ortho"
	other_embed.wv.syn0norm = other_embed.wv.syn0 = (other_embed.wv.syn0norm).dot(ortho)
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
	vocab_m1 = set(m1.wv.vocab.keys())
	vocab_m2 = set(m2.wv.vocab.keys())
	print("vocabs created")

	# Find the common vocabulary
	common_vocab = vocab_m1&vocab_m2
	if words: common_vocab&=set(words)

	# If no alignment necessary because vocab is identical...
	if not vocab_m1-common_vocab and not vocab_m2-common_vocab:
		print("No need for alignment")
		return (m1,m2)
		

	# Otherwise sort by frequency (summed for both)
	common_vocab = list(common_vocab)
	common_vocab.sort(key=lambda w: m1.wv.vocab[w].count + m2.wv.vocab[w].count,reverse=True)
	#print("Len common vocab",len(common_vocab))
	#print("Vocab in common sorted")

	# Then for each model...
	for m in [m1,m2]:
		
		# Replace old syn0norm array with new one (with common vocab)
		indices = [m.wv.vocab[w].index for w in common_vocab]
		
		old_arr = m.wv.syn0norm
		new_arr = np.array([old_arr[index] for index in indices])
		m.wv.syn0norm = m.wv.syn0 = new_arr


		# Replace old vocab dictionary with new one (with common vocab)
		# and old index2word with new one
		m.wv.index2word = common_vocab
		old_vocab = m.wv.vocab
		new_vocab = {}
		for new_index,word in enumerate(common_vocab):
			old_vocab_obj=old_vocab[word]
			new_vocab[word] = gensim.models.word2vec.Vocab(index=new_index, count=old_vocab_obj.count)
		m.wv.vocab = new_vocab
	

	return (m1,m2)

def LA_to_TR_input():
	lang = "LA"
	files = [os.path.join(path_data_out,lang,file) for file in os.listdir(os.path.join(path_data_out,lang)) if file.endswith(".gensim")]
	with open("/home/gntsh/git/TemporalReferencing/corpus/test/files/corpus.txt", "w") as f_out:
		for index, file in enumerate(sorted(files)):
			with open(file) as f:
				for line in f.readlines():
					f_out.write(str(index)+"\t"+line.lower())
	os.system("gzip -f "+"/home/gntsh/git/TemporalReferencing/corpus/test/files/corpus.txt")

def AG_to_TR_input():
	lang = "AG"
	corpus = pd.read_csv(corpus_path, sep='\t',names=["year","genre","sentence"])

	years = list(corpus.year.unique())

		#sorted_df = corpus.sort_values(by="genre")
		#df_genre = df[corpus[""]

	earliest = -700 #sorted(years)[0]
	last = 400 #sorted(years)[-1]
	slice_length = 100
	bins = []
	for i in range(earliest,last+slice_length,slice_length):
		bins.append(i)

	with open("/home/gntsh/git/TemporalReferencing/corpus/AG/files/corpus.txt", "w") as f:
		for bin in bins:
			sub_corpus = corpus[(corpus['year'] >= bin) & (corpus['year'] < bin + slice_length)]
			
			for index, row in sub_corpus.iterrows():
				f.write(str(bin)+"\t"+row["sentence"].lower()+"\n")

		
	os.system("gzip -f "+"/home/gntsh/git/TemporalReferencing/corpus/AG/files/corpus.txt")
	

def train_model(slice,genre,lang):
	"""
	Quite simply it trains models
	"""
	if lang == "AG":
		filename = "BIN_"+str(slice)+"_"+genre+".gensim"
		corpus_file = os.path.join(path_data_out,lang,filename)
		model_file = os.path.join(path_models_out,lang,genre,filename.replace(".gensim",".w2v"))
		if os.path.exists(os.path.join(path_models_out,lang,genre)) == False:
			try:
				os.mkdir(os.path.join(path_models_out,lang,genre))
			except FileExistsError:
				pass

		if os.stat(corpus_file).st_size < 10:
			return 
		if os.path.exists(model_file):
			return
		model = gensim.models.Word2Vec(corpus_file=corpus_file, min_count=1, sg=1 ,size=300, workers=3, seed=1830, iter=5)
		model.save(model_file)
		print("Trained",model_file,"\n")
	
	
	#TODO: transform input data as GENRE input data
	if lang == "LA":
		
		filename = "BIN_"+str(slice)+"_"+genre+".gensim"
		corpus_file = os.path.join(path_data_out,lang,genre,filename)
		model_file = os.path.join(path_models_out,lang,genre,filename.replace(".gensim",".w2v"))
		
		if os.path.exists(os.path.join(path_models_out,lang,genre)) == False:
			os.mkdir(os.path.join(path_models_out,lang,genre))

		try:
			if os.stat(corpus_file).st_size < 10:
				return 
		except FileNotFoundError:
			pass

		if os.path.exists(model_file):
			return

		model = gensim.models.Word2Vec(corpus_file=corpus_file, min_count=1, sg=1 ,size=300, workers=3, seed=1830, iter=5)
		model.save(model_file)
		print("Trained",model_file,"\n")
	

def corpus_transformer(genre_sep,lang,slice_length=100):
	"""
	Will transform the main corpus file into gensim files
	genre_sep is either 'technical', 'narrative', or None
	"""
	if lang == "AG":
		if genre_sep not in ["technical", "narrative",None]:
			sys.exit("genre_sep is",genre_sep,"not a valid value")
		
		
		print("Reading corpus at",corpus_path)

		corpus = pd.read_csv(corpus_path, sep='\t',names=["year","genre","sentence"])
		
		#print(corpus.head())

		ids_blacklist = []
		for key,val in genres_id[lang].items():
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
			fileout = os.path.join(path_data_out,lang,"BIN_"+str(bin)+"_NOT-"+genres_id[lang][id_OK]+".gensim")
			if os.path.exists(fileout) == False:
				sub_corpus = corpus[(corpus['year'] >= bin) & (corpus['year'] < bin + slice_length) & (corpus['genre'] != id_OK )]
				with open(fileout,"w") as f:
					for index, row in sub_corpus.iterrows():
						f.write(row["sentence"].lower()+"\n")
			
			fileout = os.path.join(path_data_out,lang,"BIN_"+str(bin)+"_"+genres_id[lang][id_OK]+".gensim")
			if os.path.exists(fileout) == False:
				sub_corpus = corpus[(corpus['year'] >= bin) & (corpus['year'] < bin + slice_length) & (corpus['genre'] == id_OK )]
				with open(fileout,"w") as f:
					for index, row in sub_corpus.iterrows():
						f.write(row["sentence"].lower()+"\n")

def get_models_stats(lang):
	"""
	Loads all models and prints out some descriptive stats
	"""
	for genre_stat in genre_stats[lang]:

		models = [os.path.join(path_models_out,lang,genre_stat,model) for model in os.listdir(os.path.join(path_models_out,lang,genre_stat))]
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

def check_target_in_models(target,genre,lang):
	"""
	for target word we check if it exists in the model
	"genre" is narrative or technical, so not the "NOT" versions
	"""
	
	models = [os.path.join(path_models_out,lang,genre,model) for model in os.listdir(os.path.join(path_models_out,lang,genre)) if genre in model]
	
	for model in sorted(models):
		#print(model)
		m = gensim.models.Word2Vec.load(model)
		present = False
		for form in target_words[lang][target]:
			if form in m.wv.vocab:
				print(form)
				present = True
		if present == True:
			print(target,"is present in",model)
	
	#μῦς