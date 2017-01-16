import re
import random
import sys

import numpy as np

def makeNetwork():
    tokens_count = {}
    tokens_index = []

    # Read every word and build matrix
    regex = re.compile("[.,;!?\"”“]")

    cindex = 0
    with open("the_idiot") as f:
        for i in f:
            i_strip = i.strip()
            # i_regex = regex.sub(" \g<0> ", i_strip)
            i_regex = regex.sub(" ", i_strip)
            i_low = i_regex.lower()
            tokens = i_low.split()

            for j in tokens:
                if j not in tokens_count:
                    tokens_count[j] = cindex
                    tokens_index.append(j)
                    cindex += 1

    # Count
    network = []
    for i in range(len(tokens_count)):
        network.append(np.zeros(len(tokens_count)))

    prev = ""
    cur = ""

    step = 0

    with open("the_idiot") as f:
        for i in f:
            i_strip = i.strip()
            # i_regex = regex.sub(" \g<0> ", i_strip)
            i_regex = regex.sub(" ", i_strip)
            i_low = i_regex.lower()
            tokens = i_low.split()

            for j in tokens:
                if step == 0:
                    prev = j
                elif step == 1:
                    cur = j
                else:
                    prev = cur
                    cur = j
                    network[tokens_count[prev]][tokens_count[cur]] += 1

                step += 1

    # Normalize
    for i in range(len(network)):
        network[i] = network[i] / network[i].sum()

    return network, tokens_index


def makeRandomText(network, tokens_index, words_num):
    c_index = random.randint(0, len(network)-1)

    for i in range(words_num):
        sys.stdout.write(tokens_index[c_index] + " ")

        # prev = tokens_index[c_index]
        # cur = tokens_index[c_index]
        # while prev == cur:
        #     r = random.random()
        #     for jindex, j in enumerate(network[c_index]):
        #         if r < j:
        #             c_index = jindex
        #             cur = tokens_index[c_index]
        #             print(r)
        #             print(prev, cur)
        #             break

        r = random.random()
        for jindex, j in enumerate(network[c_index]):
            if r < j:
                c_index = jindex
                break


if __name__ == "__main__":
    network, tokens_index = makeNetwork()

    # network = [
    #     np.array([0.05, 0.8, 0.15]),
    #     np.array([0.15, 0.05, 0.8]),
    #     np.array([0.8, 0.15, 0.05])
    # ]
    #
    # tokens_index = ["i", "am", "me"]

    makeRandomText(network, tokens_index, 1000)
