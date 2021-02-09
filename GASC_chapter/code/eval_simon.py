import sys
#genre = sys.argv[1]
import sklearn.metrics
import math

# change (1) / no-change (0)

LA_genres = ["SGNS-NOT-christian", "SGNS-NAIVE", "TR-NAIVE", "TR-NOT-christian"]
AG_genres = ["SGNS-NAIVE", "SGNS-NOT-narrative", "SGNS-narrative", "SGNS-NOT-technical", "SGNS-technical", "TR-NAIVE", "TR-NOT-narrative", "TR-narrative", "TR-NOT-technical", "TR-technical"]
#AG_genres = ["SGNS-technical"]

def eval_LA(changed,not_changed):

	gt = {}
	preds = {}
	with open("../input/gold_standard_binary_Latin.txt") as f:
		for line in f:
			s = line.rstrip().split("\t")
			gt[s[0]] = int(s[1])
	#print(gt)
	
	for w in gt:
		if w in changed:
			preds[w] = 1
		elif w in not_changed:
			preds[w] = 0
	#print(list(gt.values()))
	#print(list(preds.values()))
	#f = sklearn.metrics.precision_recall_fscore_support(list(gt.values()), list(preds.values()),average="macro")
	#for i in f:
	#print("Precision:",f[0])
	#print("Recall:",f[1])
	#print("F-Score:",f[2])
	#print(f,"\n")

	tp = 0
	fp = 0
	tn = 0
	fn = 0
	true_positives = []
	false_negatives = []
	for w in preds:
		if preds[w] == 1:
			if preds[w] == gt[w]:
				tp +=1
				true_positives.append(w)
			else:
				fp +=1
		elif preds[w] == 0:
			if preds[w] == gt[w]:
				tn += 1
			else:
				fn +=1
				false_negatives.append(w)
	print(tp,fp,tn,fn)
	print("TRUE POSITIVES",true_positives)
	print("FALSE NEGATIVES",false_negatives)
	
	try:
		P = tp/(tp+fp) 
		print("P = tp / (tp + fp)",P)
	except ZeroDivisionError:
		P = float("NaN")
		print("P = NaN")
	
	try:
		R =  tp / (tp + fn)
		print("R = tp / (tp + fn)",R)
	except ZeroDivisionError:
		R = float("NaN")
		print("R = NaN")
	
	if math.isnan(P) == False:
		if math.isnan(R) == False:
			F =  2 * (P * R) / (P + R)
			print("F",F)
		else:
			print("R is nan, no F")
	else:
		print("P is nan, no F")
	
	

def eval_AG(changed,not_changed):

	gt = {"κόσμος": "0", "ἁρμονία":"0", "μῦς":"0", "παράδεισος":"1", "παραβολή": "1"}
	preds = {}
	
	for w in gt:
		if w in changed:
			preds[w] = "1"
		elif w in not_changed:
			preds[w] = "0"
	
	f = sklearn.metrics.precision_recall_fscore_support(list(gt.values()), list(preds.values()),average="macro")

	print(f,"\n")

def eval_AG_BINARY(changed,not_changed):

	gt = {"κόσμος": 0, "ἁρμονία":0, "μῦς":0, "παράδεισος":1, "παραβολή": 1}
	#for k in gt:
	#	gt[k] = str(gt[k])
	
	
	preds = {}
	for w in gt:
		if w in changed:
			preds[w] = 1
		elif w in not_changed:
			preds[w] = 0
	print(preds)
	print(gt)
	#f = sklearn.metrics.precision_recall_fscore_support(list(gt.values()), list(preds.values()))
	#pr = sklearn.metrics.precision_recall_curve(list(gt.values()), list(preds.values()))
	#f = sklearn.metrics.f1_score(list(gt.values()), list(preds.values()))

	#print(pr)
	#print(pr[0][0], pr[1][0])
	#print(f,"\n")
	tp = 0
	fp = 0
	tn = 0
	fn = 0
	true_positives = []
	false_negatives = []
	for w in preds:
		if preds[w] == 1:
			if preds[w] == gt[w]:
				tp +=1
				true_positives.append(w)
			else:
				fp +=1
		elif preds[w] == 0:
			if preds[w] == gt[w]:
				tn += 1
			else:
				fn +=1
				false_negatives.append(w)
	print(tp,fp,tn,fn)
	print("TRUE POSITIVES",true_positives)
	print("FALSE NEGATIVES",false_negatives)
	try:
		P = tp/(tp+fp) 
		print("P = tp / (tp + fp)",P)
	except ZeroDivisionError:
		P = float("NaN")
		print("P = NaN")
	
	try:
		R =  tp / (tp + fn)
		print("R = tp / (tp + fn)",R)
	except ZeroDivisionError:
		R = float("NaN")
		print("R = NaN")
	
	if math.isnan(P) == False:
		if math.isnan(R) == False:
			F =  2 * (P * R) / (P + R)
			print("F",F)
		else:
			print("R is nan, no F")
	else:
		print("P is nan, no F")
	


"""
for genre in LA_genres:
	print(genre)
	if genre == "SGNS-NOT-christian":
		not_changed = ['acerbus', 'ancilla', 'civitas', 'cohors', 'consilium', 'consul', 'credo', 'dolus', 'dubius', 'dux', 'fidelis', 'honor', 'hostis', 'humanitas', 'itero', 'jus', 'licet', 'necessarius', 'nobilitas', 'oportet', 'poena', 'pontifex', 'potestas', 'regnum', 'salus', 'sapientia', 'senatus', 'sensus', 'simplex', 'templum', 'virtus', 'voluntas']
		changed =  ['adsumo', 'beatus', 'imperator', 'nepos', 'sacramentum', 'sanctus', 'scriptura', 'titulus']

	if genre == "SGNS-NAIVE":
		changed = ['adsumo', 'beatus', 'dolus', 'dux', 'humanitas', 'imperator', 'sacramentum', 'scriptura', 'simplex', 'titulus']
		not_changed = ['acerbus', 'ancilla', 'civitas', 'cohors', 'consilium', 'consul', 'credo', 'dubius', 'fidelis', 'honor', 'hostis', 'itero', 'jus', 'licet', 'necessarius', 'nepos', 'nobilitas', 'oportet', 'poena', 'pontifex', 'potestas', 'regnum', 'salus', 'sanctus', 'sapientia', 'senatus', 'sensus', 'templum', 'virtus', 'voluntas']

	if genre == "TR-NOT-christian":
		changed = ['beatus', 'civitas', 'fidelis', 'imperator', 'itero', 'pontifex', 'sacramentum', 'sanctus', 'simplex']
		not_changed = ['acerbus', 'adsumo', 'ancilla', 'cohors', 'consilium', 'consul', 'credo', 'dolus', 'dubius', 'dux', 'honor', 'hostis', 'humanitas', 'jus', 'licet', 'necessarius', 'nepos', 'nobilitas', 'oportet', 'poena', 'potestas', 'regnum', 'salus', 'sapientia', 'scriptura', 'senatus', 'sensus', 'templum', 'titulus', 'virtus', 'voluntas']

	eval_LA(changed,not_changed)
"""


for genre in AG_genres:
	print(genre)
	changed = []
	not_changed = []
	# ["SGNS-NAIVE", "SGNS-NOT-narrative", "SGNS-narrative", "SGNS-NOT-technical", "SGNS-technical"]
	
	if genre == "SGNS-NAIVE":
		changed =  ['μῦς', 'παραβολή', 'παράδεισος']
		not_changed =  ['ἁρμονία', 'κόσμος']
	
	if genre == "SGNS-NOT-narrative":
		changed =  ['μῦς', 'παραβολή', 'παράδεισος']
		not_changed =  ['ἁρμονία', 'κόσμος']

	if genre == "SGNS-narrative":
		changed =  ['ἁρμονία', 'παραβολή', 'παράδεισος']
		not_changed =  ['κόσμος', 'μῦς']

	if genre == "SGNS-NOT-technical":
		changed =  ['κόσμος', 'μῦς', 'παραβολή']
		not_changed =  ['ἁρμονία', 'παράδεισος']

	if genre == "SGNS-technical":
		changed =  ['ἁρμονία', 'κόσμος', 'μῦς', 'παράδεισος']
		not_changed =  ['παραβολή']
	
	if genre == "TR-NAIVE":
		changed = []
		not_changed = ['ἁρμονία', 'κόσμος', 'μῦς', 'παραβολή', 'παράδεισος']
	
	if genre == "TR-NOT-narrative":
		changed = []
		not_changed = ['ἁρμονία', 'κόσμος', 'μῦς', 'παραβολή', 'παράδεισος']

	if genre == "TR-narrative":
		changed = []
		not_changed = ['ἁρμονία', 'κόσμος', 'μῦς', 'παραβολή', 'παράδεισος']

	if genre == "TR-NOT-technical":
		changed = []
		not_changed = ['ἁρμονία', 'κόσμος', 'μῦς', 'παραβολή', 'παράδεισος']

	if genre == "TR-technical":
		changed = []
		not_changed = ['ἁρμονία', 'κόσμος', 'μῦς', 'παραβολή', 'παράδεισος']
	
	
	eval_AG_BINARY(changed,not_changed)


