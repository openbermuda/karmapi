""" Teapot
teapot == tpot 

hpat == tpot + covo

path+ == hpat

mastermind
"""
import numpy as np

# tea
class TeaPlot:

    def __init__(self,
                 A=None, B=None, P0=None):
        
        self.A = A
        self.B = B
        self.P0 = P0
        self.ALPHA = None
        self.BETA = None
        self.GAMMA = None
        self.SCALE = None

        # beer
        self.R_A = None
        self.R_B = None
        self.R_P0 = None
        self.R_ALPHA = None
        self.R_BETA = None
        self.R_GAMMA = None


        # ingredients
        self.OBSERVATIONS = None

    def alpha(self):
        """ Alpha pass

        observations: array with observations at time t=0,1, .. T
        
        A: state transition matrix. n x n, n = number of states

        B: prob of observation given hidden state, n * k, 
           k = size of observation space.

        p0: initial probability of each state.

        another turning point..
       
        fork in the road...

        time will show the way.
        """

        observations = self.OBSERVATIONS
        
        T = len(observations)
        A = self.A
        B = self.B
        P0 = self.P0

        n = A.shape[0]
        k = B.shape[1]

        alpha = np.zeros(shape=(T, n))
        scale = np.zeros(T)

        # calculate alpha[0]
        alpha[0] = P0 * B[observations[0]]
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
        self.ALPHA = alpha
        self.SCALE = scale

        self.SCORE = sum(np.log(scale))

    def beta(self):
        """ Beta pass
        
        observations: array with observations at time t=0,1, .. T
        
        A: state transition matrix. n x n, n = number of states

        B: prob of observation given hidden state, n * k, 
           k = size of observation space.

        scale: scaling factors from alpha pass

        it is something unpredictable ...
        """
        observations = self.OBSERVATIONS
        scale = self.SCALE
        A = self.A
        B = self.B
        
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
        self.BETA = beta


    def gamma(self):
        """ Gamma pass 

        but in the end is right..
        """
        self.GAMMA = self.ALPHA * self.BETA

    def bm_rest(self):
        """ Re-estimate B matrix """
        
        # spin through observations to re-estimate B
        B = self.B 
        bdash = np.zeros(shape=B.shape)

        for obs, gam in zip(self.OBSERVATIONS, self.GAMMA):
            bdash[obs, :] += gam

        nstates = B.shape[1]
        
        for i in range(nstates):
            bdash[:, i] /= sum(self.GAMMA[:, i])

        self.R_B = bdash

    def p0_rest(self):
        """ Re-estimate initial state probabilities """
        self.R_P0 = self.GAMMA[0] / sum(self.GAMMA[0])

    def am_rest(self):
        """ Re-estimate A matrix. """
        A = self.A
        B = self.B
        ALPHA = self.ALPHA
        BETA = self.BETA
        SCALE = self.SCALE
        
        ksi = np.zeros(shape=A.shape)
        T = ALPHA.shape[0]
        n = A.shape[0]
        
        for t in range(1, T):
            obs = self.OBSERVATIONS[t]
            totweight = 0.
            weights = np.zeros(shape=A.shape)

            for i in range(n):
                for j in range(n):
                    # alpha[t] = (alpha[t-1] @ A) * B[o]
                    weight = ALPHA[t-1, i] * A[i, j] * BETA[t, j] * B[obs, j] / SCALE[n]
                    totweight += weight
                    weights[i, j] += weight

            weights /= totweight
            ksi += weights

        # do some gymnastics to scale ksi
        ksi = (ksi.T / ksi.T.sum(0)).T

        # Save the re-estimate
        self.R_A = ksi


    def fill(self, parms):
        """ Fill the teapot from parms

        parms: a dictionary of goodies.
        """
        self.A = parms.get('a')
        self.B = parms.get('b')
        self.P0 = parms.get('p0')

        self.OBSERVATIONS = parms.get('observations')

        self.ALPHA = parms.get('alpha')
        self.BETA = parms.get('beta')
        self.GAMMA = parms.get('gamma')
        self.ALPHA = parms.get('alpha')


    def brew(self):
        """ Brew some T """
        self.alpha()
        self.beta()
        self.gamma()
        
    def beer(self):
        """ RE-Estimate B matrix

        beer = reverse(reeb)

        Since we are in Bermuda, ginger beer perhaps.

        I hope you have the time of your life...
        """
        self.bm_rest()
        self.am_rest()
        self.p0_rest()

    def stir(self):

        self.A = self.R_A
        self.B = self.R_B
        self.P0 = self.R_P0

    def stew(self, iters = 100, epsilon=.01):

        xscore = None
        for iter in range(iters):
            self.brew()
            self.beer()
            self.stir()
            print(f'SCORE {self.SCORE}')
            # check in case we seem to have converged
            if xscore is not None:
                delta = self.SCORE - xscore
                if delta < epsilon:
                    break
            
            xscore = self.SCORE


    def ferment():
        pass



