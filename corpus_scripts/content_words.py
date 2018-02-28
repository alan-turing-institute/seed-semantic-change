import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("python3 %s/asLemmata_oneFile.py id no_location TT no_work_id no_field no_wordlist" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/extract_context_words.py" % (os.path.dirname(os.path.realpath(__file__))))