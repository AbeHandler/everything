import numpy as np
from scipy.optimize import fmin_l_bfgs_b
# http://cs.jhu.edu/~jason/tutorials/loglin/formulas.pdf

def phi(n_i, e, z):    
    '''One feature needs to be the PMI of n_i'''

    f1 = not n_i[0].isupper() and z == 0
    f2 = not n_i[0].lower() in e.lower() and z == 0
    
    f3 = n_i[0].isupper() and n_i.lower() in e.lower() and z == 1
    f4 = n_i[0].isupper() and z == 1

    return np.asarray([f1, f2, f3, f4], dtype=np.double)


def predict_Y_for_point(dno, w, feats):
    '''returns a distribution over the Y labels'''
    numerators = np.exp(feats[dno].dot(w))
    D = np.sum(numerators)
    probs = numerators / D
    return probs.reshape(len(numerators),1)
    

def get_expected_feats_for_point(dno, w, feats):
    return np.sum(predict_Y_for_point(dno, w=w, feats=feats) * feats[dno], axis=0)


def get_expected_feats_for_dataset(dataset, w, feats):
    return np.sum(np.vstack([get_expected_feats_for_point(dno, w, feats) for dno in range(len(dataset))]), axis=0)


def fprime(w, *args):
    dataset, Y, feats, actual_feats, true_feature_counts = args    
    expected_feature_counts = get_expected_feats_for_dataset(dataset, w, feats)
    delta = true_feature_counts - expected_feature_counts
    return -1 * delta


def make_feats(dataset):
    Y = set([_[0] for _ in dataset])

    feats = np.zeros((len(dataset), len(Y), len(w)))

    for ino, p in enumerate(dataset):
        ni, e, z = p
        for yno, y in enumerate(Y):
            feats[ino][yno] = phi(y, e, z)

    return feats


def get_probs(w, *args):
    dataset, Y, feats, actual_feats = args
    n = np.exp(actual_feats.dot(w))
    
    d = 0
    for yno, y in enumerate(Y):
        d += np.exp(feats[:,yno].dot(w))
    return n/d


def get_log_probs(w, *args):
    '''Big F in Eisners notation'''
    
    dataset, Y, feats, actual_feats, true_feature_counts = args
    
    n = np.exp(actual_feats.dot(w))
    
    d = 0
    for yno, y in enumerate(Y):
        d += np.exp(feats[:,yno].dot(w))

    return -1 * np.sum(np.log(n/d))


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


d0 = [("Ari", "Ariana", 0), 
      ("bill", "Ariana", 0), 
      ("bill", "Rihanna", 0),
      ("Riri", "Rihanna", 0),
      ("sand", "Ariana", 0)]


d1 = [("Ari", "Ariana", 1),  
      ("bill", "Ariana", 1), 
      ("bill", "Rihanna", 1),
      ("Riri", "Rihanna", 1),
      ("sand", "Ariana", 1)]

w = np.asarray([.2, .14, .32, .3])

feats, actual_feats = make_all_feats(d1)

true_feature_counts = np.sum(actual_feats, axis=0)

Y = set([_[0] for _ in dataset])

print(np.exp(get_log_probs(w, dataset, Y, feats, actual_feats, true_feature_counts)))

w, f, d = fmin_l_bfgs_b(func=get_log_probs, fprime=fprime, x0=w, args=(dataset, Y, feats, actual_feats, true_feature_counts))

print(np.exp(get_log_probs(w, dataset, Y, feats, actual_feats, true_feature_counts)))

get_probs(w, dataset, Y, feats, actual_feats)
