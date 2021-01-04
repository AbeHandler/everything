import pandas as pd
import sys
import ipdb
import pickle
import numpy as np
from vectors.utils import Corpus
from sklearn.neighbors import KDTree
from sklearn.decomposition import RandomizedPCA

corpus = Corpus("data/GOP_REL_ONLY.csv", n=6266)

# N = int(sys.argv[1]) if len(sys.argv) > 1 else 6266
corpus = Corpus("data/GOP_REL_ONLY.csv", n=6266)
word_doc = np.zeros((len(corpus.vocab), len(corpus.docs)))

for di, doc in enumerate(corpus.docs):
    for wrd in corpus.docs[di]:
        word_doc[corpus.windex[wrd]][di] = 1

pca = RandomizedPCA(n_components=100)
pca.fit(word_doc)

low_dim = pca.transform(word_doc)

kdt = KDTree(low_dim, leaf_size=200, metric='euclidean')

pickle.dump(low_dim, open("low_dim.r", "w"))
pickle.dump(kdt, open("vecs.r", "w"))


kdt = pickle.load(open("vecs.r", "r"))
low_dim = pickle.load(open("low_dim.r", "r"))

pt_1 = low_dim[corpus.windex[sys.argv[1]]]
pt_2 = low_dim[corpus.windex[sys.argv[2]]]
pt_3 = low_dim[corpus.windex[sys.argv[3]]]

answers = kdt.query(pt_1 + pt_2 - pt_3, k=10)

for d in answers[1]:
    for c in d:
        print corpus.reverse_windex[c]