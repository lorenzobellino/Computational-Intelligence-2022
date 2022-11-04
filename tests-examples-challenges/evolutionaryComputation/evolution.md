# Evolutionary Computation
If you have any other oprions is better to not implement evoutionary algorithm. Autograd or gradiant descent are always a better approach.

## Practical application 
### wings design
research was made in order to apply evolutionary computation to design a better design for the wings of a plane.
It was demontrated that the result obtained were very good and coul be very easily adapted to some changes in the system such as a different angles of incidence with the air.
### Pipes desing
..

## Evolution strategies
1. parameter optimization
2. wings
3. $90^{\circ}$ pipe bends
4. $180^{\circ}$ pipe bends
5. bionics

One of the great thig about evolutionary computation is creating new solution starting from 2 possible solutions. but the original strategies for evolution didn't includes recombination. the modern approach does.
$(\mu/\rho,\lambda)$ VS $(\mu/\rho + \lambda)$

An other foundamental caracteristic of ES is different survival rates between individual -> importance of fittness, different individual have differente chance of survival.
every changes in the individual brigs some advantages or some disadvantages.

# Evolutionary Programming

designed by Lawrence Fogel. It is a possible starting point for evolutionary computation.
The objective is try to think about what intelligence is and trying to replicates it. Intelligence is the ability to foresee a problem, if i can create a machine that is able to fresee the problem and act corrispondly i created an intelligent machine.
He tried to do this by using a Finate State Machine (FSM) (Mealy vs Moore machines) creating a mechanism able to evolve a machine.
the method:
- No parent selection
- No recombination (one point in the search space stands for a species not an individual and there can not be crossover between species)
- Mutation
    -   add state, remove state
    - change transition, change initial state
    - change output
- survival selection
    - similar $(\mu + \mu)$ -> you have $\mu$ parents, generate $\mu$ children
    - q random matches between $\mu + \mu$ possible solutions, the $\mu$ best survive
    - selective pressure : $f(q)$, usually $q = 10$ -> $q$ = number of matches every individual has to fight in order to recieve a fitness score. Changing the value for $q$ you can cahnge the random variace between possible choices, if there is a hig selective pressure only the fittest can generate offspring, if there is a low selective pressure everyone has the same chance at generating an offspring
- stopping condition
    - steady state
- no elitism
    - no way to keep the best individual

## Evolutionary Programming Today
is a mix with Evolutionary strategies


## Terminology
- **Individual** : is a possible solution that can be evaluated
- **Chrormosome** : sequence of elements (gene)
- **Gene** : atomic unic handled by the genetic operations
- **Genome** : sequence of genes that you can modify (similar to chromosomes) 
- **locus** : position of a gene in the genome
- **allele** : value of a gene

### Offspring
new individual created, there is no gender distinctions in the offspring, the offspring is the new individual created by the genetic operations.
genetic operations act blindly at the level ov genome. this operation could be:
+ **mutation** : change the value of a gene
+ **crossover** : mix the value of a gene from 2 parents or more

### Survival selection
is deterministic. ranks all of the individual based on their fitness and select the best ones. the best ones are the ones that survive. the best ones are the ones that will be used to create the next generation.

### Parent selection
**Roulette wheel**
- *Fitness proportionate selection* : the probability of an individual to be selected is proportional to its fitness
- *Fitness windowing* : the probability of an individual to be selected is proportional to its fitness but the fitness is normalized in a window
- *Fitness Ranking* : the probability of an individual to be selected is proportional to its rank in the population

**Tournament selection**
+ *Binary* : 2 or more individuals are selected at random and the best one is selected, no need for a global sorting of the population. If i increase the number of tournaments i increase selective pressure. Low selective pressure = exploration, high selective pressure = exploitation

### Alterative type of GA
+ **Strategy 1**:
    -  *Selection* : copy fittest individual to the next generation
    - *Mutation* : Individuals can be slightly modified during the copy
    - *Crossover rate* : Recombination

+ **Strategy 2**:
    - *Selection* : choose parents
    - *Apply genetic operation* : crossover and mutation
    - *Mutation Rate* : The offspring can be slightly modified after


.....

27/10
first 30 minutes of lesson you were late
...

## Population Topology
1. **Panmittic** : all individuals are connected to all other individuals
2. **Lattice** : all individuals are connected to their neighbours

## Termination / Stopping Condition
1. **Steady state** : stop when the fitness of the best individual doesn't change for a certain number of generations
2. **Wall clock time** : stop when a certain amount of time has passed (usefull in industrial application)
3. **Best Solution Found** : 
4. **Total number of evaluation** : stop when a certain number of fitness evaluations has been performed
5. **Number of generations** : stop when a certain number of generations has been performed

## One Max Problem
is a problem where you have a string of 0 and 1 and you have to maximize the number of 1 in the string. It is a problem that can be solved by a simple algorithm, but it is a good problem to test the performance of a GA.




## TSP
Travelling Salesman Problem
weighted fully connected graph, i want to find a path that goes to all different vertexes and come back to the starting point. The path has to be the shortest possible.

step to design the solution
1. **Representation** : how to represent the solution
2. where the information is stored
    - **order**
    - **sequence**
    - **other**
[0,1,2,3,4,5,6,7,8,9] a list of numbers that represent the order in which the vertexes are visited
3. **No aliases** : the solution has to be unique
$[0,1,2,3,4] == [1,2,3,4,0]$
$[0,1,2,3,4] == [0,4,3,2,1]$
this types of sulution should be avoided since they are the same solution. to avoid this we can fix the starting city and the starting direction. this way we can avoid the aliases.
4. **genetic operations** : how to create a new solution from 2 parents
    - **mutation** : change the value of a gene
    - **crossover** : mix the value of a gene from 2 parents or more
5. **Survival selection** : how to select the best solution
6. **Sintactillay correct solutions** : the solution has to be valid

The *INFORMATION* lies in the edge of the list, meaning that $[0,1,2]$ $0$ and $1$ are connected, $1$ and $2$ are connected, $2$ and $0$ are connected in that order. 
#### MUTATION
permutations based mutation
$[0,1,2,3,4] \rightarrow [0,1,3,2,4]$
$[0,1,2,3,4] \rightarrow [0,4,3,2,1]$
$[0,1,2,3,4] \rightarrow [0,4,2,3,1]$

#### CROSSOVER
*One Cut Crossovers*
*Two Cut Crossovers*
*infeasable solutions*


#### OTHER ALGOS
if trinagula inequality is verified we can apply[kKerningan Lin Algorithm](https://en.wikipedia.org/wiki/Kernighan%E2%80%93Lin_algorithm)


## GA VS ES
if you can use **ES** use it or better if you can use **AUTOGRAD** if you can differentiate the function and calculate the gradient. In other cases uses **GA** but be carefull beacuse you will encounter some problems! start with a random mutation hillclimber and then move from it tryng to find a feasable crossover or mutation for the population and so on.

## BINARY REPRESENTATION
**gray coding** is a way to represent binary numbers in a way that the distance between 2 numbers is the same as the distance between the binary representation of the 2 numbers. this is useful because it is easier to calculate the distance between 2 numbers in binary representation than in decimal representation.

## INTEGER REPRESENTATION
fixed lenght vs variable lenght
discrete vs categorical values


### Random resetting
the allele in a random locus is replaced with a random value
### Creep mutation
the allele in a random locus is replaced with a random value in a small range around the original value (the range is small or large depending on the problem). it can be applied only if the values are discrete and can be ordered and sorted.

### where te information is stored
1 