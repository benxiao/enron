from pandas import DataFrame
import pandas as pd
import pickle
import json
from nltk.tokenize import RegexpTokenizer, word_tokenize


def wrapline(text, length=200):
    l = len(text)
    c = 0
    while c+length <= l:
        print(text[c:c+length])
        c += length
    if c < l:
        print(text[c:])



if __name__ == '__main__':
    lst = json.load(open('enron_email.json'))

    df = DataFrame(lst)
    df.Date = pd.to_datetime(df.Date, errors='coerce')
    for i in range(2000, 2002):
        for j in range(1, 13):
            sel = df[(df.Date.dt.year == i) & (df.Date.dt.month == j)]['content']
            json.dump(list(sel), open('enron_{}_{}'.format(i, j), 'w'))




