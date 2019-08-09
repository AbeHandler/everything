import numpy as np
from scipy.special import logsumexp
from tqdm import tqdm_notebook as tqdm


def init_pi(K):
    t = np.random.uniform(0,1,size=K)
    return t/np.sum(t)


def init_phi(K,V):
    alphas = np.ones(V)
    return np.random.dirichlet(alphas, size=K)


def init_lambda_d(N, K):

    lambda_d = np.random.rand(N, K)
    lambda_d /= np.sum(lambda_d,axis=1).reshape(N, 1)

    return lambda_d


def generate_data(N, K, V, real_pi, real_phi, C):
    D = np.zeros((N, V))
    ks = []
    for d in tqdm(range(N)):
        k = np.random.choice(K, 1, p=real_pi)[0]
        D[d] = np.random.multinomial(n=C, pvals=real_phi[k])
        ks.append(k)
    return D, ks


def normalize_log_probs(lps):
    N_, K_ = lps.shape
    p = np.exp(lps - np.max(lps,axis=1).reshape(N_,1))
    p = p/np.sum(p, axis=1).reshape(N_,1)
    assert np.sum(p, axis=1).all() == 1.0
    return p


def log_prob_D_given_k(D, pi_hat_, phi_hat_, k):
    '''
    log prob of the data, given k. i.e.
    
    log( p(x, z | \theta)) =  log( p(x | z, theta) * p(z | theta) )

                           = log(p(x | z, theta)) +  log(p(z | theta))+
                           
                           = \sum_V(p(x_v | z, theta) + log(p(z | theta))
    '''
    
    # sum across rows to get the log probability of all words in the instance under phi_hat[k]
    log_prob_of_words = np.sum(D * np.log(phi_hat_[k]), axis=1)
    log_prob_of_class = np.log(pi_hat_[k])
    out = log_prob_of_words + log_prob_of_class
    assert out.shape == (N,)
    return out.reshape(N,1)
    

def expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D):
    '''
    The first term in the ELBO \sum_z q(z) log p(x,z|\theta)
    '''

    sum_ = 0

    K = pi_hat.shape[0]

    for k in range(K):
        sum_ += np.sum(lambda_d[:,k].reshape(N,1) * log_prob_D_given_k(D, pi_hat, phi_hat, k=k))

    assert sum_ < 0
    return sum_


def entropy(q):
    return -1 *  np.sum(q * np.log(q))


def elbo(lambda_d, pi_hat, phi_hat, D):
    return expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D) + entropy(lambda_d)


def e_step(pi_hat_, phi_hat_, D, N, K):

    lambda_d_new = np.zeros((N, K), dtype=np.float64)
    for k in range(K):
        lambda_d_new[:,k] = np.sum((D  * np.log(phi_hat_[k])), axis=1).reshape(N,)

    lambda_d_new += np.log(pi_hat_)

    return normalize_log_probs(lambda_d_new)


def m_step_phi(lambda_d, K_, phi_hat, D):
    phi_hat_new = np.zeros_like(phi_hat)

    for k in range(K_):
        nk = np.sum(lambda_d[:,k].reshape(N, 1) * D, axis=0)
        nd = np.sum(nk)
        phi_hat_new[k] = nk/nd

    return phi_hat_new


def m_step_pi(lambda_d):
    assert round(np.sum(lambda_d), 8) == N # i.e. denom D
    n = np.sum(lambda_d,axis=0)
    return n/(np.sum(n))


def observed_data_LL(pi_hat, phi_hat, K, D):
    ## note this is the log of the prob of the data! not the sum of the logs 'cuz Jensens

    # \ell(theta)
    
    observedD = np.zeros((N,1), dtype='float64')

    for k in range(K):
        lp_xz = log_prob_D_given_k(D, pi_hat, phi_hat, k) # log prob of all of the data, given z=k
        p_xz = np.exp(lp_xz) # exponentiate to get out of log space 
        observedD += p_xz

    log_of_all_N_points = np.log(observedD) # now take the log of the sum over instances

    sum_of_n = np.sum(log_of_all_N_points)
    
    assert sum_of_n <= 0
    
    return sum_of_n


def kl(p, q):
    return np.sum(p * np.log(p/q))


def report_kl(real_phi, phi_hat, real_pi, pi_hat):
    # assuming you have enuf N, this should go down too.
    # if you dont have enuf points, there will be variance in the draw from the
    # true parameters
    kl_phi = kl(real_phi, phi_hat)
    kl_pi = kl(real_pi, pi_hat)
    return kl_pi + kl_phi


def run_iter(lambda_d, pi_hat, phi_hat, K, D, iter_no, real_pi, real_phi, verbose=False):
    this_observed_ll = observed_data_LL(pi_hat, phi_hat, K, D)

    #### e step
    b4 = expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D)
    lambda_d = e_step(pi_hat, phi_hat, D, N, K)
    aft = expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D)

    if not np.allclose(b4, aft, rtol=1e7):
        assert(b4 <= aft)

    #### m step

    b4 = expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D)
    pi_hat = m_step_pi(lambda_d)
    aft = expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D)

    if not np.allclose(b4, aft, rtol=1e10):
        assert(b4 <= aft)

    b4 = expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D)
    phi_hat = m_step_phi(lambda_d, K, phi_hat, D)
    aft = expected_complete_log_likelihood(lambda_d, pi_hat, phi_hat, D)

    if not np.allclose(b4, aft, rtol=1e10):
        assert(b4 <= aft)
    
    # BP: observed data LL should be less than 0
    assert observed_data_LL(pi_hat, phi_hat, K, D) < 0
    
    # BP: elbo should be below observed data LL
    if not np.allclose(elbo(lambda_d, pi_hat, phi_hat, D), observed_data_LL(pi_hat, phi_hat, K, D), rtol=1e10):
        assert elbo(lambda_d, pi_hat, phi_hat, D) <= observed_data_LL(pi_hat, phi_hat, K, D)
        
    next_observed_ll = observed_data_LL(pi_hat, phi_hat, K, D)
    
    assert next_observed_ll >= this_observed_ll
    
    if verbose:
        # BP: elbo should be climbing, observed data LL should be climbing
        # BP: do a graph
        klsum = report_kl(real_phi, phi_hat, real_pi, pi_hat)
        print(iter_no, elbo(lambda_d, pi_hat, phi_hat, D), observed_data_LL(pi_hat, phi_hat, K, D), klsum)
    
    return pi_hat, phi_hat, lambda_d


def run_em(N, K, V, C):
    real_pi = init_pi(K)
    real_phi = init_phi(K,V)

    D, ks = generate_data(N, K, V, real_pi, real_phi, C)

    phi_hat = init_phi(K, V)

    pi_hat = init_pi(K)

    lambda_d = init_lambda_d(N, K)

    for iter_no in range(10):
        pi_hat, phi_hat, lambda_d = run_iter(lambda_d, pi_hat, phi_hat, K, D, iter_no, real_pi, real_phi, verbose=True)

if __name__ == "__main__":
    N = 10000
    K = 19
    V = 30
    C = 4 # context size
    run_em(N, K, V, C)

