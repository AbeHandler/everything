import numpy as np
import copy
import pickle

from functools import lru_cache
from tqdm import tqdm_notebook as tqdm
from scipy.optimize import fmin_l_bfgs_b
from scipy.special import logsumexp
# http://cs.jhu.edu/~jason/tutorials/loglin/formulas.pdf

@lru_cache(maxsize=1000000)
def phi(n_i, e, z):    
    '''One feature needs to be the PMI of n_i'''

    f1 = not n_i[0].isupper() and z == 0
    f2 = not n_i[0].lower() in e.lower() and z == 0
    
    f3 = n_i[0].isupper() and n_i.lower() in e.lower() and z == 1
    f4 = n_i[0].isupper() and z == 1

    return np.asarray([f1, f2, f3, f4], dtype=np.double)


def predict_Y_for_point(dno, w, feats):
    '''returns a distribution over the Y labels'''
    numerators = feats[dno].dot(w)
    D = logsumexp(numerators, axis=0)
    probs = np.exp(numerators - D)
    return probs.reshape(len(numerators),1)
    

def get_expected_feats_for_point(dno, w, feats):
    return np.sum(predict_Y_for_point(dno, w=w, feats=feats) * feats[dno], axis=0)


def get_expected_feats_for_dataset(dataset, w, feats):
    return np.vstack([get_expected_feats_for_point(dno, w, feats) for dno in range(len(dataset))])


def fprime(w, *args):
    '''
    Big F in Eisners notation
    
    This can handle weighted examples via the point_weights argument
    '''
    dataset, Y, feats, actual_feats, point_weights = args
    expected_feature_counts = get_expected_feats_for_dataset(dataset, w, feats)
    delta = np.sum(point_weights * actual_feats, axis=0) - np.sum(point_weights * expected_feature_counts, axis=0)
    return -1 * delta


def make_feats(dataset):
    Y = set([_[0] for _ in dataset])

    feats = np.zeros((len(dataset), len(Y), len(w)))

    for ino, p in tqdm(enumerate(dataset), total=len(dataset)):
        ni, e, z = p
        for yno, y in enumerate(Y):
            feats[ino][yno] = phi(y, e, z)

    return feats


def get_probs(w, *args):
    dataset, Y, feats, actual_feats = args
    n = actual_feats.dot(w)
    
    d = []
    for yno, y in enumerate(Y):
        d.append(feats[:,yno].dot(w))
    return np.exp(n - logsumexp(d, axis=0))


def get_log_probs(w, *args):
    '''
    Big F in Eisners notation
    
    This can handle weighted examples via the point_weights param
    '''
    
    dataset, Y, feats, actual_feats, point_weights = args
    
    n = actual_feats.dot(w)
    
    d = []
    for yno, y in enumerate(Y):
        d.append(feats[:,yno].dot(w))

    return -1 * np.sum((n - logsumexp(d, axis=0)))


def make_acutal_feats(dataset, w):
    af = np.zeros((len(dataset), len(w)), dtype=np.float)
    for dno, (y, e, z) in enumerate(dataset):
        af[dno] = phi(y, e, z)
    return af


def make_all_feats(data_set):
    '''make all feats'''
    actual_feats = make_acutal_feats(data_set, w)
    feats = make_feats(data_set)
    
    return feats, actual_feats


if __name__ == "__main__":
   

    d0 = [("Ari", "Ariana", 1), 
      ("bill", "Ariana", 0), 
      ("bill", "Rihanna", 0),
      ("Riri", "Rihanna", 1),
      ("sand", "Ariana", 0)] 


    print("making feats")
            
    w = np.asarray([.2, .14, .32, .3])

    feats, actual_feats = make_all_feats(d0)
    
    point_weights = np.ones((len(d0), 1))
    
    Y = set([_[0] for _ in d0])
    
    assert Y == set([o[0] for o in d0])
    
    print("ok")
    print(np.exp(get_log_probs(w, d0, Y, feats, actual_feats, point_weights)))

    w, f, d = fmin_l_bfgs_b(func=get_log_probs, fprime=fprime, x0=w, args=(d0, Y, feats, actual_feats, point_weights))

    print(np.exp(get_log_probs(w, d0, Y, feats, actual_feats, point_weights)))
