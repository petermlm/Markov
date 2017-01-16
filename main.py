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


def makeNetwork():
    tokens_word2index = {}
    tokens_index2word = []

    # Read every word and build matrix
    regex_special = re.compile("[" + "".join(special_chars) + "]")
    regex_ignored = re.compile("[" + "".join(ignored_chars) + "]")

    cindex = 0
    with open("the_idiot") as fd:
        for line in fd:
            for token in cleanLine(regex_special, regex_ignored, line):
                if token not in tokens_word2index:
                    tokens_word2index[token] = cindex
                    tokens_index2word.append(token)
                    cindex += 1

    # Count
    network = []
    words_num = cindex
    for i in range(words_num):
        network.append(np.zeros(words_num))

    prev = ""
    cur = ""
    first_step = True

    with open("the_idiot") as fd:
        for line in fd:
            for token in cleanLine(regex_special, regex_ignored, line):
                if first_step:
                    cur = token
                    first_step = False
                    continue

                prev = cur
                cur = token

                prev_index = tokens_word2index[prev]
                cur_index = tokens_word2index[cur]

                network[prev_index][cur_index] += 1

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
        next_prob_cum = 0
        for next_index, next_prob in enumerate(network[c_index]):
            next_prob_cum += next_prob

            if rand_val < next_prob_cum:
                c_index = next_index
                break

    sys.stdout.write("\n")


if __name__ == "__main__":
    network, tokens_index2word = makeNetwork()

    # network = [
    #     np.array([0.05, 0.8, 0.15]),
    #     np.array([0.15, 0.05, 0.8]),
    #     np.array([0.8, 0.15, 0.05])
    # ]
    #
    # tokens_index2word = ["i", "am", "me"]

    makeRandomText(network, tokens_index2word, 100)
