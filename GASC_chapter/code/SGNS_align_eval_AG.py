from utils import *
import sys

# change (1) / no-change (0)

targets = ["ἁρμονία", "κόσμος", "μῦς", "παραβολή", "παράδεισος"]

# SGNS
basedir = "/home/gntsh/git/seed-semantic-change/GASC_chapter/trained_models/AG/"

genres = ["narrative", "NOT-narrative", "technical", "NOT-technical", "NAIVE"]
genre_target_bin_change = {}
genres = ["NAIVE"]

for genre in genres:
	
	if genre == "NAIVE":
		trained_models = {0: "BIN_-700_NAIVE.w2v",
						2: "BIN_-500_NAIVE.w2v",
						3: "BIN_-400_NAIVE.w2v",
						4: "BIN_-300_NAIVE.w2v",
						5: "BIN_-200_NAIVE.w2v",
						6: "BIN_-100_NAIVE.w2v",
						7: "BIN_0_NAIVE.w2v",
						8: "BIN_100_NAIVE.w2v",
						9: "BIN_200_NAIVE.w2v",
						10: "BIN_300_NAIVE.w2v",
						11: "BIN_400_NAIVE.w2v",	
			}
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
	"""
    for i in range(0,12):
        if i in trained_models and i+1 in trained m
    m1 = gensim.models.KeyedVectors.load(model_1)
    m2 = gensim.models.KeyedVectors.load(model_2)
    #other_embed = smart_procrustes_align_gensim(m1, m2, targets)
    #other_embed.save(model_2)
    """
	
	threshold_path = basedir+genre+"/thresholds.tsv"
	if os.path.exists(threshold_path) == False:
		threshold_d = fit_to_gamma_get_changed_words("AG",genre)
		print(threshold_d)
		with open(basedir+genre+"/thresholds.tsv", "w") as f:
			for key in threshold_d.keys():
				f.write(str(key)+"\t"+str(threshold_d[key])+"\n")
	else:
		threshold_d = {}
		with open(basedir+genre+"/thresholds.tsv", "r") as f:
			for line in f:
				s = line.rstrip().split()
				threshold_d[int(s[0])] = float(s[1])
	

	print(genre)
	for bin in threshold_d:
		print(bin,threshold_d[bin])
	
	targets = ["ἁρμονία", "κόσμος", "μῦς", "παραβολή", "παράδεισος"]
	
	target_bin_change = {}
	for target in targets:
		target_bin_change[target] = {} 


	for i, bin in enumerate(list(threshold_d.keys())):
		changed = []
		not_changed = []
		#print("Looking at bin",bin,"index",i)
		try:
			m1 = gensim.models.KeyedVectors.load(basedir+genre+"/"+trained_models[bin])
			m2 = gensim.models.KeyedVectors.load(basedir+genre+"/"+trained_models[list(threshold_d.keys())[i+1]])
		except KeyError:
			#print("No models")
			print("")
		except IndexError:
			#print("Index")
			print("")

		for target in targets:
			try:
				cos = spatial.distance.cosine(m1.wv.get_vector(target),m2.wv.get_vector(target))
				if cos > threshold_d[bin]:
					changed.append(target)
					target_bin_change[target][bin] = "change"
				else:
					not_changed.append(target)
					target_bin_change[target][bin] = "no-change"
			except KeyError:
				continue
		print("changed",changed)
		print("not_changed",not_changed)

	genre_target_bin_change[genre] = target_bin_change
	decisions_path = basedir+genre+"/decisions.tsv"

	with open(decisions_path, "w") as f:
		for w in target_bin_change:
			for bin in target_bin_change[w]:
				f.write(w+"\t"+str(bin)+"\t"+target_bin_change[w][bin]+"\n")


# TR
basedir = "/home/gntsh/git/TemporalReferencing/matrices/"
random_words_AG = ['μέγας', 'ποιέω', 'καλέω', 'μόνος', 'ἔρχομαι', 'συνάγω', 'ὅμοιος', 'κύκλος', 'εἶδος', 'ὅσος', 'καταλιμπάνω', 'πάλιν', 'μένω', 'δείκνυμι', 'ἀίω', 'ἄγω', 'ἀνίστημι', 'γίγνομαι', 'τυγχάνω', 'πρότερος', 'λαμβάνω', 'δέομαι', 'πίπτω', 'δίδωμι', 'βαίνω', 'δέχομαι', 'δύναμαι', 'οἷος', 'ἀμφότερος', 'ἄκρος', 'ἔχω', 'ἕτερος', 'φέρω', 'ἵστημι', 'πολύς', 'λέγω', 'φημί']
genres = ["narrative", "NOT-narrative", "technical", "NOT-technical", "NAIVE"]

earliest = -700 #sorted(years)[0]
last = 400 #sorted(years)[-1]
slice_length = 100
bins = []

for i in range(earliest,last+slice_length,slice_length):
	if i != "-600":
		bins.append(i)

random_words_AG_targets = random_words_AG + targets

for genre in genres:
	if genre == "NAIVE":
			model = basedir+"AG/tr/vectors.w2v"
	else:
		model = basedir+"AG_"+genre+"/tr/vectors.w2v"

	m = gensim.models.KeyedVectors.load_word2vec_format(model)
	
	for index, bin in enumerate(bins):
		cosines = {}
		args_R = ""
		x_cos = 0
		for target in random_words_AG_targets:
			try:
				if target in targets:
					cosines[target] = m.distance(target+"_"+str(bin),target+"_"+str(bins[index+1]))
				#print(target+"_"+str(bin))
				#print(target+"_"+str(bins[index+1]))
				args_R += str(m.wv.distance(target+"_"+str(bin),target+"_"+str(bins[index+1])))+" "
				x_cos += 1
			except KeyError:
				#print(target+"_"+str(bin))
				continue
			except IndexError:
				print("Index")
		#print(args_R)

		if x_cos > 2:
			Routput = subprocess.check_output("Rscript get_75quantile_threshold.Rscript "+args_R, shell=True).decode()
			Routput = Routput.replace("\n","")
			threshold = float(Routput.split()[1])
			print("Threshold for bin",bin,threshold)
			changed = []
			not_changed = []
			for key in cosines:
				if cosines[key] > threshold:
					changed.append(key)
				else:
					not_changed.append(key)
			print("changed",changed)
			print("not_changed",not_changed)

		
