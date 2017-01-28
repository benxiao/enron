import json
import pandas as pd
from pandas import DataFrame
import pickle
import io
import gensim
from gensim import corpora
from gensim.models.wrappers.ldamallet import LdaMallet
from multiprocessing import cpu_count

MALLET_PATH='/usr/local/Cellar/mallet/2.0.7/bin/mallet'
df = pickle.load(open('json_files/enron_df.pkl','rb'))
df = df[df.time.notnull()]


dictionary = corpora.Dictionary([json.loads(x) for x in df.tokens.head(200)])
dictionary.filter_extremes(20, 0.1)

print(dictionary)


# for k, group in df.groupby(df.time.dt.year.map(lambda x: str(int(x))) + df.time.dt.month.map(lambda x: "-"+str(int(x)))):
#     if k.split('-')[0] in ['2000', '2001']:
#         print(k)
#         tokens_at_that_month = list(group.tokens)
#         tokens_at_that_month = [json.loads(x) for x in tokens_at_that_month]
#         corpus = [dictionary.doc2bow(x) for x in tokens_at_that_month]
#         lda = LdaMallet(
#             mallet_path=MALLET_PATH,
#             corpus=corpus,
#             id2word=dictionary,
#             num_topics=30,
#             optimize_interval=10,
#             iterations=2000,
#             workers=cpu_count(),
#         )
#         lda.save('{}_mallet'.format(k))

