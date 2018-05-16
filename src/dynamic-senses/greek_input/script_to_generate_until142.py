import io
fichier = io.open("/Users/hengchen/git/seed-semantic-change/corpus_scripts_output/full_corpus_ids.txt","r")
count = 0
count_all = 0
resultat = io.open("full_corpus_ids_142.txt","w")
for line in fichier.readlines():
	count_all += 1
	split_ = line.split("\t")
	if int(split_[0]) < 143:
		resultat.write(line)
		count += 1

print("count",count)
print("count_all",count_all)