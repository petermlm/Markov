#!/usr/bin/env python3

import re
import random
import sys

import numpy as np


special_chars = [
    '.',
    ',',
    ';',
    '!',
    '?',
]

ignored_chars = [
    '\'',
    '"',
    '”',
    '“',
    '(',
    ')'
]

cap_chars = [
    '.',
    '!',
    '?',
]


words_num = 100


def tokenize(text, regex_special, regex_ignored):
    text = text.strip()
    text = regex_special.sub(' \g<0> ', text)
    text = regex_ignored.sub(' ', text)
    text = text.lower()
    return text.split()


def make_network(text):
    tokens_word2index = {}
    tokens_index2word = []
    network = []

    # Read every word and build matrix
    regex_special = re.compile('[' + ''.join(special_chars) + ']')
    regex_ignored = re.compile('[' + ''.join(ignored_chars) + ']')

    first_step = True
    cindex = 0
    prev = ''
    cur = ''

    for token in tokenize(text, regex_special, regex_ignored):
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

    # Last word loops back to first
    network[-1][0] += 1

    # Normalize
    for i in range(len(network)):
        network[i] = network[i] / network[i].sum()

    return network, tokens_index2word


def make_random_text(network, tokens_index2word, words_num):
    c_index = random.randint(0, len(network) - 1)
    output = ''

    prev_word = ''
    for i in range(words_num):
        # Write current word
        c_word = tokens_index2word[c_index]

        if i != 0 and c_word not in special_chars:
            output += ' '

        if i == 0 or prev_word in cap_chars or c_word == 'i':
            output += c_word[0].upper() + c_word[1:]
        else:
            output += c_word

        prev_word = c_word

        # Determine next index
        rand_val = random.random()
        next_prob_cumul = 0
        for next_index, next_prob in enumerate(network[c_index]):
            next_prob_cumul += next_prob

            if rand_val < next_prob_cumul:
                c_index = next_index
                break

    return output


def markov(text, words_num=100):
    """
    Reads the string in `text` and returns a generated text with `words_num`
    words.
    """

    network, tokens_index2word = make_network(text)
    return make_random_text(network, tokens_index2word, words_num)


def read(source=None, words_num=100):
    """
    Reads the text in the file given to `source` and returns a generated text
    with `words_num` words. If `source` is `None`, read from `stdin`.
    """

    if source is not None:
        fd = open(source)
    else:
        fd = sys.stdin

    text = fd.read()
    return markov(text, words_num)


if __name__ == '__main__':
    argc = len(sys.argv)
    if not (2 <= argc <= 3):
        print("Usage: main.py source_file [words]")
        exit(1)

    if sys.argv[1] == "-":
        source = None
    else:
        source = sys.argv[1]

    if len(sys.argv) == 3:
        try:
            words_num = int(sys.argv[2])
        except ValueError:
            print('Word number not an int')
            exit(1)

        generated = read(source, words_num=words_num)

    else:
        generated = read(source)

    print(generated)
