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