from auxilliary import BuildTree, UCB
import numpy as np
from numpy.random import binomial, choice
from joblib import Parallel, delayed, parallel_backend
import multiprocessing

#POMCP solver
class POMCP():
    # gamma = discount rate
    # c = higher value to encourage UCB exploration
    # threshold = threshold below which discount is too little
    # timeout = number of runs from node
    def __init__(self, generator, gamma = 0.95, c = 1, threshold = 0.005, timeout = 10000, no_particles = 1200):
        self.gamma = gamma 
        if gamma >= 1:
            raise ValueError("gamma should be less than 1.")
        self.Generator = generator
        self.e = threshold
        self.c = c
        self.timeout = timeout
        self.no_particles = no_particles
        self.tree = BuildTree() 
        
    # give state, action, and observation space
    def initialize(self, S , A, O):
        self.states = S
        self.actions = A
        self.observations = O

    # searchBest action to take
    # UseUCB = False to pick best value at end of Search()
    def SearchBest(self, h, UseUCB = True):
        max_value = None
        result = None
        resulta = None
        if UseUCB:
            if self.tree.nodes[h][4] != -1:
                children = self.tree.nodes[h][1]
                # UCB for each child node
                for action, child in children.items():
                    # if node is unvisited return it
                    if self.tree.nodes[child][2] == 0:
                        return action, child
                    ucb = UCB(self.tree.nodes[-1][2], self.tree.nodes[child][2], 
                    self.tree.nodes[child][3], self.c)
            
                    # Max is kept 
                    if max_value is None or max_value < ucb:
                        max_value = ucb
                        result = child
                        resulta = action
            #return action-child_id values
            return resulta, result
        else:
            if self.tree.nodes[h][4] != -1: 
                children = self.tree.nodes[h][1]
                # pick optimal value node for termination
                for action, child in children.items():
                    node_value = self.tree.nodes[child][3]
                    # keep max
                    if max_value is None or max_value < node_value:
                        max_value = node_value
                        result = child
                        resulta = action
            return resulta, result

    # Search module
    def Search(self):
        Bh = self.tree.nodes[-1][4].copy()
        # Repeat Simulations until timeout
        for _ in range(self.timeout):
            if Bh == []:
                s = choice(self.states)
            else:
                s = choice(Bh)
            self.Simulate(s, -1, 0)
        # Get best action
        action, _ = self.SearchBest(-1, UseUCB = False)
        return action

    # Check if a given observation node has been visited
    def getObservationNode(self,h,sample_observation):
        
        if sample_observation not in list(self.tree.nodes[h][1].keys()):
            # If not create the node
            self.tree.ExpandTreeFrom(h, sample_observation)
        # Get the nodes index
        Next_node = self.tree.nodes[h][1][sample_observation]
        return Next_node

    def Rollout(self, s, depth):

        # Check significance of update
        if (self.gamma**depth < self.e or self.gamma == 0 ) and depth != 0:
            return 0
        
        cum_reward = 0
        
        # Pick random action; maybe change this later
        # Need to also add observation in history if this is changed
        action = choice(self.actions)
        
        # Generate states and observations
        sample_state, _, r = self.Generator(s,action)
        cum_reward += r + self.gamma*self.Rollout(sample_state, depth + 1)
        return cum_reward

    def Simulate(self, s, h, depth):

        # Check significance of update
        if (self.gamma**depth < self.e or self.gamma == 0 ) and depth != 0:
            return 0

        # If leaf node
        if self.tree.isLeafNode(h):
            for action in self.actions:
                self.tree.ExpandTreeFrom(h, action, IsAction=True)
            new_value = self.Rollout(s,depth)
            self.tree.nodes[h][2] += 1
            self.tree.nodes[h][3] = new_value
            return new_value
        
        cum_reward = 0
        # Searches best action
        next_action, next_node = self.SearchBest(h)
        # Generate next states etc.. 
        sample_state, sample_observation, reward = self.Generator(s, next_action)
        # Get resulting node index
        Next_node = self.getObservationNode(next_node,sample_observation)
        # Estimate node Value
        cum_reward += reward + self.gamma*self.Simulate(sample_state, Next_node, depth + 1)
        # Backtrack
        self.tree.nodes[h][4].append(s)
        if len(self.tree.nodes[h][4]) > self.no_particles:
            self.tree.nodes[h][4] = self.tree.nodes[h][4][1:]
        self.tree.nodes[h][2] += 1
        self.tree.nodes[next_node][2] += 1
        self.tree.nodes[next_node][3] += (cum_reward - self.tree.nodes[next_node][3])/self.tree.nodes[next_node][2]
        return cum_reward

    # FIXFIXFIX
    # Samples from posterior after action and observation
    def PosteriorSample(self, Bh, action, observation):
        if Bh == []:
            s = choice(self.states)
        else:
            s = choice(Bh)
        #Sample from transition distribution
        s_next, o_next, _ = self.Generator(s,action)
        if o_next == observation:
            return s_next
        result = self.PosteriorSample(Bh,action,observation)
        return result
   
    # Updates belief by sampling posterior
    def UpdateBelief(self, action, observation):
        prior = self.tree.nodes[-1][4].copy()
        
        self.tree.nodes[-1][4] = []
        for _ in range(self.no_particles):
            self.tree.nodes[-1][4].append(self.PosteriorSample(prior, action, observation))