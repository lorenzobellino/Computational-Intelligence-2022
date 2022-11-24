# Adversarial Search
we have somthing that is playing agains us.
this creates a mindset where i am able to solve a problem much better.
an example is **games**, a lot of research has been done about this topic because they are really good model for real-world scenarios.
The goal of adversarial search is to find an **optimal policy** which is a set of rules that defines the behaviour in different scenarios

## Taxonomy
- **deterministic** vs **probabilistic**
- **perfect information** vs **imperfect information**
- **zero-sum** vs **non-zero-sum**
- **Turn-based** vs **real-time**

Chess --> turn-based zero-sum deterministic perfect information
Poker --> turn-based zero-sum probabilistic imperfect information
Nuclear war --> real-time non-zero-sum probabilistic imperfect information

in a game we do not know how the opponent will play -> the algorithm would have to give us a policy or strategy 

## Deterministic games
- **player**
- **state**
    - **terminal state** 
    - **terminal utility**
- **action**
    - **transition function** -> move from one state to an other

we might want to represent our game with a **tree** where each node is a state and each edge is an action

### Minimax
minimize the loss in the worst case scenario (studied a lot in economics)
we have two player with perfect information in a game that is fully deterministic.
what is my best move considering my opponent will respond with their best move that will minimize my reward?

It is complete only if the tree is finite.
It is optimal against an optimal opponent
Complexity:
- time: $O(b^m)$ -> branching factor $b$ and depth $m$
- space: $O(bm)$ -> branching factor $b$ and depth $m$

#### Alpha-Beta pruning
is done to decrease the search space.
if you have an idea that is surely bad, ron't waste time to see how truly awfull it really is.
we can prune the tree by not exploring the branches that are surely worse than the best move we have found so far.

### Limith depth
- **hard cutoff** -> we stop the search at a certain depth
- **horizon effect** -> incorrectly estimate the value of a state by overlooking an event that is just beyond the depth limit
    - *negativre horizon effect* -> delay an unavoidable conesquences
    - *positive horizon effect* -> overestimate some mooves, behaviou is too greedy
#### Quiescence search
increae depth when evaluating volatile positions, but how can **volatile** and **quiet** positions be discriminated?
we have to be able to understand when is needed to increase the depth of the search.

### Other tecniques
1. **hash table** -> store the value of a state so that it can be reused
2. **forward pruning** -> if a state is already evaluated, we can prune the branch, avoid considering all possible moves. How likely is that a remaining move is better than the current best moves?
3. **lookup table** -> store opening moves and endgames

## Evaluation
### Heuristic evaluation
often we are not able to search until a terminal state so we need some sort of heuristic in order to come up with a way to evaluate a state. DeepBlue used 8K feature to avaluate a state.
this is still better than nothing ab it works really well because of the amount of calculation that is done so high that it doesn't matter if the heuristic is not 100% precise.
Some of the evaluated features can be also self adapted by the algorithm.
### Machine learning
the value of a position might be learned using ML techniques.

# Chess and AI
..

# Stochastic games
how can we introduce dice throwing inside the game tree?
how to introduce uncertainty in the game tree?

we can add a layer in minmax in order to add uncertainty to the tree
## Stochastic MinMax
we have to minimize the expected reward -> the reward could be a weighted sum of the possible outcomes or maybe the reward should always be considered as the lowest possible value

## imperfect information
how i can handle a game where i do not have all the informations?
we can treat uncertainty as randomness

## stochastic SEARCH
1. **deep minmax** -> can be unfeasable
2. **monte Carlo simulation** -> applyed to random games

## monte carlo tree search
usefull in stochastic games but also in deterministic games
having a minmax approach and at some point we stop the exaustive minmax and we start sampling and then backpropagate the information found during the sampling.

# non zero sum games
prisoner's dilemma

# rule based systems

# learning classifier systems
rule based system that are learning the rules. it's not very used today but it had a preatty significant role in the past.
there is an incredible link between LCS and reinforcement learning.
we have a finite population of classifier (ruleset) as bitstrings. we also have a discovery component that is able to discover new rules and enhancing existing ones. in the end we need a preformance component or better a reinforcement component that is abel to assign some fitness to the ruleset.
## michigan style
OG style of LCS studied by holand
## pittsburg style
*Offline* learning -> evalutate all the systme inside the GA itself

# LCS rules
should work collaboratively
the set of rules should cover all the important situations -> **coverage** is a very important issue
only rules responsible for choosen decision should be rewarded/penalized
lazy and inactive rules should be removed
