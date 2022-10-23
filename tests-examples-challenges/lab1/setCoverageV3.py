import logging
import random
from collections import deque
import heapq
N = 500
seed = 42

class el:
    def __init__(self, data:set):
        self.data = data.copy()
    def __lt__(self, other):
        return len(self.data) < len(other.data)
    def __eq__(self, other):
        return len(self.data) == len(other.data)
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return repr(self.data)


def problem(N, seed=None):
    random.seed(seed)
    bag = [set(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2)))) for n in range(random.randint(N,N*5))]
    goal = [_ for _ in range(N)]
    return bag,goal

def search(subsets, parent_set):
    parent_set = set(parent_set)
    max = len(parent_set)
    explored = 0
    # create the initial heap. Note 'subsets' can be unsorted,
    # so this is independent of whether remove_redunant_subsets is used.
    heap = []
    for s in subsets:
        # Python's heapq lets you pop the *smallest* value, so we
        # want to use max-len(s) as a score, not len(s).
        # len(heap) is just proving a unique number to each subset,
        # used to tiebreak equal scores.
        heapq.heappush(heap, [max-len(s), len(heap), s])
    results = []
    result_set = set()
    while result_set < parent_set:
        logging.debug('len of result_set is {0}'.format(len(result_set)))
        best = []
        unused = []
        while heap:
            explored += 1
            score, count, s = heapq.heappop(heap)
            if not best:
                best = [max-len(s - result_set), count, s]
                continue
            if score >= best[0]:
                # because subset scores only get worse as the resultset
                # gets bigger, we know that the rest of the heap cannot beat
                # the best score. So push the subset back on the heap, and
                # stop this iteration.
                heapq.heappush(heap, [score, count, s])
                break
            score = max-len(s - result_set)
            if score >= best[0]:
                unused.append([score, count, s])
            else:
                unused.append(best)
                best = [score, count, s]
        add_set = best[2]
        logging.debug('len of add_set is {0} score was {1}'.format(len(add_set), best[0]))
        results.append(add_set)
        result_set.update(add_set)
        # subsets that were not the best get put back on the heap for next time.
        while unused:
            heapq.heappush(heap, unused.pop())
    logging.info(f"explored {explored} nodes")
    return results


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    blocks,goal = problem(N, seed)
    logging.debug(f"\nproblem : {blocks}\nsolution : {goal}")
    #search(blocks,goal)
    # parent = set()
    res = search(blocks,range(N))
    logging.info(f"result: {res}")
    logging.info(f"result: {sum([len(s) for s in res])}")
    # print(make_subsets(range(N),20))