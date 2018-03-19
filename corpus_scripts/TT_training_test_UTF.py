import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("python3 %s/TT_training_prepare_test_set_UTF.py" % (os.path.dirname(os.path.realpath(__file__))))
os.system("python3 %s/TT_training_tag_test_set_and_compare_UTF.py" % (os.path.dirname(os.path.realpath(__file__))))