from utils import *


basedir = "/home/gntsh/git/seed-semantic-change/GASC_chapter/training_models/AG_BINARY/"
outdir = "/home/gntsh/git/TemporalReferencing/corpus/AG_BINARY_"
#if os.path.exists(outdir) == False:
#	os.mkdir(outdir)

for folder in os.listdir(basedir):
	if os.path.exists(outdir+folder) == False:
		os.mkdir(outdir+folder)
		os.mkdir(outdir+folder+"/files")

	with open(outdir+folder+"/files/corpus.txt","w") as f_out:
		for index, file in enumerate(sorted(os.listdir(os.path.join(basedir,folder)))):
			with open(os.path.join(basedir,folder,file)) as f:
				for line in f:
					f_out.write(str(index)+"\t"+line)
			
