# Lab 3: Policy Search

## Task

Write agents able to play [*Nim*](https://en.wikipedia.org/wiki/Nim), with an arbitrary number of rows and an upper bound $k$ on the number of objects that can be removed in a turn (a.k.a., *subtraction game*).

The player **taking the last object wins**.

* Task3.1: An agent using fixed rules based on *nim-sum* (i.e., an *expert system*)
* Task3.2: An agent using evolved rules
* Task3.3: An agent using minmax
* Task3.4: An agent using reinforcement learning

## Instructions

* Create the directory `lab3` inside the course repo 
* Put a `README.md` and your solution (all the files, code and auxiliary data if needed)

## Notes

* Working in group is not only allowed, but recommended (see: [Ubuntu](https://en.wikipedia.org/wiki/Ubuntu_philosophy) and [Cooperative Learning](https://files.eric.ed.gov/fulltext/EJ1096789.pdf)). Collaborations must be explicitly declared in the `README.md`.
* [Yanking](https://www.emacswiki.org/emacs/KillingAndYanking) from the internet is allowed, but sources must be explicitly declared in the `README.md`.

## Deadlines ([AoE](https://en.wikipedia.org/wiki/Anywhere_on_Earth))

* Sunday, December 4th for Task3.1 and Task3.2
* Sunday, December 11th for Task3.3 and Task3.4
* Sunday, December 18th for all reviews

## Task 3.1
### An agent using fixed rules based on *nim-sum* (i.e., an *expert system*)
this is the simplest of the tasks, we just need to implement the rules of the game and the agent will play accordingly. The obvious answer is to use nim-sum but we can also try some other tactics.
some examples of agents can be found in the file [opponents.py](https://github.com/lorenzobellino/Computational-Intelligence-2022/tree/main/lab3/opponents.py)

## Task 3.2
### An agent using evolved rules

My approach to this task can be seen in the file [nim_GA.py](https://github.com/lorenzobellino/Computational-Intelligence-2022/tree/main/lab3/nim_GA.py)

#### Core idea
The idea is to use a gnetic approach to evolve a genome that will be used to play the game. Given a population size of $N$, $N$ individuals are randomly generated. Starting from this individuals $O$ offspring are generated applyng some sort of mutation to the genome of the parent. The offspring are then evaluated and the best $N$ individuals are selected to be the parents of the next generation. This process is repeated until a certain number of generations is reached.
#### Genome and representation
At first I tried to use some simple rules such as *shortest-row* and *longest-row* and using a genome composed of two parameters: ```genome = {"p_rule": random.random(), "p_row": random.random()}```. The first parameter is used as a probability of using the first or the second rule, the second parameter is used as a percentage of the row to be removed. The problem with this approach is that the agent is not able to learn the best strategy, it just learns to play a bit better than the random agent.
Then i tried different parameters for different approaches such as ```genome = {"aggression": random.random(), "finisher": random.random()}``` where the first parameter is used to decide if the agent should play aggressively or not, the second parameter is used to decide if the agent should try to take all objects from a row or leave one object.
Ultimately all of my attempts failed and i decided to use a different approach, finally i came up with a genome inspired by the way of nim-sum is calculated.
the genome is composed of 4 parameters:
```python
genome = {
            "alpha": random.uniform(-10, 10),
            "beta": random.uniform(-10, 10),
            "gamma": random.uniform(-10, 10),
            "delta": random.uniform(-10, 10),
        }
```
each of this parameters is then used to calculate the score for a given board in the following way:
```python
res = (
            (a[0], abs(alpha * a[1] + beta * b[1] + gamma * c[1] + delta * d[1] + epsilon * e[1]))
            for a, b, c, d in zip(data["and"], data["or"], data["sum"], data["sub"])
        )
```
where ```data``` is a dictionary calculated in the function ```cook_status()```. Each key represent an operation calculated between the different rows of the board in the following way:
1. **sub** : subtraction between the rows
```python
def sub_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.sub)
    return result
```
2. **sum** : sum between the rows
```python
sum(state.rows)
```
3. **and** : and between the rows
```python
def and_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.and_)
    return result
```
4. **or** : or between the rows
```python
def or_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.or_)
    return result
```
Finally **res** is a generator where for each move given an initial state the score is calculated based on the parameters of the genome. The score is calculated as the absolute value of the sum of the parameters multiplied by the value of the operation between the rows of the board. The parameters are then used to calculate the score for each move and the move with the lowest score is chosen.

#### Mutations
The mutations are applied to the genome in the following way:
```python
for i in range(OFFSPRING):
        p = tournament(population)

        p[2]["alpha"] += random.gauss(0, 10 / (gen + 1))
        p[2]["beta"] += random.gauss(0, 10 / (gen + 1))
        p[2]["gamma"] += random.gauss(0, 10 / (gen + 1))
        p[2]["delta"] += random.gauss(0, 10 / (gen + 1))
        p[2]["epsilon"] += random.gauss(0, 10 / (gen + 1))

        strat = make_strategy(p[2])
```
for each offspring a parent **p** is selected using the tournament selection method. Then the parameters of the genome are mutated using a gaussian distribution with a standard deviation that decreases with the number of generations. Finally the strategy is created using the new genome.

#### Evaluations
In order to evaluate the performance of the agent i tested it agains four different opponents:
1. **optimal_strategy**: the optimal strategy for the game using nim-sum
2. **pure_random**: a random agent
3. **gabriele**: an agent that uses the same approach proposed by one of our colleagues
4. **take_one_never_finish**: an agent that takes one object from a random row, if it can it will never remove the last object from a row

Each opponent is played for a fixed number of matches **NUM_MATCHES** and the number of victory with each component is saved in a tuple.
```python
eval = (
        evaluate(strat, opponents.optimal_startegy),
        evaluate(strat, opponents.pure_random),
        evaluate(strat, opponents.gabriele),
        evaluate(strat, opponents.take_one_never_finish),
        )
```

#### Results and minor tweaks
Using this apprach it is possible to evolve a genome able to beat all the opponents consistently, except for nim-sum where it reaches a win rate of roughly $52%$.
It is important to notes that this result is only reachable in a reasonable amount of time for boards with a fixed size that is not too big. In my case i calculated the best genome for a board with 5 rows:
```python
genome = {
        "alpha": 12.812770589035535,
        "beta": -16.051123920350758,
        "gamma": -0.20956437443764508,
        "delta": -8.234717910949916,
    }
```
I tried to calculate a similar genome but for a generic board size but it was not possible to reach the same result in a reasonable amount of time. 
The best i could do was an agent with a win rate of $1.5%$ against nim-sum. The genome for this agent is:
```python
genome = {
        "alpha": 15.945309194204931,
        "beta": -3.2707966609771746,
        "gamma": -25.708257470959275,
        "delta": 14.81947128092396,
    }
```

I tried also an approach with five parameters, with the fifth one used in the formula above as a constant multiplied by the result of an other function, in particular the nand operation between rows:
```python
def nand_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, lambda x, y: ~(x & y))
    return result
```

The agent with a five parameters genome was able to beat nim-sum with a win rate of $62%$ for a fixed board size of 5 rows. The genome for this agent is:
```python
genome = {
        "alpha": -42.5399485484396,
        "beta": 114.60961375796023,
        "gamma": -52.64808867035252,
        "delta": 0.49668038593870456,
        "epsilon": 18.15686871650329,
    }
```
But the result for a random sized board were similar to the one with four parameters.

All of my previews attempt can be found [here](https://github.com/lorenzobellino/Computational-Intelligence-2022/tree/main/test-examples-challenges/lab3/) and my optimal palyers [here](https://github.com/lorenzobellino/Computational-Intelligence-2022/tree/main/lab3/best_player.py)

## Task 3.3
### An agent using minmax

The minmax algorithm is a recursive algorithm that is used to find the best move for a player in a two player game. It is based on the assumption that the opponent will play in the best way possible. The algorith is implemented in the function ```minmax()``` [here](https://github.com/lorenzobellino/Computational-Intelligence-2022/tree/main/lab3/minmax.py)
In order too speed up the process of recursion i decided to use a cache to store the results of the function ```minmax()``` for each state. The cache is implemented as a dictionary where the key is a tuple of (state,player) and the value is a boolean value to represent the outcome of the game starting from that state for the player zero.
An other aspect of the algorith used to speed up the process is the use of alpha-beta pruning. Here is used to prune the branches of the tree that are not useful for the calculation of the best move. 
If the player is minimizing means that given a state if there is a move that leads to a loss for the maximising player we don't need to check the other moves because the minimising player will choose the move that leads to the loss. a similar approach is used for the maximising player.

My full algorithm implementation can be found [here](https://github.com/lorenzobellino/Computational-Intelligence-2022/tree/main/lab3/minmax.py)

## Task 3.3
### An agent using reinforcement learning