<h1 style= "color: rgb(39, 147, 221)"> README </h1>

## Description
This project contains code for a general purpose Partially Observable Monte Carlo Tree Search algorithm taken from [1]. This is an online POMDP solver, *ie* it approximates the optimal policy one action at a time. 

## Documentation

<div style= "font-size: 140% ;color: rgb(39, 147, 221)"> auxilliary.py </div>

Contains some helpful functions and a class to help construct and manipulate the tree of agent beliefs.

The way we implemented the tree is through the BuildTree() class. Each node in the tree is associated with a list of five elements. These are:
1. The key of its parent node
2. A dictionary whose keys are either action or observation indices and its values are the key of some child node. This holds all the child nodes at each node. For example, say taking the index 1 action from the current node leads us to the key 253 node. Then there will be an entry {1:253} in this dictionary.
3. The number of times a simulation visited this node.
4. The current estimate of the nodes value (kept as a running average of simulation values)
5. The list of particles associated with the node; A list of all states that were sampled at this node at some simulation.

The association is implemented with a Python dictionary. Each node has a unique key which can be used to access its values. The root node always has -1 as key. 

<div style= "color: rgb(247, 247, 158)"> UCB()</div>

Calculates UCB score.

Input:
1. N (int): Total number of simulations (from root).
2. n (int): Total number of simulations through current node.
3. V (float): Running average.
4. c (float): Controls importance of exploration in score.

Outputs:
1. (float): UCB score for node.

<div style= "color: rgb(247, 247, 158)"> powerset()</div>

Returns the powerset of a given list. (Taken from itertools recipes)

Input:
1. iterable (list): 

Outputs:
1. (iterable): powerset of input

<div style= "font-size: 120% ;color: rgb( 31, 232, 187 )"> BuildTree()</div>


<div style= "color: rgb(247, 247, 158)"> __init__()</div>

1. **giveParameters** (list): A list of necessary information for root node. Default is ['isRoot',{},0,0,[]]

Sets the following attributes:

1. self.nodes (dictionary): Stores the tree.

<div style= "color: rgb(247, 247, 158)"> ExpandTreeFrom()</div>
Expands the tree from a given *parent* node. It adds a new node and informs its parent.

Input:
1. parent (int): index of node from which the tree is expanded.
2. index (int): index of action or observation.
3. IsAction (Boolean): If expansion of tree is due to action or observation. Default **False**.

Outputs:
1. None; updates the tree

<div style= "color: rgb(247, 247, 158)"> isLeafNode()</div>

Checks if a given key corresponds to a leaf node.

Input:
1. n (int): key of node in questions.

Outputs:
1. (Boolean): If the given key corresponds to a leaf node.

<div style= "color: rgb(247, 247, 158)"> getObservationNode()</div>

Taken a generated observation *o* and the key of the current node (say *ha*), this will either return the key of the resulting node *hao* or it will create this node and return its key (if it does not exist).

Input:
1. h (int): key of current node.
2. sample_observation (int): Index of sampled observation.

Outputs:
1. (int): key for resulting node in current tree.

<div style= "color: rgb(247, 247, 158)"> prune()</div>

Removes input node from tree and calls itself on all of its children.

Input:
1. node (int): key of node from which pruning starts.

Outputs:
1. None; updates tree.

<div style= "color: rgb(247, 247, 158)"> make_new_root()</div>

Sets an input node as the new root.

Input:
1. node (int): key of node from which pruning starts.

Outputs:
1. None; updates tree.

<div style= "color: rgb(247, 247, 158)"> prune_after_action()</div>

After an input action is taken and an input observation occurs, sets the new root and prunes redundant branches of the old tree. 

Input:
1. action (int): index of action taken.
2. observation (int): index of observation that occured.

Outputs:
1. None; updates tree.

<div style= "font-size: 140% ;color: rgb(39, 147, 221)"> POMCP.py </div>

Contains the POMCP class.

<div style= "font-size: 120% ;color: rgb( 31, 232, 187 )"> POMCP()</div>


<div style= "color: rgb(247, 247, 158)"> __init__()</div>

1. **Generator** (function): Specifies a function to be used as a blackbox generator for the underlying POMDP dynamics. This will be called during simulations and should take as arguments the indices of a state and an action in the underlying state and action spaces.
2. **gamma** (float): The discounting factor for cost calculation. Should be <1. Default value is 0.95.
3. **e** (float): Threshold value below which the expected sum of discounted rewards for the POMDP is considered 0. Default value is 0.005.
4. **c** (float): Parameter that controls the importance of exploration in the UCB heuristic. Default value is 1.
5. **timeout** (int): Controls the number of simulations that will be run from the current root at each call of **Search()**. Default value is 10000.
6. **no_particles** (int): Controls the maximum number of particles that will be kept at each node and the number of particles that will be sampled from the posterior belief after an action is taken. Default value is 1200.
7. **Parallel** (Boolean): Controls if posterior belief is sampled with multiple threads. Default value is **False**. Tested only on Ubuntu.


<div style= "color: rgb(247, 247, 158)"> initialize()</div>

Input:
1. S (list): State space indices
2. A (list): Action space indices
3. O (list): Observation space indices

Initializes some internal variables.

<div style= "color: rgb(247, 247, 158)"> SearchBest()</div>

Finds the best action to take at a node according to some given metric (UCB or Value).

Input:
1. h (int): Current node.
2. UseUCB (Boolean): Whether to use UCB as metric or simply node value. Default **True**.

Outputs:
1. (int): Action index with highest score (UCB  or value)
2. (int): key for resulting node in current tree.

<div style= "color: rgb(247, 247, 158)"> Search()</div>

Runs *timeout* number of simulations from current root and outputs the index of the best action to take according to estimated values.

Outputs:
1. (int): Action index with highest value.


<div style= "color: rgb(247, 247, 158)"> getObservationNode()</div>

Taken a generated observation *o* and the key of the current node (say *ha*), this will either return the key of the resulting node *hao* or it will create this node and return its key (if it does not exist).

Input:
1. h (int): key of current node.
2. sample_observation (int): Index of sampled observation.

Outputs:
1. (int): key for resulting node in current tree.

<div style= "color: rgb(247, 247, 158)"> Rollout()</div>

Runs *Rollout* as specified in [1].

Input:
1. h (int): key of current node.
2. depth (int): Current depth of tree; Important for recursion. When called set *depth = 0*

Outputs:
1. (float): Estimate of input node value.

<div style= "color: rgb(247, 247, 158)"> Simulate()</div>

Runs *Simulate* as specified in [1].

Input:
1. s (int): Index of sample initial state.
2. h (int): key of current node.
3. depth (int): Current depth of tree; Important for recursion. When called set *depth = 0*

Outputs:
1. (float): Estimate of root node value.
(it affects values in the entire tree)


<div style= "color: rgb(247, 247, 158)"> PosteriorSample()</div>

Samples from the posterior belief. Start by sampling a state from prior belief, then sampling a subsequent state from the transition probability distribution and an observation from the emission probability distribution until the sampled observation matches the real observation. 

Input:
1. Bh (list): List of (prior) particles.
2. action (int): index of action taken.
3. observation (int): index of observation that occured.

Outputs:
1. (int): index of sampled state (from posterior belief)

<div style= "color: rgb(247, 247, 158)"> UpdateBelief()</div>
Updates particles of new root node after an action is taken and an observation occurs. 

Input:
1. action (int): index of action taken.
2. observation (int): index of observation that occured.

Outputs:
1. None; updates *Bh* element of new root node (with *no_particles* samples from the posterior belief)



## Bibliography
[1] Silver, David, and Joel Veness. "Monte-Carlo planning in large
POMDPs." Advances in Neural Information Processing Systems
23 (NIPS) (2010).