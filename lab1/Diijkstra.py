import random
import heapq
from collections import Counter
from typing import Callable
import logging

N = 5
SEED = 42

logging.getLogger().setLevel(logging.DEBUG)


class PriorityQueue:
    """A basic Priority Queue with simple performance optimizations"""

    def __init__(self):
        self._data_heap = list()
        self._data_set = set()

    def __bool__(self):
        return bool(self._data_set)

    def __contains__(self, item):
        return item in self._data_set

    def push(self, item, p=None):
        assert item not in self, f"Duplicated element"
        if p is None:
            p = len(self._data_set)
        self._data_set.add(item)
        heapq.heappush(self._data_heap, (p, item))

    def pop(self):
        p, item = heapq.heappop(self._data_heap)
        self._data_set.remove(item)
        return item


def problem(N, seed=None):
    """
    Creates an instance of the problem
    param N: number of elements
    param seed: random seed
    return: list of lists
    """
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def state_to_set(state):
    """Converts a state to a set of integers"""
    return set(sum((e for e in state), start=()))


def goal_test(state, GOAL):
    """
    Checks if the state is a goal state
    param state: a state
    param GOAL: the goal state
    return: True if the state is a goal state
    """
    return state_to_set(state) == GOAL


def possible_steps(state, all_lists):
    """
    Returns a list of possible steps
    param state: a state
    param all_lists: a list of lists of possible sets to choose from
    return: a list of possible steps
    """
    current = state_to_set(state)
    return [l for l in all_lists if not set(l) <= current]


def weight(state):
    """Returns the weight of a state
    param state: a state
    return: the weight of the state as 2 value:
        - the number of repetitions of elements
        - the number of elements with no repetitions as a negative value
    """
    cnt = Counter()
    cnt.update(sum((e for e in state), start=()))
    return sum(cnt[c] - 1 for c in cnt if cnt[c] > 1), -sum(cnt[c] == 1 for c in cnt)


def dijkstra(N, all_lists):
    """
    Vanilla Dijkstra's algorithm
    param N: number of elements
    param all_lists: a list of lists of possible sets to choose from
    return: the solution to the set covering problem"""

    GOAL = set(range(N))
    all_lists = tuple(set(tuple(_) for _ in all_lists))
    frontier = PriorityQueue()
    nodes = 0
    state = tuple()
    while state is not None and not goal_test(state, GOAL):
        nodes += 1
        for s in possible_steps(state, all_lists):
            frontier.push((*state, s), p=weight((*state, s)))
        state = frontier.pop()

    logging.info(f"nodes visited={nodes}; weight={sum(len(_) for _ in state)}")
    return state


def main():
    for N in [5, 10, 20]:
        logging.info(f" Solution for N={N}:")
        solution = dijkstra(N, problem(N, seed=42))


if __name__ == "__main__":
    main()
