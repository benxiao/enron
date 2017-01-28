from gensim.matutils import hellinger
import json

# define a merge
# when more than 1 topic_dist points to a particular topic_dist in the next time slice.


# define a split
# a particular topic_dist points to more than 1 topic_dist in the next time slice.
class DynamicTopic:
    """
    
    """
    def __init__(self, dynamic_model, time_slice, topic_n):
        self._dm = dynamic_model
        self._time_slice = time_slice
        self._topic_n = topic_n

    def next(self):
        related_future_topics = self._dm.get_outgoing_connections(self._time_slice, self._topic_n)
        return [DynamicTopic(self._dm, self._time_slice+1, i) for i in related_future_topics]

    def __str__(self):
        return str(self._dm.get_topic_keys(self._time_slice, self._topic_n))

    __repr__ = __str__


class TopicChain:
    """
    json format [[{topic(k:p)}, {topic}, {topic} ...]... more time_slices... ]
    while k is the keyword and p is the probability
    """
    def __init__(self, json_, **kwargs):
        self._data = json.load(open(json_))
        self._data = [[{k: float(y[k]) for k in y} for y in x] for x in self._data]
        self._threshold = 0.3
        self._max_outgoing = 3
        self._conn = self._generate_conns_from_data()


    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, new_value):
        self._threshold = new_value
        self._conn = self._generate_conns_from_data()

    @property
    def max_outgoing(self):
        return self._max_outgoing

    @max_outgoing.setter
    def max_outgoing(self, new_value):
        self._max_outgoing = new_value
        self._conn = self._generate_conns_from_data()

    def get_topics_with_outgoing_connections(self, time_slice):
        return [i for i, x in enumerate(self._conn[time_slice]) if len(x)]

    def get_outgoing_connections(self, time_slice, topic_n):
        return self._conn[time_slice][topic_n]

    def get_topic_keys(self, time_slice, topic_n):
        return self._data[time_slice][topic_n]

    def get_dynamic_topic(self, time_slice, topic_n):
        return DynamicTopic(self, time_slice, topic_n)

    def _generate_conns_from_data(self):
        result = []
        data = self._data
        for i in range(len(data) - 1):
            lda_topic_1 = data[i]
            lda_topic_2 = data[i + 1]
            lda_topic_1 = [sorted([(topic[k], k) for k in topic], key=lambda x: -x[0]) for topic in lda_topic_1]
            lda_topic_2 = [sorted([(topic[k], k) for k in topic], key=lambda x: -x[0]) for topic in lda_topic_2]
            l = len(lda_topic_1)
            d_matrix = [[None] * l for _ in range(l)]
            for i in range(l):
                for j in range(l):
                    d_matrix[i][j] = self.compute_hellinger(lda_topic_1[i], lda_topic_2[j])
            slice_result = []
            for group in self.get_edges_between_two_time_slices(d_matrix,
                                                                threshold=self.threshold,
                                                                max_outgoing=self.max_outgoing):
                slice_result.append([x[1] for x in group])
            result.append(slice_result)
        return result

    @staticmethod
    def compute_hellinger(dist01, dist02):
        unique_words = set([x[1] for x in dist01] + [x[1] for x in dist02])
        dict_dist01 = {x[1]: x[0] for x in dist01}
        dict_dist02 = {x[1]: x[0] for x in dist02}
        vec01 = [dict_dist01.get(x, 0) for x in unique_words]
        vec02 = [dict_dist02.get(x, 0) for x in unique_words]
        return hellinger(vec01, vec02)

    @staticmethod
    def get_edges_between_two_time_slices(matrix, threshold=0.3, max_outgoing=3):
        lst = []
        l = len(matrix)
        for i in range(l):
            outgoings = list(filter(lambda x: x[-1] < threshold, ((i, j, matrix[i][j]) for j in range(l))))
            outgoings = sorted(outgoings, key=lambda x: x[-1])[:max_outgoing]
            lst.append(outgoings)
        return lst

if __name__ == '__main__':
    dm = TopicChain('json_files/topic_keys.json')
    print(dm.get_topics_with_outgoing_connections(0))
    print(dm.get_outgoing_connections(0, 2))
    print(dm.get_topic_keys(0, 14))
    print(dm.get_topic_keys(1, 0))
    print(dm._conn)
    dm.threshold = 0.4
    print("*" * 200)
    print(dm._conn)
    print(dm.get_dynamic_topic(0,0))
    print(dm.get_dynamic_topic(0,0).next())
    dm.max_outgoing = 1
    print(dm._conn)
