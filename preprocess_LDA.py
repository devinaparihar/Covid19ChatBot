import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem.porter import *
import numpy as np
np.random.seed(400)


# Tokenize, stem and removing stopwords

import nltk
nltk.download('stopwords')

stemmer = PorterStemmer()

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['coronavirus', 'Koronavirus', 'trump', 'covid-19', 'corona', 'covid', 
                  'covid19', 'covd', 'virus', 'pandemic', 'chinese', 'china', 'wuhan', 'ncov', 'Kungflu',
                  'chinavirus', 'fuck', 'fuckers', 'covidiot'])


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in stopwords:
            result.append(stemmer.stem(token))
    return result
