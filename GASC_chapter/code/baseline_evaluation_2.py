## -*- coding: utf-8 -*-
# Authors: Barbara McGillivray, Valerio Perrone
# Date: 23/6/2020
# Python version: 3
# Script for processing output files from SCAN and GASC and reduce them to a binary change score for each word, for Latin and Ancient Greek


# Activate the virtual enviroment
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
import numpy as np
import sys


now = datetime.datetime.now()
today_date = str(now)[:10]

current_time_index = 0
current_genre = 0

true_positives = 0
false_negatives = 0
false_positives = 0
true_negatives = 0


def add_probabilities_to_dict(line_text, time, k, times):
    """For each time and sense, adds probability at each iteration to the dictionary time2sense2probabilities.
    This dictionary is useful at the end to compute probability means and standard deviations.

    Inputs:
    line_text: current line of text
    k: number of senses
    times: number of time points
    """

    starting_pattern = '{(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),'
    ending_pattern = ' (0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?)}'
    intermediate_pattern = '\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),'

    #print(line_text)
    if re.match(starting_pattern, line_text):
        time = 0
        #print('initial pattern')
        #print('time = {}'.format(time))
        match = re.match(starting_pattern, line_text)
        for i in range(k):
            sense_index = i + 1
            sense_prob = float(match.group(sense_index))
            if time not in time2sense2probabilities:
                time2sense2probabilities[time] = {sense_index: [sense_prob]}
            else:
                if sense_index not in time2sense2probabilities[time]:
                    time2sense2probabilities[time][sense_index] = [sense_prob]
                else:
                    time2sense2probabilities[time][sense_index].append(sense_prob)
    elif re.match(ending_pattern, line_text):
        time = times - 1
        #print('ending pattern')
        #print('time = {}'.format(time))
        match = re.match(ending_pattern, line_text)
        for i in range(k):
            sense_index = i + 1
            sense_prob = float(match.group(sense_index))
            if time not in time2sense2probabilities:
                time2sense2probabilities[time] = {sense_index: [sense_prob]}
            else:
                if sense_index not in time2sense2probabilities[time]:
                    time2sense2probabilities[time][sense_index] = [sense_prob]
                else:
                    time2sense2probabilities[time][sense_index].append(sense_prob)
    elif re.match(intermediate_pattern, line_text):
        time += 1
        #print('intermediate pattern')
        #print('time = {}'.format(time))
        match = re.match(intermediate_pattern, line_text)
        for i in range(k):
            sense_index = i + 1
            sense_prob = float(match.group(sense_index))
            if time not in time2sense2probabilities:
                time2sense2probabilities[time] = {sense_index: [sense_prob]}
            else:
                if sense_index not in time2sense2probabilities[time]:
                    time2sense2probabilities[time][sense_index] = [sense_prob]
                else:
                    time2sense2probabilities[time][sense_index].append(sense_prob)
    return time


def add_probabilities_to_dict_with_genre(line_text, time, genre, k, times):
    """For each time and sense, adds probability at each iteration to the dictionary time2sense2probabilities.
    This dictionary is useful at the end to compute probability means and standard deviations.

    Inputs:
    line_text: current line of text
    k: number of senses
    times: number of time points
    """

    starting_pattern = '{(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),'
    ending_pattern = ' (0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?)}'
    intermediate_pattern = '\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),\s+(0\.\d+?),'

    #print(line_text)
    #print('genre at the beginning:' + str(genre))
    if re.match(starting_pattern, line_text):
        time = 0
        #print('initial pattern')
        #print('time = {}'.format(time))
        match = re.match(starting_pattern, line_text)
        for i in range(k):
            sense_index = i + 1
            sense_prob = float(match.group(sense_index))
            if genre not in genre2time2sense2probabilities:
                genre2time2sense2probabilities[genre] = {time: {sense_index: [sense_prob]}}
            else:
                if time not in genre2time2sense2probabilities[genre]:
                    genre2time2sense2probabilities[genre][time] = {sense_index: [sense_prob]}
                else:
                    if sense_index not in genre2time2sense2probabilities[genre][time]:
                        genre2time2sense2probabilities[genre][time][sense_index] = [sense_prob]
                    else:
                        genre2time2sense2probabilities[genre][time][sense_index].append(sense_prob)
    elif re.match(ending_pattern, line_text):
        time = times - 1
        #print('ending pattern')
        #print('time = {}'.format(time))
        match = re.match(ending_pattern, line_text)
        for i in range(k):
            sense_index = i + 1
            sense_prob = float(match.group(sense_index))
            if genre not in genre2time2sense2probabilities:
                genre2time2sense2probabilities[genre] = {time: {sense_index: [sense_prob]}}
            else:
                if time not in genre2time2sense2probabilities[genre]:
                    genre2time2sense2probabilities[genre][time] = {sense_index: [sense_prob]}
                else:
                    if sense_index not in genre2time2sense2probabilities[genre][time]:
                        genre2time2sense2probabilities[genre][time][sense_index] = [sense_prob]
                    else:
                        genre2time2sense2probabilities[genre][time][sense_index].append(sense_prob)
        genre += 1
    elif re.match(intermediate_pattern, line_text):
        time += 1
        #print('intermediate pattern')
        #print('time = {}'.format(time))
        match = re.match(intermediate_pattern, line_text)
        for i in range(k):
            sense_index = i + 1
            sense_prob = float(match.group(sense_index))
            if genre not in genre2time2sense2probabilities:
                genre2time2sense2probabilities[genre] = {time: {sense_index: [sense_prob]}}
            else:
                if time not in genre2time2sense2probabilities[genre]:
                    genre2time2sense2probabilities[genre][time] = {sense_index: [sense_prob]}
                else:
                    if sense_index not in genre2time2sense2probabilities[genre][time]:
                        genre2time2sense2probabilities[genre][time][sense_index] = [sense_prob]
                    else:
                        genre2time2sense2probabilities[genre][time][sense_index].append(sense_prob)
    else:
        # print reset current_genre as we went through all genres
        genre = 0
    #print('genre at the end:' + str(genre))
    return time, genre


def print_means_and_stds(k, times):
    print('\nFor each time, mean and standard deviations of probability of each sense.')
    for time in range(times):
        print("time = " + str(time))
        for sense in range(k):
            print("sense = " + str(sense + 1))
            mean_prob = np.mean(time2sense2probabilities[time][sense + 1])
            std_prob = np.sqrt(np.var(time2sense2probabilities[time][sense + 1]))
            print("mean prob +- standard deviations: " + str(mean_prob) + " +- " + str(std_prob))


def detect_drops_and_peaks(k, times, num_stds):
    # num_stds is the number of standard deviations to use to assess significance
    # under Gaussian assumption:
    # 1 ---> 68% confidence interval
    # 2 ---> 95% confidence interval
    # 3 ---> 99.7% confidence interval
    print("\nConsecutive drops and peaks.")
    for sense in range(k):
        print("sense = " + str(sense + 1))
        for t in range(times - 1):
            print("from time {} to time {}".format(t, t + 1))
            mean_prob_0 = np.mean(time2sense2probabilities[t][sense + 1])
            std_prob_0 = np.sqrt(np.var(time2sense2probabilities[t][sense + 1]))
            mean_prob_1 = np.mean(time2sense2probabilities[t + 1][sense + 1])
            std_prob_1 = np.sqrt(np.var(time2sense2probabilities[t + 1][sense + 1]))
            if mean_prob_1 - mean_prob_0 > 0:
                significant = (mean_prob_1 - num_stds * std_prob_1) > (mean_prob_0 + num_stds * std_prob_0)
                print('Probability INcrease: {}; significant? {}'.format(mean_prob_1 - mean_prob_0, significant))
            else:
                significant = (mean_prob_1 + num_stds * std_prob_1) < (mean_prob_0 - num_stds * std_prob_0)
                print('Probability DEcrease: {}; significant? {}'.format(mean_prob_0 - mean_prob_1, significant))


def detect_overall_drops_and_peaks(k, times, num_stds):
    #print("\nDrops and peaks across entire time series.")
    increase_indicator = 0
    decrease_indicator = 0
    changed_sense = -1
    for sense in range(k):
        print("sense = " + str(sense + 1))
        min_prob = 2
        max_prob = -2
        std_min = 0
        std_max = 0
        time_min = 0
        time_max = 0
        for t in range(times):
            print("time = " + str(t))
            if np.mean(time2sense2probabilities[t][sense + 1]) < min_prob:
                min_prob = np.mean(time2sense2probabilities[t][sense + 1])
                std_min = np.sqrt(np.var(time2sense2probabilities[t][sense + 1]))
                time_min = t
            if np.mean(time2sense2probabilities[t][sense + 1]) > max_prob:
                max_prob = np.mean(time2sense2probabilities[t][sense + 1])
                std_max = np.sqrt(np.var(time2sense2probabilities[t][sense + 1]))
                time_max = t

        significant = (max_prob - num_stds * std_max) > (min_prob + num_stds * std_min)
        if time_min < time_max:
            #print("min probability at time {}, max at time {}".format(time_min, time_max))
            #print('Max global probability INcrease: {}; significant? {}'.format(max_prob - min_prob, significant))
            if significant:
                increase_indicator = True
                changed_sense = sense
        else:
            #print("min probability at time {}, max at time {}".format(time_min, time_max))
            #print('Max global probability DEcrease: {}; significant? {}'.format(max_prob - min_prob, significant))
            if significant:
                decrease_indicator = True
                changed_sense = sense

    print("===========Model Outcome===========")
    change_indicator = increase_indicator or decrease_indicator
    if change_indicator:
        print('The model detected a significant meaning change ({} std).'.format(num_stds))
        if increase_indicator:
            print('In particular, the model detected the significant rise of a new sense, sense K=' + str(changed_sense) +'.')
        elif decrease_indicator:
            print('In particular, the model detected the significant fall of an old sense, sense K=' + str(changed_sense) +'.')
    else:
        print('The model did NOT detect any significant meaning change ({} std).'.format(num_stds))
    return change_indicator, changed_sense


def detect_overall_drops_and_peaks_with_genre(k, times, genres, num_stds):
    #print("\nDrops and peaks across entire time series.")
    increase_indicator = 0
    decrease_indicator = 0
    changed_sense = -1
    for sense in range(k):
        print("sense = " + str(sense + 1))
        min_prob = 2
        max_prob = -2
        std_min = 0
        std_max = 0
        time_min = 0
        time_max = 0

        # for every sense, we check if there has been a significant change over time ACROSS ANY GENRE
        for genre in range(genres):
            for t in range(times):
                #print("time = " + str(t))
                if np.mean(genre2time2sense2probabilities[genre][t][sense + 1]) < min_prob:
                    min_prob = np.mean(genre2time2sense2probabilities[genre][t][sense + 1])
                    std_min = np.sqrt(np.var(genre2time2sense2probabilities[genre][t][sense + 1]))
                    time_min = t
                if np.mean(genre2time2sense2probabilities[genre][t][sense + 1]) > max_prob:
                    max_prob = np.mean(genre2time2sense2probabilities[genre][t][sense + 1])
                    std_max = np.sqrt(np.var(genre2time2sense2probabilities[genre][t][sense + 1]))
                    time_max = t

            significant = (max_prob - num_stds * std_max) > (min_prob + num_stds * std_min)
            if time_min < time_max:
                #print("min probability at time {}, max at time {}".format(time_min, time_max))
                #print('Max global probability INcrease: {}; significant? {}'.format(max_prob - min_prob, significant))
                if significant:
                    increase_indicator = True
                    changed_sense = sense
            else:
                #print("min probability at time {}, max at time {}".format(time_min, time_max))
                #print('Max global probability DEcrease: {}; significant? {}'.format(max_prob - min_prob, significant))
                if significant:
                    decrease_indicator = True
                    changed_sense = sense

    print("===========Model Outcome===========")
    change_indicator = increase_indicator or decrease_indicator
    if change_indicator:
        print('The model detected a significant meaning change ({} std).'.format(num_stds))
        if increase_indicator:
            print('In particular, the model detected the significant rise of a new sense, sense K=' + str(changed_sense) +'.')
        elif decrease_indicator:
            print('In particular, the model detected the significant fall of an old sense, sense K=' + str(changed_sense) +'.')
    else:
        print('The model did NOT detect any significant meaning change ({} std).'.format(num_stds))
    return change_indicator, changed_sense


# ---------------------------------------
# Initialization:
# ---------------------------------------


# Parameters:

#istest_default = "yes"
#istest = input("Is this a test? Leave empty for default (" + istest_default + ").")

language = input("Which language are you interested in? Choose Latin or Greek.")
model = input("Which model are you interested in? Choose SCAN or GASC.")
word = input("Which lemma are you interested in? All lower-case letters. "
             "Enter 'all' if you would like results for all target words.")
num_stds = input("What confidence interval would you like to use to declare semantic change? "
                 "1 = 68%, 2 = 95%, 3 = 99.7%. Enter either 1, 2 or 3.")

result_folder = ""
if model == "SCAN":
    if language == "Latin":
        result_folder = input("Which SCAN output would you like to use? Choose among SCAN_BCAC_OK, SCAN_BCAC_kappaF1000_OK, SCAN_dT1_minus2_OK, SCAN_dT3_minus2_OK. ")
    elif language == "Greek":
        result_folder = input("Which SCAN output would you like to use? Choose among SCAN_it1500, SCAN_it2500, SCAN_it10000. ")
    else:
        raise ValueError('Language {} not supported. Please choose either Latin or Greek'.format(language))
if model == "GASC":
    if language == "Latin":
        result_folder = input("Which GASC output would you like to use? Choose among GASC_BCAC_Christian, GASC_dT1_minus2_Christian, GASC_dT3_minus2_Christian. ")
    elif language == "Greek":
        result_folder = input(
            "Which GASC output would you like to use? Choose among GASC_it10000_Tech, GASC_it10000_Narr, GASC_it10000_Relig.")


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

dir_model_output = os.path.join(parents_parent_dir_of_file, "GASC_chapter", language + "_" + model + "_output", result_folder)

# Input files:
gold_standard_file_name = "gold_standard_binary_" + language + ".txt"
#model_output_file_name = "output_" + word + "_NOSTOPWORDS.dat"

# for both Latin and Greek
if word == 'all':
    all_files = [f
                 for f in os.listdir(dir_model_output)
                 if os.path.isfile(os.path.join(dir_model_output,f))
                 and f != '.DS_Store']
    all_files = [file for file in all_files if file != 'output.dat']
else:
    all_files = [word + ".dat"]
# deprecated
# else:
#     if word == "kosmos":
#         id = 59339
#         dir_model_output = os.path.join(parents_parent_dir_of_file, "src", "dynamic-senses", "greek_input", "all_results", word + "_simon_k15", str(id))
#         all_files = ["output.dat"]
#     elif word == "harmonia":
#         dir_model_output = os.path.join(parents_parent_dir_of_file, "src", "dynamic-senses", "greek_input",
#                                         "all_results")
#         all_files = ["output_" + word + "_K5.dat"]


# Output file:

binary_file_name = "binary_change_" + language + "_" + model + "_" + word + "_" + num_stds + "stds" + "_" + result_folder + ".txt"

#if istest == "yes":
#    binary_file_name = binary_file_name.replace(".txt", "_test.txt")

output = open(os.path.join(dir_out, binary_file_name), 'w')

# The following two lines redirect the output from the terminal to the output file
orig_stdout = sys.stdout
sys.stdout = output

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


# ---------------------------------------
# Process model files:
# ---------------------------------------


# Read model output files:

for model_output_file_name in all_files:

    print("model_output_file_name:" + model_output_file_name)
    print("\n========================================================")
    print("Opening model output file: " + model_output_file_name + " in " + str(dir_model_output))
    model_output_file = open(os.path.join(dir_model_output, model_output_file_name), 'r', encoding="utf-8")

    found_time_probabilities = 0
    found_time_slices = 0
    found_iterations = 0

    time2sense2probability = dict()  # maps a time slice and sense number to its probability predicted by the model
    time2sense2probabilities = dict()  # maps a time slice and sense number to the probability at each iteration
    genre2time2sense2probabilities = dict()  # maps a genre to a time slice and sense number to the probability at each iteration

    count = 0
    for line in model_output_file:
        count += 1
        line_text = line.rstrip()
        #print(str(count))

        if model == 'SCAN':
            # Use a test to identify statistically significant drops or peaks
            if 'kappaF' in line_text:
                # Extract the number of used senses K
                K = int(line_text.split(', K ')[1].split(', ')[0])
                print('There are K = {} senses in the output.'.format(K))
                times = int(line_text.split(', times ')[1].split(', ')[0])
                print('There are times = {} time points in the output.'.format(times))
                found_iterations = 1
            if found_iterations == 1:
                current_time_index = add_probabilities_to_dict(line_text, current_time_index, K, times)
        elif model == 'GASC':
            # this is temporarily hard coded. We should have the same output for SCAN and GASC
            #K = 4
            #times = 8
            if 'kappaF' in line_text:
                # Extract the number of used senses K
                K = int(line_text.split(', K ')[1].split(', ')[0])
                print('There are K = {} senses in the output.'.format(K))
                times = int(line_text.split(', times ')[1].split(', ')[0])
                print('There are times = {} time points in the output.'.format(times))
                found_iterations = 1
            if found_iterations == 1:
                current_time_index, current_genre = add_probabilities_to_dict_with_genre(line_text, current_time_index, current_genre, K, times)


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

    print("\n===========Ground Truth===========")
    if word != 'all':
        gold = gold_standard[word]
        if  gold == 0:
            print("The word " + word + " did not change.")
        else:
            print("The word " + word + " changed.")
    else:
        current_word = model_output_file_name.split('.')[0]
        gold = gold_standard[current_word]
        if  gold == 0:
            print("The word " + current_word + " did not change.")
        else:
            print("The word " + current_word + " changed.")

    if model == 'SCAN':
        # print_means_and_stds(K, times)
        # detect_drops_and_peaks(K, times, 2)
        result = detect_overall_drops_and_peaks(K, times, num_stds=int(num_stds))
    elif model == 'GASC':
        num_genres = 2  # TODO: hard-coded to two for now. To be generalized if needed.
        result = detect_overall_drops_and_peaks_with_genre(K, times, num_genres, num_stds=int(num_stds))

    change_detected = result[0]
    changed_sense = result[1]
    if change_detected == 1 and gold == 1:
        true_positives += 1
    elif change_detected == 0 and gold == 1:
        false_negatives += 1
    elif change_detected == 1 and gold == 0:
        false_positives += 1
    elif change_detected == 0 and gold == 0:
        true_negatives += 1


print("===========Precision, Recall and F1 score===========")
print('true_positives: {}'.format(true_positives))
print('true_negatives: {}'.format(true_negatives))
print('false_positives: {}'.format(false_positives))
print('false_negatives: {}'.format(false_negatives))
try:
    print('precision: {}'.format(true_positives / (true_positives + false_positives)))
    print('recall: {}'.format(true_positives / (true_positives + false_negatives)))
    print('F1 score: {}'.format(true_positives / (true_positives + 1/2 * (false_positives + false_negatives))))
except:
    print('Error in computing precision, recall or F1 score. Some denominator is 0.')

sys.stdout = orig_stdout
output.close()
print('Results saved to {}'.format(os.path.join(dir_out, binary_file_name)))
