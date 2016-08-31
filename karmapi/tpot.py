""" Teapot
teapot == tpot 

hpat == tpot + covo

path+ == hpat

mastermind
"""
import numpy as np

# tea
A = None
B = None
P0 = None
ALPHA = None
BETA = None
GAMMA = None
SCALE = None

# beer
R_A = None
R_B = None
R_P0 = None
R_ALPHA = None
R_BETA = None
R_GAMMA = None


# ingredients
OBSERVATIONS = None

def alpha():
    """ Alpha pass

    observations: array with observations at time t=0,1, .. T
    
    A: state transition matrix. n x n, n = number of states

    B: prob of observation given hidden state, n * k, 
       k = size of observation space.

    p0: initial probability of each state.
    """

    observations = OBSERVATIONS
    
    T = len(OBSERVATIONS)

    n = A.shape[0]
    k = B.shape[1]

    alpha = np.zeros(shape=(T, n))
    scale = np.zeros(T)

    # calculate alpha[0]
    alpha[0] = p0 * B[observations[0]]
    scale[0] = sum(alpha[0])
    alpha[0] /= scale[0]

    # spin through the remaining observations
    for t in range(1, T):
        o = observations[t]
        alpha[t] = (alpha[t-1] @ A) * B[o]
        
        # normalise
        scale[t] = sum(alpha[t])
        alpha[t] /= scale[t]

    # Save results for later passes
    global ALPHA, SCALE, SCORE
    ALPHA = alpha
    SCALE = scale

    SCORE = sum(np.log(scale))

def beta():
    """ Beta pass
    
    observations: array with observations at time t=0,1, .. T
    
    A: state transition matrix. n x n, n = number of states

    B: prob of observation given hidden state, n * k, 
       k = size of observation space.

    scale: scaling factors from alpha pass
    """
    observations = OBSERVATIONS
    scale = SCALE
    
    T = len(observations)

    n = A.shape[0]
    k = B.shape[1]

    beta = np.zeros(shape=(T, n))

    # Beta[T-1] uniformly set to 1.0
    beta[T-1] = 1

    # spin through the remaining observations
    for t in range(T-2, -1, -1):
        o = observations[t+1]

        beta[t] = (beta[t+1] * B[o]) @ A.T
        
        # normalise
        beta[t] /= scale[t+1]

    # save beta pass results
    global BETA
    BETA = beta


def gamma():
    """ Gamma pass """
    global GAMMA

    GAMMA = ALPHA * BETA

def bm_rest():
    """ Re-estimate B matrix """
    
    # spin through observations to re-estimate B
    bdash = np.zeros(shape=B.shape)

    for obs, gam in zip(OBSERVATIONS, GAMMA):
        bdash[obs, :] += gam

    nstates = B.shape[1]
    
    for i in range(nstates):
        bdash[:, i] /= sum(GAMMA[:, i])

    global R_B

    R_B = bdash


def am_rest():
    pass

def p0_rest():
    """ Re-estimate initial state probabilities """
    global R_P0

    R_P0 = GAMMA[0] / sum(GAMMA[0])

def am_rest():
    """ Re-estimate A matrix. """
    
    ksi = np.zeros(shape=A.shape)
    T = alpha.shape[0]
    n = A.shape[0]
    
    for t in range(1, T):
        obs = OBSERVATIONS[t]
        totweight = 0.
        weights = np.zeros(shape=A.shape)

        for i in range(n):
            for j in range(n):
                # alpha[t] = (alpha[t-1] @ A) * B[o]
                weight = alpha[t-1, i] * A[i, j] * beta[t, j] * B[obs, j] / scale[n]
                totweight += weight
                weights[i, j] += weight

        weights /= totweight
        ksi += weights

    global R_A
    R_A = ksi


def fill(parms):
    """ Fill the teapot """
    global A, B, P0, ALPHA, BETA, GAMMA, OBSERVATIONS

    A = parms.a
    B = parms.b
    P0 = parms.p0
    ALPHA = parms.alpha 
    BETA = parms.beta
    GAMMA = parms.gamma
    ALPHA = parms.alpha


def brew():
    """ Brew some T """
    alpha()
    beta()
    gamma()
    
def beer():
    """ RE-Estimate B matrix

    beer = reverse(reeb)

    Since we are in Bermuda, ginger beer perhaps.
    """
    global R_B, R_A, R_P0
    R_B = bm_rest()
    R_A = am_rest()
    R_P0 = p0_rest()

def stir():

    global P0, A, B

    A = R_A
    B = R_B
    P0 = R_P0

def stew(iters = 100, epsilon=.01):

    xscore = None
    for iter in range(iters):
        brew()
        beer()
        stir()

        # check in case we seem to have converged
        if xscore is not None:
            delta = SCORE - xscore
            if delta < epsilon:
                break
        
        xscore = SCORE


def ferment():
    pass



