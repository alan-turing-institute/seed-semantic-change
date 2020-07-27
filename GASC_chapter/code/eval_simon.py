import sys
#genre = sys.argv[1]
import sklearn.metrics

# change (1) / no-change (0)

LA_genres = ["SGNS-NOT-christian", "SGNS-NAIVE", "TR-NAIVE", "TR-NOT-christian"]
AG_genres = ["SGNS-NAIVE", "SGNS-NOT-narrative", "SGNS-narrative", "SGNS-NOT-technical", "SGNS-technical", "TR-NAIVE", "TR-NOT-narrative", "TR-narrative", "TR-NOT-technical", "TR-technical"]

def eval_LA(changed,not_changed):

	gt = {}
	preds = {}
	with open("../input/gold_standard_binary_Latin.txt") as f:
		for line in f:
			s = line.rstrip().split("\t")
			gt[s[0]] = s[1]
	#print(gt)
	
	for w in gt:
		if w in changed:
			preds[w] = "1"
		elif w in not_changed:
			preds[w] = "0"
	#print(list(gt.values()))
	#print(list(preds.values()))
	f = sklearn.metrics.precision_recall_fscore_support(list(gt.values()), list(preds.values()),average="macro")
	#for i in f:
	#print("Precision:",f[0])
	#print("Recall:",f[1])
	#print("F-Score:",f[2])
	print(f,"\n")
	

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

	gt = {"κόσμος": "0", "ἁρμονία":"0", "μῦς":"0", "παράδεισος":"1", "παραβολή": "1"}
	preds = {}
	
	for w in gt:
		if w in changed:
			preds[w] = "1"
		elif w in not_changed:
			preds[w] = "0"
	print(preds)
	print(gt)
	f = sklearn.metrics.precision_recall_fscore_support(list(gt.values()), list(preds.values()),average="macro")

	print(f,"\n")


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


