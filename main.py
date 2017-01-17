#!/usr/bin/env python3

import re
import random
import sys

import numpy as np


special_chars = [
    ".",
    ",",
    ";",
    "!",
    "?",
]

ignored_chars = [
    "\"",
    "”",
    "“",
    "(",
    ")"
]

cap_chars = [
    ".",
    "!",
    "?",
]


def cleanLine(regex_special, regex_ignored, line):
    line = line.strip()
    line = regex_special.sub(" \g<0> ", line)
    line = regex_ignored.sub(" ", line)
    line = line.lower()
    return line.split()


def makeNetwork(source_file):
    tokens_word2index = {}
    tokens_index2word = []
    network = []

    # Read every word and build matrix
    regex_special = re.compile("[" + "".join(special_chars) + "]")
    regex_ignored = re.compile("[" + "".join(ignored_chars) + "]")

    first_step = True
    cindex = 0
    prev = ""
    cur = ""

    # with open(source_file) as fd:
    if source_file != None:
        fd = open(source_file)
    else:
        fd = sys.stdin

    for line in fd:
        for token in cleanLine(regex_special, regex_ignored, line):
            if token not in tokens_word2index:
                tokens_word2index[token] = cindex
                tokens_index2word.append(token)
                network.append(np.zeros(len(network) + 1))
                cindex += 1

            if first_step:
                cur = token
                first_step = False
                network[0][0] = 0
                continue

            prev = cur
            cur = token

            prev_index = tokens_word2index[prev]
            cur_index = tokens_word2index[cur]

            if len(network[prev_index]) <= cur_index:
                zeros_num = cur_index - len(network[prev_index]) + 1
                network[prev_index] = np.append(network[prev_index], np.zeros(zeros_num))

            network[prev_index][cur_index] += 1

    if source_file != None:
        fd.close()

    # Normalize
    for i in range(len(network)):
        network[i] = network[i] / network[i].sum()

    return network, tokens_index2word


def makeRandomText(network, tokens_index2word, words_num):
    c_index = random.randint(0, len(network)-1)

    prev_word = ""
    for i in range(words_num):
        # Write current word
        c_word = tokens_index2word[c_index]

        if i != 0 and c_word not in special_chars:
            sys.stdout.write(" ")

        if i == 0 or prev_word in cap_chars or c_word == "i":
            sys.stdout.write(c_word[0].upper() + c_word[1:])
        else:
            sys.stdout.write(c_word)

        prev_word = c_word

        # Determine next index
        rand_val = random.random()
        next_prob_cumul = 0
        for next_index, next_prob in enumerate(network[c_index]):
            next_prob_cumul += next_prob

            if rand_val < next_prob_cumul:
                c_index = next_index
                break

    sys.stdout.write("\n")


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: main.py source_file [words]")

    if sys.argv[1] == "-":
        source_file = None
    else:
        source_file = sys.argv[1]

    words_num = 100
    if len(sys.argv) == 3:
        words_num = int(sys.argv[2])

    network, tokens_index2word = makeNetwork(source_file)
    makeRandomText(network, tokens_index2word, words_num)
