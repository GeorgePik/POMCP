import numpy as np
from auxilliary import BuildTree, UCB
import numpy as np
from numpy.random import binomial, choice, multinomial


S = [0,1]
A = [0,1]
O = [0,1]

# new_s, s, a
a = np.genfromtxt('Transition_Probabilities.csv', delimiter=',').reshape((2,2,2))
# obs, s, a
b = np.genfromtxt('Emission_Probabilities.csv', delimiter=',').reshape((2,2,2))

# s, a
r = np.genfromtxt('RewardTable.csv', delimiter=',').reshape((2,2))

# define a black box generator
def Generator(s,act):
    ss = multinomial(1, a[:,s,act])
    ss= int(np.nonzero(ss)[0])
    o = multinomial(1, b[:,ss,act])
    o= int(np.nonzero(o)[0])
    rw = r[s,act]
    return ss, o , rw
