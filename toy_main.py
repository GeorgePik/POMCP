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

ab = POMCP(Generator,timeout = 10000, gamma= 0.8)
ab.initialize(S,A,O)
print('PARALLEL')
start = timer()
print(ab.Search(-1))
end = timer()
print('Simulation:',end-start)

# print(ab.tree.nodes[-1])

start = timer()
ab.tree.prune_after_action(1,1)
end = timer()
print('Prune:',end-start)
# print(ab.tree.nodes[-1][4])

start = timer()
ab.UpdateBelief(1,1)
end = timer()
print('Update Time:',end-start)
# print(ab.tree.nodes[-1])
# print(ab.tree.nodes[-1][4])




