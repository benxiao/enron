import json
from gensim import corpora
from gensim.models.wrappers.ldamallet import LdaMallet
from multiprocessing import cpu_count

MALLET_PATH = '/usr/local/mallet-2.0.6/bin/mallet'
DATA_PATH = '../data/enron'

if __name__ == '__main__':
    entire_corpus = []
    for y in range(2000, 2001):
        for m in range(1, 13):
            lst = json.load(open('processed_{}_{}.json'.format(y, m)))
            entire_corpus.extend(lst)
            # constructing a document-term matrix
    dictionary = corpora.Dictionary(entire_corpus)
    dictionary.filter_extremes(5, 0.1)
    dictionary.save('enron_dict.dict')
    dictionary = corpora.Dictionary.load('enron_dict.dict')
    for y in range(2000, 2001):
        for m in range(1, 13):
            lst = json.load(open('processed_{}_{}.json'.format(y, m)))
            corpus = [dictionary.doc2bow(x) for x in lst]
            lda = LdaMallet(
                mallet_path=MALLET_PATH,
                corpus=corpus,
                id2word=dictionary,
                num_topics=30,
                optimize_interval=10,
                iterations=3000,
                workers=cpu_count(),
            )
            lda.save(DATA_PATH + '/mallet_files/enron_{}_{}_mallet_model'.format(y, m))
