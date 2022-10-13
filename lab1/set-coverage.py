import logging
import random
from collections import deque

def check_goal(current_bag,goal):
    flat_list = [item for sublist in current_bag for item in sublist]
    return set(goal) == set(flat_list)

N = 500
seed = 42
def problem(N, seed=None):
    random.seed(seed)
    return[
        list(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N,N*5))
    ],[_ for _ in range(N)]

def search(blocks,goal):
    frontier = deque()
    frontier.append(((),tuple(blocks)))
    n = 0
    while frontier:
        n+=1
        state = frontier.pop()
        c_bag, available_blocks = state

        if(check_goal(c_bag,goal)):
            logging.info("Found solution after %d iterations",n)
            break
        for i, object in enumerate(available_blocks):
            new_state = (
                tuple((*c_bag, object)),
                tuple(available_blocks[:i] + available_blocks[i + 1 :]),
            )
        frontier.append(new_state)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    blocks,goal = problem(N, seed)
    logging.debug(f"problem : {blocks} and solution : {goal}")
    search(blocks,goal)
