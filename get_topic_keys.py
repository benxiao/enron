from gensim.models.wrappers.ldamallet import LdaMallet
import json

result = []
for y in [2000, 2001]:
    for m in range(1, 13):
        topic_keys = []
        mallet_name = 'mallet_models/{}-{}_mallet'.format(y, m)
        lda = LdaMallet.load(mallet_name)
        for i in range(30):
            topic_keys.append({w: str(p) for p, w in lda.show_topic(i, num_words=30)})
        result.append(topic_keys)

json.dump(result, open('json_files/topic_keys.json','w'))

