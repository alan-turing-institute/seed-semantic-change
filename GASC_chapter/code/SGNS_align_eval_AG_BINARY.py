from utils import *
import sys

# change (1) / no-change (0)

targets = ["ἁρμονία", "κόσμος", "μῦς", "παραβολή", "παράδεισος"]

"""
# SGNS
basedir = "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG_BINARY/"

genres = ["NAIVE","narrative", "NOT-narrative", "technical", "NOT-technical"]
genre_target_bin_change = {}
#genres = ["NAIVE"]


for genre in genres:
	print(genre)

	if genre == "NAIVE":
		trained_models = {1: "BIN_1_NAIVE.w2v", 2: "BIN_2_NAIVE.w2v"}
	if genre == "NOT-narrative":
		trained_models = {1: "BIN_1_NOT-narrative.w2v", 2: "BIN_2_NOT-narrative.w2v"}
	if genre == "NOT-technical":
		trained_models = {1: "BIN_1_NOT-technical.w2v", 2: "BIN_2_NOT-technical.w2v"}
	if genre == "technical":
		trained_models = {1: "BIN_1_technical.w2v", 2: "BIN_2_technical.w2v"}
	if genre == "narrative":
		trained_models = {1: "BIN_1_narrative.w2v", 2: "BIN_2_narrative.w2v"}


	threshold = fit_to_gamma_get_changed_words("AG_BINARY",genre)
	print("Threshold is",threshold)

	m1 = gensim.models.KeyedVectors.load(basedir+"/"+genre+"/"+trained_models[1])
	m2 = gensim.models.KeyedVectors.load(basedir+"/"+genre+"/"+trained_models[2])

	changed = []
	not_changed = []
	for target in targets:
		cos = spatial.distance.cosine(m1.wv.get_vector(target),m2.wv.get_vector(target))
		if cos > threshold:
			#print(target,cos,threshold)
			changed.append(target)
		else:
			not_changed.append(target)
	
	print(genre)
	print("changed = ",changed)
	print("not_changed = ",not_changed)
	print("\n")
"""
# TR
basedir = "/home/gntsh/git/TemporalReferencing/matrices/"
random_words_AG = ['μέγας', 'ποιέω', 'καλέω', 'μόνος', 'ἔρχομαι', 'συνάγω', 'ὅμοιος', 'κύκλος', 'εἶδος', 'ὅσος', 'καταλιμπάνω', 'πάλιν', 'μένω', 'δείκνυμι', 'ἀίω', 'ἄγω', 'ἀνίστημι', 'γίγνομαι', 'τυγχάνω', 'πρότερος', 'λαμβάνω', 'δέομαι', 'πίπτω', 'δίδωμι', 'βαίνω', 'δέχομαι', 'δύναμαι', 'οἷος', 'ἀμφότερος', 'ἄκρος', 'ἔχω', 'ἕτερος', 'φέρω', 'ἵστημι', 'πολύς', 'λέγω', 'φημί']


for genre in ["NAIVE","narrative", "NOT-narrative", "technical", "NOT-technical"]:
    
	### load model here
	model = basedir + "AG_BINARY_" + genre + "/tr/vectors.w2v"
	print(model)
	m = gensim.models.KeyedVectors.load_word2vec_format(model)

	changed = []
	not_changed = []

	cosines = []
	args_R = ""
	for target in random_words_AG + targets:
		if target in targets:
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
	
	print(genre, "TR")
	print("changed =",changed)
	print("not_changed =",not_changed)
