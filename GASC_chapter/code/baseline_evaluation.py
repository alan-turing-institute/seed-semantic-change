## -*- coding: utf-8 -*-
# Author: Barbara McGillivray
# Date: 23/6/2020
# Python version: 3
# Script for processing output files from SCAN and GASC and reduce them to a binary change score for each word, for Latin and Ancient Greek


# Activate the virtual enviroment (this is important because that's where to install ruptures, which downgrades some Python packages including scipy and numpy!)
# source gasc_python/bin/activate
# Deactivate: deactivate

# ----------------------------
# Initialization
# ----------------------------


# Import modules:

import os
import csv
import datetime
import re
from collections import Counter
import locale
from pandas import read_excel
import numpy as np
import math
from statistics import mean
from scipy.stats import spearmanr
from os.path import dirname, realpath
import matplotlib.pyplot as plt
import ruptures as rpt
import numpy as np


now = datetime.datetime.now()
today_date = str(now)[:10]

# ---------------------------------------
# Initialization:
# ---------------------------------------


# Parameters:

#istest_default = "yes"
#istest = input("Is this a test? Leave empty for default (" + istest_default + ").")
number_test = 2 # number of annotators considered when testing
language = input("Which language are you interested in? Choose Latin or Greek.")
model = input("Which model are you interested in? Choose SCAN or GASC.")
word = input("Which lemma are you interested in? All lower-case letters.")

if language == "Latin":
    time_slices = [0, 1]
    number_senses = 4

#if istest == "":
#    istest = istest_default

# Directory and file names:

filepath = realpath(__file__)

dir_of_file = dirname(filepath)
parent_dir_of_file = dirname(dir_of_file)
parents_parent_dir_of_file = dirname(parent_dir_of_file)
dir_in = os.path.join(parent_dir_of_file, "input")
dir_out = os.path.join(parent_dir_of_file, "baseline_evaluation_output")
#dir_model_output = os.path.join(parents_parent_dir_of_file, "src", "dynamic-senses", language + "_input", model)
dir_model_output = os.path.join(parents_parent_dir_of_file, "GASC_chapter", language + "_" + model + "_output")

# Input files:
gold_standard_file_name = "gold_standard_binary_" + language + ".txt"
#model_output_file_name = "output_" + word + "_NOSTOPWORDS.dat"
if language == "Latin":
    model_output_file_name = word + ".dat"
else:
    if word == "kosmos":
        id = 59339
        dir_model_output = os.path.join(parents_parent_dir_of_file, "src", "dynamic-senses", "greek_input", "all_results", word + "_simon_k15", str(id))
        model_output_file_name = "output.dat"
    elif word == "harmonia":
        dir_model_output = os.path.join(parents_parent_dir_of_file, "src", "dynamic-senses", "greek_input",
                                        "all_results")
        model_output_file_name = "output_" + word + "_K5.dat"


# Output file:

binary_file_name = "binary_change_" + language + "_" + model + "_" + word + ".txt"

#if istest == "yes":
#    binary_file_name = binary_file_name.replace(".txt", "_test.txt")

output = open(os.path.join(dir_out, binary_file_name), 'w')

# ---------------------------------------
# Process gold standard files:
# ---------------------------------------

gold_standard = dict() # maps a lemma to 0 if it didn't change according to the gold standard, and to 1 if it changed.

gold_standard_file = open(os.path.join(dir_in, gold_standard_file_name), 'r', encoding="utf-8")

for line in gold_standard_file:
    fields = line.rstrip().split("\t")
    lemma = fields[0]
    binary_score = fields[1]
    gold_standard[lemma] = int(binary_score)
    #print("lemma=" + lemma + "end")
    #print("binary=" + binary_score + "end")

gold_standard_file.close()

if gold_standard[word] == 0:
    print("The word " + word + " did not change.")
else:
    print("The word " + word + " changed.")

# ---------------------------------------
# Process model files:
# ---------------------------------------


# Read model output files:

print("Opening model output file:" + model_output_file_name + " in " + str(dir_model_output))
model_output_file = open(os.path.join(dir_model_output, model_output_file_name), 'r', encoding="utf-8")

found_time_probabilities = 0
found_time_slices = 0

time2sense2probability = dict()  # maps a time slice and sense number to its probability predicted by the model

count = 0
for line in model_output_file:
    count += 1
    line_text = line.rstrip()
    print(str(count))

    #SCAN for Latin: use a test to identify statistically significant drops or peaks - Barbara

    if " per time " in line_text:
        found_time_probabilities = 1
        print("Found per time" + line_text)

    if line_text.startswith("Time"):
        found_time_slices += 1
        time_n = line_text.split("=")
        time_n = time_n[1]
        print("Found time" + line_text)

    if found_time_probabilities == 1 and found_time_slices > 0:
        #print(line_text)
        pattern0 = '^(0\.\d+?) {3}T=(\d+?),K=(\d+?):'
        if re.match(pattern0, line_text):
            match = re.search(pattern0, line_text)
            prob = match.group(1)
            time = match.group(2)
            sense = match.group(3)
            print("prob = " + str(prob))
            print("time = " + str(time))
            print("sense = " + str(sense))
            time2sense2probability[sense, time] = prob

    #if found_time_probabilities == 1:
        #if found_time_slices == 1:
            #print("Time:" + str(time_n))


model_output_file.close()

# For Greek: find changepoint in time series using ruptures
# C. Truong, L. Oudre, N. Vayatis. Selective review of offline change point detection methods. Signal Processing, 167:107299, 2020.

#algo = rpt.Pelt(model="rbf").fit(signal)
#result = algo.predict(pen=10)
# display
#rpt.display(signal, bkps, result)
#plt.show()




output.close()