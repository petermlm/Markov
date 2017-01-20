This is a simple implementation of a text generator using Markov Chains. A
Markov Chain, which is a probability distribution of the form:

    P(Xn | Xn-1)

Can be build from text. Like this, each state of the chain is a word, and each
pair of words forms a transition.

Given a particular text, a chain representing the transitions in words of a
text built. Using that chain, random text is generated.

# How to Use

You'll just need Python3 and Numpy.

Usage:

    main.py source_file [words]

Where `source_file` is a file with text from whichthe chain will be built, and
words is an optional parameter which states the number of words in the
generated text (defaults to 100).

If `source_file` is "-", values are read from stdin.
