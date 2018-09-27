import numpy as np
from auxilliary import BuildTree, UCB
from numpy.random import binomial, choice

# Generate data and store as csv

S = [0,1]
A = [0,1]
O = [0,1]

# Test transition probabilities
# New state, state, action
a = np.zeros((2,2,2))
a[0,0,0] = 0.9
a[1,0,0] = 0.1
a[0,1,0] = 0.35
a[1,1,0] = 0.65
a[0,0,1] = 0.4
a[1,0,1] = 0.6
a[0,1,1] = 0.8
a[1,1,1] = 0.2

np.savetxt("Transition_Probabilities.csv", a.flatten(), delimiter=",")

# Obser, state, action
# Test emission probabilities
b = np.zeros((2,2,2))
b[0,0,0] = 0.8
b[1,0,0] = 0.2
b[0,1,0] = 0.3
b[1,1,0] = 0.7
b[0,0,1] = 0.4
b[1,0,1] = 0.6
b[0,1,1] = 0.5
b[1,1,1] = 0.5


np.savetxt("Emission_Probabilities.csv", b.flatten(), delimiter=",")

#rewards
# s,action
r = np.zeros((2,2))
r[0,0] = 1
r[0,1] = 50
r[1,0] = 1
r[1,1] = 2

np.savetxt("RewardTable.csv", r.flatten(), delimiter=",")
