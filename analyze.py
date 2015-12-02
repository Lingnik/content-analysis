#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
"""
Content analysis in python.
"""

import sys
import re
import nltk
from nltk.util import ngrams as ng

if len(sys.argv) > 1:
    DICTFILE = sys.argv[1]
    TEXTFILE = sys.argv[2]
else:
    DICTFILE = 'dict.txt'
    TEXTFILE = 'melanie_only.txt'

MIN_NGRAMS = 2
MAX_NGRAMS = 6

MIN_UNIQUE_COUNT = 10
MAX_UNIQUE_COUNT = 999


def plot_ngrams(ngrams_list, max_results=100):
    fd = nltk.FreqDist(ngrams_list)
    fd.plot(max_results)


def ngrams_to_strngrams(ngrams_list):
    return [' '.join(n) for n in ngrams_list]


def flatten_ngrams(ngrams_dict):
    ngrams_list = []
    for ngrams in ngrams_dict:
        ngrams_list.extend(ngrams_dict[ngrams])
    return ngrams_list


def text_to_ngrams(text):
    ngrams_dict = {}
    for n in range(MIN_NGRAMS, MAX_NGRAMS + 1):
        ngrams_dict[n] = [n for n in ng(text.split(), n)]
    return ngrams_dict


def read_file(f_in):
    """
    Read a file, return an array of strings (lines).
    """
    fd_in = open(f_in)
    lines = fd_in.readlines()
    fd_in.close()
    return lines


def lines_to_str(lines):
    s = ""
    for line in lines:
        s += " {}".format(line)
    return s


def text_to_words(text):
    return nltk.word_tokenize(text)


def unique_words(words):
    uwords = {}
    for word in words:
        uwords[word] = uwords[word] + 1 if uwords.get(word, None) else 1
    return uwords


def metrics():
    """
    Calculate and print basic text metrics.
    """
    lines = read_file(TEXTFILE)
    text = lines_to_str(lines)
    words = text_to_words(text)
    uwords = unique_words(words)
    ngrams = text_to_ngrams(text)
    return ngrams

    print('')
    print('Metrics')
    print('Number of words: {}'.format(len(words)))
    print('Number of unique words: {}'.format(len(uwords)))
    print('')
    print('Frequency Analysis of words > {} and < {} occurrences'.format(MIN_UNIQUE_COUNT, MAX_UNIQUE_COUNT))
    print('Number of words: {}'.format(len(["{}: {}".format(uwords[w], w) for w in uwords if uwords[w] > MIN_UNIQUE_COUNT and uwords[w] <= MAX_UNIQUE_COUNT])))
    #print('\n'.join(sorted(["{0: >3}: {1}".format(uwords[w], w) for w in uwords if uwords[w] >= MIN_UNIQUE_COUNT and uwords[w] <= MAX_UNIQUE_COUNT])))
    print('')
    #analyze_dictionary(ngrams, DICTFILE)


def analyze_dictionary(uwords, dictfile):
    """
    Analyze dictionary against text.
    source: http://conjugateprior.org/software/ca-in-python/
    """
    # fd_text = open(textfile)
    # text = fd_text.read().split()  # lowercase the text
    # fd_text.close()

    fd_dict = open(dictfile)
    dict_lines = fd_dict.readlines()
    fd_dict.close()

    dic = {}
    scores = {}

    # a default category for simple word lists
    current_category = "Default"
    scores[current_category] = 0

    # inhale the dictionary
    for dict_line in dict_lines:
        if dict_line[0:2] == '>>':
            pass
            current_category = dict_line[2:].strip()
            scores[current_category] = 0
        else:
            dict_line = dict_line.strip()
            if len(dict_line) > 0:
                pattern = re.compile(dict_line, re.IGNORECASE)
                dic[pattern] = current_category

    # examine the text
    for uword in uwords:
        match = False
        for pattern in dic.keys():
            if pattern.match(uword):
                categ = dic[pattern]
                scores[categ] = scores[categ] + (uwords[uword] if isinstance(uwords, dict) else 1)
                match = True
            else:
                scores["Default"] = scores["Default"] + (uwords[uword] if isinstance(uwords, dict) else 1)
        if not match:
            print("{0: <3}: {1}".format((uwords[uword] if isinstance(uwords, dict) else 1), uword))
    print('-----')

    for key in scores.keys():
        print(key, ":", scores[key])


