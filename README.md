# Markov.py

This is a simple implementation of a text generator using Markov Chains.

A Markov Chain is a probability distribution of the form:

    P(Xn | Xn-1)

Given some text, a chain can be built where each node represents a word and
each transition represents the frequency of seeing word Xn after word Xn-1.

# How to Use

Python3 and Numpy are needed.

## Execute Script

    markov.py source_file [words]

Where `source_file` is a file with text from which the chain will be built, and
words is an optional parameter which states the number of words in the
generated text (defaults to 100).

If `source_file` is "-", values are read from `stdin`.

## Import

You can import the script:

    import markov

And use one of the functions.

    markov(text, words_num=100)

This will read the string in `text` and output a generated text with
`words_num` words.

    read(source=None, words_num=100)

This will read the text in the file given to `source` and outputs a generated
text with `words_num` words. If `source` is `None`, read from `stdin`.

# Style

To format, [Black](https://github.com/psf/black) is used.

# Tests

Simply run:

    python3 tests.py
