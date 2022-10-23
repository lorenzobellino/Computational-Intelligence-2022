import random
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
import logging
import random
from collections import deque
N = 500
seed = 42

@dataclass(order=True)
class PrioritizedSet:
    priority: int
    item: Any=field(compare=False)

def problem(N, seed=None):
    random.seed(seed)
    bag = [set(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2)))) for n in range(random.randint(N,N*5))]
    goal = [_ for _ in range(N)]
    return bag,goal

def search(subsets, parent_set):
    parent_set = set(parent_set)
    
    pq = PriorityQueue() 
    for ps in subsets:
        pq.put(PrioritizedSet(-len(ps), ps))

    results = []
    result_set = set()
    while result_set < parent_set:
        logging.debug(f"len of result_set is {len(result_set)}")
        best = []
        unused = []
        while not pq.empty():
            s = pq.get().item
            score = N - len(s)
            if not best:
                best = [N-len(s - result_set),s]
                continue
            if score >= best[0]:
                pq.put(PrioritizedSet(-len(s),s))
                break
            score = N-len(s - result_set)
            if score >= best[0]:
                unused.append([score, s])
            else:
                unused.append(best)
                best = [score, s]
        add_set = best[1]
        logging.debug(f"len of added set is {len(add_set)} score was {best[0]}")
        result_set = result_set.union(add_set)
        results.append(add_set)
        for score,s in unused:
            pq.put(PrioritizedSet(score,s))
        
    return results


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    blocks,goal = problem(N, seed)
    res = search(blocks,range(N))
    logging.info(f"{res}")
    logging.info(f"len of res is {sum(len(s) for s in res)}")
