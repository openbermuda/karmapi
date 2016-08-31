""" Teapot
teapot == tpot 

hpat == tpot + covo

path+ == hpat

mastermind
"""

# tea
A = None
B = None
P0 = None
ALPHA = None
BETA = None
GAMMA = None

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
    pass

def beta():
    pass

def gamma():
    pass


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
    global SCORE
    
    alpha()
    beta()
    SCORE = gamma()
    
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

def stew():
    pass

def ferment():
    pass
