from auxilliary import BuildTree, UCB
import numpy as np
from numpy.random import binomial, choice
from toy_generator import Generator
from pomcp import POMCP
from timeit import default_timer as timer
from time import sleep
from joblib import Parallel, delayed, parallel_backend

S = [0,1]
A = [0,1]
O = [0,1]

# setup start
ab = POMCP(Generator,gamma = 0.5)
ab.initialize(S,A,O)

# Calculate policy in a loop
time = 0
while time <= 10:
    time += 1
    action = ab.Search()
    print(ab.tree.nodes[-1][:4])
    print(action)
    observation = choice(O)
    ab.tree.prune_after_action(action,observation)
    ab.UpdateBelief(action, observation)


