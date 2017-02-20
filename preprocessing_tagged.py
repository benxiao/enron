"""
Assume input is a lst of strings
"""
__author__ = 'Ran Xiao'
# built in
import time
import json
from functools import partial
from collections import Counter
from multiprocessing import Pool, cpu_count

# 3rd-party
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

# Constants
NOUN_TYPES = ('NN','NNS','NNP','NNPS')
PLURAL_NOUN_TYPES = ('NNS', 'NNPS')
DATA_PATH = '../data/enron/tagged'
REMOVED = ['www', 'http', 'com']


# Acquired resources
lemmatizer = WordNetLemmatizer()
word_tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')


def predoc(tagged):
    """
    turn text into a list of tokens aka list of string for lda
    :param text:
    :return:
    """
    sent_components = [(lemmatizer.lemmatize(w), t) if t in PLURAL_NOUN_TYPES else (w, t) for (w, t) in tagged]
    # merge
    sent_components = merge_components(sent_components)
    # get only nouns
    nouns = [w for w, t in sent_components if t in NOUN_TYPES]
    # get lower
    return [x.lower() for x in nouns]


def find_ngrams(lst_str, threshold=0.2, minimum=10):
    word_freq = Counter(lst_str)
    unique_words = word_freq.keys()
    n_grams = []
    for w in unique_words:
        if '_' in w:
            cur = w
            while '_' in cur:
                next_ = cur[(cur.find('_')+1):]
                if (word_freq[cur] and # greater than 0
                    (word_freq[next_] >= minimum and word_freq[cur] >= minimum) and# pass minimum check
                    word_freq[cur] / (word_freq[cur] + word_freq[next_] >= threshold) # pass threshold check
                    ): # find n_gram
                    n_grams.append(cur)
                    break
                else:
                    cur = next_
    return set(n_grams) # hashset for fast lookups


def get_result(nouns, known=None):
    """
    :param known:
    :param nouns:
    :return:
    """
    if known is None:
        raise ValueError('known cannot be none')
    if not known:
        raise ValueError('known cannot be emtpy!')

    transformed = []
    for w in nouns:
        if '_' not in w:
            transformed.append(w)
        else:
            cur = w
            added = False
            while '_' in cur:
                if cur in known:
                    transformed.append(cur)
                    added = True
                    break
                cur = cur[(cur.find('_')+1):] # beautiful_painting -> painting
            if not added:
                transformed.append(cur)
    return transformed


def merge_components(sent_components):
    """
    complexity: O(n)
    merge adjacement nouns together
    merge adjacement nouns with one adjative
    :param sent_components:
    :return: merged sent_components
    """
    prev = None
    merged = []
    for w, t in sent_components:
        if prev in NOUN_TYPES and t in NOUN_TYPES:
            last = merged[-1]
            new_word = last[0] + '_' + w
            merged[-1] = (new_word, t)

        elif prev == 'JJ' and t in NOUN_TYPES:
            last = merged[-1]
            new_word = last[0] + '_' + w
            merged[-1] = (new_word, t)
        else:
            merged.append((w, t))
        prev = t
    return merged



if __name__ == '__main__':
    start = time.time()
    # create processing pool
    pool = Pool(cpu_count())

    for i in range(2000, 2001):
        for j in range(1, 13):
            print('processing {}...'.format((i,j)))
            raw = json.load(open(DATA_PATH+'/tagged_{}_{}.json'.format(i, j)))
            lst_lst_nouns = pool.map(predoc, raw)
            lst_nouns = [x for l in lst_lst_nouns for x in l]
            n_grams = find_ngrams(lst_nouns)
            print(n_grams)
            # share n_grams acro00ss multiple processes
            target = partial(get_result, known=n_grams)
            result = pool.map(target, lst_lst_nouns)
            json.dump(result, open('processed_{}_{}.json'.format(i,j), 'w'))
    pool.close()

