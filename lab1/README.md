# Lab 1 : Set Covering Problem

First lab + peer review. List this activity in your final report, it will be part of your exam.

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, 
determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\forall n \in [0, N-1] \ \exists i : n \in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum. 

## Instructions

* Create the directory `lab1` inside the course repo (the one you registered with Andrea)
* Put a `README.md` and your solution (all the files, code and auxiliary data if needed)
* Use `problem` to generate the problems with different $N$
* In the `README.md`, report the the total numbers of elements in $L_{s_i}$ for problem with $N \in [5, 10, 20, 100, 500, 1000]$ and the total number on $nodes$ visited during the search. Use `seed=42`.
* Use `GitHub Issues` to peer review others' lab

## Notes

* Working in group is not only allowed, but recommended (see: [Ubuntu](https://en.wikipedia.org/wiki/Ubuntu_philosophy) and [Cooperative Learning](https://files.eric.ed.gov/fulltext/EJ1096789.pdf)). Collaborations must be explicitly declared in the `README.md`.
* [Yanking](https://www.emacswiki.org/emacs/KillingAndYanking) from the internet is allowed, but sources must be explicitly declared in the `README.md`.

**Deadline**

* Sunday, October 16th 23:59:59 for the working solution
* Sunday, October 23rd 23:59:59 for the peer reviews

# My proposed solution

## Reference and material
This solution was developed partially in conjunction with Elia Fontana and partially by searching some online references, which includes:
1. This [paper](https://arxiv.org/ftp/arxiv/papers/1506/1506.04220.pdf) by Drona Pratap Chandu on some greedy implementation of set cover
2. This [thread](https://stackoverflow.com/questions/21973126/set-cover-or-hitting-set-numpy-least-element-combinations-to-make-up-full-set) on stackoverflow
3. The slide used by the Professor during lecture, especially the proposed solution for the MinSum problem

## Greedy approach

Although I have used this as reference material my solution differ from the other that i have seen. The basic greedy implementation of this algorithm choose the local best set based on the maximum number of new elements that it will cover if inserted in te solution. My implementation instead is based on the percentage of new coverage in each set.
For examples, given:

$N = 10$
$goal = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \}$
$result = \{ 1, 3, 5 \}$
$set = \{ 3, 5, 7, 8 \}$

The weight is given by the fact that $set$ has $4$ values of which only $2$ are not already in the reslut set, so it's weight is $\frac{2}{4} = 0.5$
then the percentage is transformed in a value between $0$ and $100$ using this formula
```python
def calculate_weight(r,g,s = set(),threshold=1):
    w = ceil(100*sum(x in g-r for x in s) / len(s))
    return 100 if w>=threshold*100 else w
```
I decided also to include a treshold in order to speed up the algorithm and to drastically reduce the number of explored states, the default value is one but it can be expressed as a value between $0.01$ and $1$.
If the value is set as default only when a set has a coverage of $100\%$ is chosen as a local best but if the value of threshold is set to a value $\lt 1$ then if the coverage of the set is $\ge threshold * 100$ then it will be considered a local optimum. 

This weight is then used to store the sets in a PriorityQueue, in order to use this object i had to create my own class to store the sets with the priority calculate with the formula above, the class is:

```python
class PrioritizedSet:
    def __init__(self, priority: int, s: set):
        self.priority = 100 - priority
        self.item = s

    def __lt__(self, other):
        return self.priority < other.priority
    
    def __eq__(self, other):
        return self.priority == other.priority
    
    def __gt__(self, other):
        return self.priority > other.priority
```
The priority is insrted as $100 - weight$ because the PriorityQueue insert the smallest priority at the top of the queue.

## The core of my algorithm

```python
while result is not None and not result_set == goal:
        while not options.empty():
            discovered_state += 1
            s = options.get().item
            coverage = calculate_weight(result_set,goal,s,threshold)
            if coverage == 100:
                result.append(s)
                result_set = result_set.union(s)
                while not unused.empty():
                    pq.put(unused.get())
                break
            elif coverage != 0:
                unused.put(PrioritizedSet(coverage,s))
        else:
            if unused.empty():
                result = None
                break
            else:
                local_best = unused.get().item
                result.append(local_best)
                result_set = result_set.union(local_best)
                while not unused.empty():
                    options.put(unused.get())
```
Until a solution is not reached i extract an element from the queue, then calculate its coverage. If the coverage is $100\%$ the set is appended to the solution otherwise is appended to an other queue of unused set. the unused sets are reinserted in the original queue and the next local best set is calculated.

If there is no set with coverage $100\%$ then the set with the gratest coverage is selected as a local best.

If a set has a coverage of 0 it means that adding it to the result set will only increment the weight of the solution, for this reason if found it is not reinserted in the unused queue but it is discarded.

If after calculating all the new weight and searching for a local best the unused queue is empty it means that there are no solution reachable from that state so the algorithm stops and return  ``` None ```

## Results

#### Using a value of $1$ for $threshold$ I obtained the following results:
#### $N = 5$
```Explored states``` : $8$
```Solution's weight``` : $5$

#### $N = 10$
```Explored states``` : $52$
```Solution's weight``` : $10$

#### $N = 20$
```Explored states``` : $66$
```Solution's weight``` : $24$

#### $N = 50$
```Explored states``` : $832$
```Solution's weight``` : $76$

#### $N = 100$
```Explored states``` : $2098$
```Solution's weight``` : $181$

#### $N = 500$
```Explored states``` : $17914$
```Solution's weight``` : $1244$

#### $N = 1000$
```Explored states``` : $39631$
```Solution's weight``` : $2871$

For a combined time of 2 minute and 23.2 seconds 


#### Using a value of $0.5$ for $threshold$ I obtained the following results:
#### $N = 5$
```Explored states``` : $4$
```Solution's weight``` : $6$

#### $N = 10$
```Explored states``` : $17$
```Solution's weight``` : $13$

#### $N = 20$
```Explored states``` : $41$
```Solution's weight``` : $32$

#### $N = 50$
```Explored states``` : $591$
```Solution's weight``` : $77$

#### $N = 100$
```Explored states``` : $1035$
```Solution's weight``` : $172$

#### $N = 500$
```Explored states``` : $15959$
```Solution's weight``` : $1309$

#### $N = 1000$
```Explored states``` : $35395$
```Solution's weight``` : $2971$

For a combined time of 2 minutes and 7.3 seconds
Which is not much in time saving but the space of the states explored is much smaller and in case for $N = 100$ it found even a better solution

#### Testing for different values of threshold

In the file [results.txt](https://github.com/lorenzobellino/Computational-Intelligence-2022/blob/main/lab1/results.txt) file i have collected the results and timing for each $\forall n \in [0, N-1]$ and $\forall t \in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]$ where $t = threshold$ 


