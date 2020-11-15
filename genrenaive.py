#!/usr/bin/python3
# A Naive bayes classifier for Cyber Analytics and Machine Learning, Group 1
# Authors: Joshua Niemann, Michael Smith

# imports
import math
import re

# Define variables
training = .7
rockprobability = .6 # Found by distribution of song genre
popprobability = .4


def remove_special_characters(line):
    return (re.sub('[^A-Za-z0-9 ]+', '', line))


def import_data(filename):
    output = []
    for i in open(filename, 'r'):
        split_data = i.split("\t")
        classification_tmp = (0 if split_data[0] == 'pop' else 1)
        data_tmp = (split_data[1])
        output.append([classification_tmp, data_tmp])
    return output


def process(line):
    data = remove_special_characters(line.lower()).split(" ")
    # surprisingly, this is the best way to remove all instances of '' from the data
    return data


def generate_probability_table(pop_wordlist, rock_wordlist):
    ##expect a pop wordlist and rock wordlist with frequencies for each
    # this method determines the frequency based on pop vs rock and returns a table
    freq_table = {}
    total_pop = len(pop_wordlist)
    total_rock = len(rock_wordlist)
    for i in pop_wordlist.keys():
        freq_table[i] = [pop_wordlist[i], 1]
    for i in rock_wordlist.keys():
        if (freq_table.get(i) != None):
            count = freq_table[i]
            count[1] = rock_wordlist[i]
        else:
            freq_table[i] = [1, rock_wordlist[i]]
    final_table = {}
    for i in freq_table.keys():
        final_table[i] = [(freq_table[i][0])/ (total_pop * len(freq_table)), (freq_table[i][1])/ (total_rock * len(freq_table))]
    return final_table


def train(data):
    # first thing i'm doing here is going through and finding probabilities
    # this method expects an import_data processed 2d array that contains a 0 or 1 for pop and rock, and a string of text to process.
    pop_wordlist = dict()
    rock_wordlist = dict()
    for i in data:
        processed_words = process(i[1])
        for word in processed_words:
            if (i[0] == 0):
                if (pop_wordlist.get(word) == None):
                    pop_wordlist[word] = 2
                else:
                    pop_wordlist[word] = pop_wordlist[word] + 1
            elif (i[0] == 1):
                if (rock_wordlist.get(word) == None):
                    rock_wordlist[word] = 2
                else:
                    rock_wordlist[word] = rock_wordlist[word] + 1
    table = generate_probability_table(pop_wordlist, rock_wordlist)
    return table


def calculate(data, trained_table):
    rocktotal = rockprobability
    poptotal = popprobability

    processed_words = process(data[1])
    for word in processed_words:
        if (trained_table.get(word) != None):
            if(trained_table[word][1] != 0):
                rocktotal *= trained_table[word][1]
            if (trained_table[word][0] != 0):
                poptotal *= trained_table[word][0]

    if(rocktotal >= poptotal):
        return 1
    else:
        return 0


def calculate_pop(data, trained_table, ppop):
    poptotal = []

    for i in data:
        total = ppop
        processed_words = process(i[1])
        for word in processed_words:
            if (trained_table.get(word) == None):
                total += 0
            else:
                if (trained_table[word][1] != 0):
                    total *= trained_table[word][0]
        poptotal.append(total)
    return poptotal


def main():
    filedata = import_data('SMSrockCollection')
    traindata = filedata[:math.floor(training * len(filedata))]
    testdata = filedata[len(filedata) - math.floor(training * len(filedata)):]  # was missing a :
    table = train(traindata)

    tpcount = 0 # Correctly labeled rock
    tncount = 0 # Correctly labeled pop
    fpcount = 0 # pop labeled as rock
    fncount = 0 # rock labeled as pop

    answers = []
    for i in testdata:
        answers.append(calculate(i, table))

    rockcount = 0
    popcount = 0
    counter = 0

    for i in testdata:
        if i[0] == 1 and answers[counter] == 1:
            tpcount += 1
        elif i[0] == 1 and answers[counter] == 0:
            fpcount += 1
        elif i[0] == 0 and answers[counter] == 0:
            tncount += 1
        else:
            fncount += 1
        counter += 1

    accuracy = (tpcount + tncount) / (tpcount + fpcount + tncount + fncount) * 100
    precision = tpcount / (tpcount + fpcount) * 100
    recall = tpcount / (tpcount + fncount) * 100

    print('TP: ', tpcount)
    print('FP: ', fpcount)
    print('TN: ', tncount)
    print('FN: ', fncount)
    print('Accuracy: ', accuracy, '%')
    print('Precision: ', precision, '%')
    print('Recall: ', recall, '%')

    test1 = [0, "dude! dude! look!"]
    test2 = [1, "winner babe! click for prize"]
    print(calculate(test1,table))
    print(calculate(test2, table))



main()