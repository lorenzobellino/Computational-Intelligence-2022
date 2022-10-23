import logging
from queue import PriorityQueue
import random
from collections import deque
from utility import *

N = 10
seed = 42
logging.basicConfig(level=logging.DEBUG)


def check_goal(current_bag, goal):
    flat_list = [item for sublist in current_bag for item in sublist]
    return set(goal) == set(flat_list)


def problem(N, seed=None):
    random.seed(seed)
    bag = [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    goal = [_ for _ in range(N)]
    return bag, goal


def search(blocks, goal):
    frontier = deque()
    frontier.append(((), tuple(blocks)))
    w = len(blocks)
    n = 0
    while frontier:
        n += 1
        state = frontier.pop()
        c_bag, available_blocks = state
        if check_goal(c_bag, goal):
            numbers = sum([len(l) for l in c_bag])
            logging.info(
                f"\nFound solution after {n} iterations\nThe solution contains {numbers} numbers",
            )
            logging.debug(f"\n{set([item for sublist in c_bag for item in sublist])}")
            break
        for i, object in enumerate(available_blocks):
            new_state = (
                tuple((*c_bag, object)),
                tuple(available_blocks[:i] + available_blocks[i + 1 :]),
            )
            frontier.append(new_state)
    else:
        logging.info(f"\nThere is no solution with this initial dataset")


if __name__ == "__main__":
    for n in [5, 10, 20, 50, 100, 500, 1000]:
        blocks, goal = problem(n, seed)
        # logging.debug(f"\nproblem : {blocks}\nsolution : {goal}")
        search(blocks, goal)
