from __future__ import division
from decimal import Decimal

import math
import re,string
import collections
import os

spamwords = 1;
nonspamwords = 1; 

spamtest = 0;
nonspamtest = 0;

num_of_spam = 1;
nonnum_of_spam = 1;

dictionary_of_words=dict();

def create_bag_of_words_first(fileloc):

    global num_of_spam,nonnum_of_spam;
    
    list_of_files = os.listdir(fileloc);
    words_collection_dict = dict();
    temp_words_collection_dict = dict();
    spam_or_notspam_count = 0;
    object_temp_dict_list = list();

    for name_file in list_of_files:

        spam_or_notspam_count = spam_or_notspam_count + 1;
        temp_words_collection_dict[str(spam_or_notspam_count)] = dict();

        file_object = open(fileloc + name_file,"r");
        read_line = str.lower(re.sub("[%s]" % re.escape(string.punctuation), "", file_object.read()));
        list1 = re.split(",\\n",read_line);

        new_objects = [];

        for object in list1:
            new_objects.extend(object.split());
           
        for word in new_objects:
            if word not in temp_words_collection_dict[str(spam_or_notspam_count)]:
                temp_words_collection_dict[str(spam_or_notspam_count)][word] = 1;
                
    if "notspam" in fileloc:
        nonnum_of_spam = spam_or_notspam_count;
    else:
        num_of_spam = spam_or_notspam_count;
        
    for count_temp in range(1, spam_or_notspam_count + 1):
        for object_temp_dict in temp_words_collection_dict[str(count_temp)]:
            object_temp_dict_list.append(object_temp_dict);
            
    for object_temp_dict_list_text in object_temp_dict_list:
        if object_temp_dict_list_text in words_collection_dict:
            words_collection_dict[object_temp_dict_list_text] = words_collection_dict[object_temp_dict_list_text] + 1;
        else:
            words_collection_dict[object_temp_dict_list_text] = 1;
            
    return words_collection_dict;

def create_bag_of_words(doc_type,fileloc):

    global spamwords, num_of_spam, nonspamwords, nonnum_of_spam;
    
    spam_or_notspam_count = 0;
    spam_or_notspam_count_temp = 0;
    
    new_objects = [];
    read_line = "";

    list_of_files = os.listdir(fileloc);
    
    word_list=dict();
    
    for name_file in list_of_files:
        spam_or_notspam_count = spam_or_notspam_count + 1;

        file_object = open(fileloc + name_file,"r");
        read_line = read_line + str.lower(re.sub("[%s]" % re.escape(string.punctuation), "", file_object.read()));
        read_line = read_line + "\n";
        
        if(doc_type==""):
            for word in remove_punctuations_func(read_line):
                word_list[word] = True; 

    list1 = re.split(",\\n",read_line);
    
    for object in list1:
        new_objects.extend(object.split());
        
    spam_or_notspam_count_temp = len(new_objects);
    
    if("spam" in fileloc):
        spamwords = spam_or_notspam_count_temp;
        num_of_spam = spam_or_notspam_count;
    else:
        nonspamwords = spam_or_notspam_count_temp;
        nonnum_of_spam = spam_or_notspam_count;
        
    if doc_type=="mydoctype":
        words_collection_dict = [collections.Counter(re.findall(r"\w+", txt)) for txt in list1];
        
    return words_collection_dict;

def testdata(given_datas, expect,dictionary_of_words, feature):

    global spamwords, num_of_spam, nonspamwords, nonnum_of_spam, spamtest, nonspamtest;
        
    acc = 4;
    temp1 = 0;    
    
    acc_spam_or_notspam_count = 0;
    temp2 = 0;
    
    list_of_files = os.listdir(given_datas);
    
    for name_file in list_of_files:
        
        if("notspam" in given_datas):
            nonspamtest = nonspamtest + 1;
        else:
            spamtest = spamtest + 1;
            
        my_file = open(given_datas + name_file,"r");
        read_line = str.lower(re.sub("[%s]" % re.escape(string.punctuation), "", my_file.read()));
        list1 = re.split(",\\n" , read_line);
        new_objects = [];

        condprobspam = Decimal(1);
        condprobnotspam = Decimal(1);
        
        for object in list1:
            new_objects.extend(object.split());

        for word in new_objects:
            if word in dictionary_of_words["spam"][0]:
                temp_word = float(dictionary_of_words["spam"][0][word]);
                if(temp_word != 0):
                    condprobspam = calculate_conditional_probability_spam(feature, condprobspam, num_of_spam, spamwords);
            else:
                condprobspam = calculate_conditional_probability_spam(feature, condprobspam, num_of_spam, spamwords);
                temp1 = temp1 + 1;
                
            if word in dictionary_of_words["notspam"][0]:
                temp_word = dictionary_of_words["notspam"][0][word];
                if(temp_word != 0):
                    condprobnotspam = calculate_conditional_probability_non_spam(feature, condprobnotspam, temp_word, nonspamwords, nonum_of_spam);
            else:
                temp2 = temp2 + 1;
                condprobnotspam = calculate_conditional_probability_non_spam(feature, condprobnotspam, temp_word, nonspamwords, nonum_of_spam);
         
        psam = 1.0;
        pnotspam = 1.0;

        c = float(num_of_spam + nonnum_of_spam);

        psam = num_of_spam / c;
        pnotspam = nonnum_of_spam / c;

        psam = Decimal(0.5); 
        pnotspam = Decimal(0.5);

        finalpspam = condprobspam * psam;
        finalpnotspam = condprobnotspam * pnotspam;

        acc_spam_or_notspam_count = check_spam(finalpspam, finalpnotspam, expect);

    return acc_spam_or_notspam_count;

def calculate_conditional_probability_spam(feature, condprobspam, num_of_spam, spamwords):
    if feature != "mydoctype":
        condprobspam = condprobspam * Decimal((1 / num_of_spam));
    else:
        condprobspam = condprobspam * Decimal((1 / (spamwords / num_of_spam)));
    return condprobspam;

def calculate_conditional_probability_non_spam(feature, condprobnotspam, temp_word, nonspamwords, nonum_of_spam):
    if feature=="mydoctype":
        condprobnotspam = condprobnotspam * Decimal((temp_word / (nonspamwords / nonnum_of_spam)));
    else: 
        condprobnotspam = condprobnotspam * Decimal((temp_word / nonnum_of_spam));
    return condprobnotspam;

def check_spam(finalpspam, finalpnotspam, expect):
    
    if(finalpspam>finalpnotspam):
        if(expect == "spam"):
            acc_spam_or_notspam_count+=1
    else:
        if(expect == "notspam"):
            acc_spam_or_notspam_count+=1

doc_type = "mydoctype";
dictionary_of_words["notspam"] = dict();
dictionary_of_words["spam"] = dict();

if doc_type != "mydoctype":
    dictionary_of_words["spam"] = create_bag_of_words_first("train/spam/");
    dictionary_of_words["notspam"] = create_bag_of_words_first("train/notspam/");
else:
    dictionary_of_words["spam"] = create_bag_of_words(doc_type,"train/spam/");
    dictionary_of_words["notspam"] = create_bag_of_words(doc_type,"train/notspam/");
    
print(dictionary_of_words);

print("Spam Accuracy");
spam = testdata("test/spam/","spam",dictionary_of_words,doc_type);
print(spam);
print(spamtest);
print((a / spamtest) * 100.0);

print("Non_spam Accuracy");
Nspam = testdata("test/notspam/","notspam",dictionary_of_words,doc_type);
print(Nspam);
print(nonspamtest);
print((c / nonspamtest) * 100.0);


