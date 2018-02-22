import os
os.system("python3 %s/tokenizePerseus.py" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/tokenizeConverted.py" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/corporaParser.py" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/TT_format_our_data.py" % (os.path.dirname(os.path.realpath(__file__))))