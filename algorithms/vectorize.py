import gensim
from .utils import preprocess
import numpy as np


class Sentence2Vec():
    """
    https://towardsdatascience.com/sentence-embedding-3053db22ea77
    http://proceedings.mlr.press/v37/kusnerb15.pdf
    """

    def __init__(self):
        self.word_vectors = gensim.models.KeyedVectors.load_word2vec_format(
            'data/GoogleNews-vectors-negative300.bin', binary=True)

    def predict(self, word):
        if word not in self.word_vectors:
            # print(f'Word "{word}" not found in word2vec model!')
            return None
        return self.word_vectors[word]

    def vectorize_tweet(self, tweet):
        content = tweet.content
        preprocessed_content_tokens = preprocess(content)
        tweet_vector = np.mean([self.predict(word)
                                for word in preprocessed_content_tokens if self.predict(word) is not None])
        return tweet_vector


class Tweet2Vec():
    pass
