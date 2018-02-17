# References:  www.dataquest.io ,
# http://stackoverflow.com/questions/15371691/python-sorted-sorting-a-dictionary-by-value-desc-then-by-key-asc
# http://stackoverflow.com/questions/30975339/slicing-a-python-ordereddict


# Importing all the libraries which are required for the computation
# We require numpy library for all the math computations. We require pandas library
# for all the data related computations and math library for maths computations

import os, sys
import numpy
import pandas as pd
import math

# Define all the required lists and dictionaries for computations
dictionary_words = []
final_dictionary = []
label_0s = []
label_1s = []
tree = []
top20 = {}

# Define the path from where to access the email files. The program takes in the files
# from both spam and non-spam folders in train directory
# path = "./part1/train/"
path = sys.argv[3]
dirs = os.listdir(path)

# Read in individual directory for spam and non spam and read in all the files. Split each and every word
# in the file and store it in a list. Since we need each occurance of the word, we do  set of those
# captured words and then convert back the same into the list. final_dictionary will have our
# final list of dictionary words
for dir_name in dirs:
    for f in os.listdir(os.path.join(path, dir_name)):
        document = os.path.join(path, dir_name, f)
        with open(document, 'r') as file:
            contents = file.read()
            indiv = contents.split(" ")
            dictionary_words = set(indiv)
            dictionary_words = list(set(dictionary_words))
            for word in dictionary_words:
                final_dictionary.append(word)

final_dictionary = list(set(dictionary_words))

# In order to capture top 20 words from the list of emails form which the split can be made
# is stored in the top20. The entropy calculation happens with these list of words and the split
# happens with the lowest entropy value. That is the highest information gain value
for dir_name in dirs:
    for f in os.listdir(os.path.join(path, dir_name)):
        document = os.path.join(path, dir_name, f)
        with open(document, 'r') as file:
            contents = file.read()
            indiv = contents.split(" ")
            dictionary_words = set(indiv)
            dictionary_words = list(set(dictionary_words))
            for word in dictionary_words:
                top20[word] = 1

top20 = sorted(top20, reverse=True)


# This function calculates the entropy for each word in the top20 dictionary and returns back the
# calculated entropy value. Based on which information gain is calculated. As we can see, Entropy is
# calculated using the probabilities and log probabilities
def calc_entropy(column):
    counts = numpy.bincount(column)
    probabilities = counts / len(column)
    entropy = 0
    for prob in probabilities:
        if prob > 0:
            entropy += prob * math.log(prob, 2)
            return -entropy


# Based on the calculated entropy, information gain is calculated. The higher the
# information gain, higher is the probability that the word gets split for that word
def calc_information_gain(data, split_name, target_name):
    original_entropy = calc_entropy(top20)
    column = data[split_name]
    median = column.median()
    left_split = data[column <= median]
    right_split = data[column > median]
    to_subtract = 0
    for subset in [left_split, right_split]:
        prob = (subset.shape[0] / data.shape[0])
        to_subtract += prob * calc_entropy(subset[target_name])
        return original_entropy - to_subtract
    
# This function finds out the best column to make the split on
def find_best_column(data, target_name, columns):
    information_gains = []
    for col in columns:
        information_gain = calc_information_gain(data, col, "top20")
        information_gains.append(information_gain)
        highest_gain_index = information_gains.index(max(information_gains))
        highest_gain = columns[highest_gain_index]
        return highest_gain

# The recursive id3 algorithm. Takes in the data and builds up the recursive tree
def id3(data, target, columns):
    unique_targets = pd.unique(data[target])
    if len(unique_targets) == 1:
        if 0 in unique_targets:
            label_0s.append(0)
        elif 1 in unique_targets:
            label_1s.append(1)
        return
    best_column = find_best_column(data, target, columns)
    column_median = data[best_column].median()
    tree["column"] = best_column
    tree["median"] = column_median
    left_split = data[data[best_column] <= column_median]
    right_split = data[data[best_column] > column_median]
    split_dict = [["left", left_split], ["right", right_split]]
    for name, split in split_dict:
        tree[name] = {}
        id3(split, target, columns, tree[name])

# The predict function which takes in the test set and predicts the class
# (spam or non spam) for a particular email
def predict(tree, row):
    if "label" in tree:
        return tree["label"]
        column = tree["column"]
        median = tree["median"]
        if row[column] <= median:
            return predict(tree["left"], row)
        else:
            return predict(tree["right"], row)


# The main function
if __name__ == "__main__":
    (mode, technique, directory_path, model_file) = sys.argv[1:5]
