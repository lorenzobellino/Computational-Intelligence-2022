from collections import namedtuple

# from best_player import cook_data
from opponents import pure_random, Nim
from itertools import product
from copy import deepcopy
from functools import cache
import random


Nimply = namedtuple("Nimply", "row, num_objects")


@cache
def cook_data(state: Nim) -> dict:
    # print(f"rows: {state.rows}")
    bf = []
    data = {}
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    for m in possible_moves:
        tmp = deepcopy(state)
        tmp.nimming(m)
        # bf.append(tmp)
        bf.append((m, tmp))
    data["brute_force"] = bf
    data["possible_moves"] = possible_moves

    return data


def RLAgent(G: dict) -> Nimply:
    """the agent related to the task 3.4"""

    def agent(state: Nim):
        possibleStates = cook_data(state)["brute_force"]
        ply = max(((s[0], G[s[1].rows]) for s in possibleStates if s[1].rows in G), key=lambda i: i[1])[0]
        return Nimply(ply[0], ply[1])

    return agent


class Agent(object):
    def __init__(self, state, alpha=0.15, random_factor=0.2):
        self.state_history = [(tuple(state._rows), 0)]  # state, reward
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}
        self.init_reward(state)

    def init_reward(self, state):
        for i in product(*(range(x + 1) for x in state._rows)):
            self.G[i] = random.uniform(0.1, 1)

    def choose_action(self, state, allowedMoves):
        maxG = -10e15
        next_move = None

        randomN = random.random()
        if randomN < self.random_factor:
            random.randint(0, len(allowedMoves) - 1)
            next_move = allowedMoves[random.randrange(len(allowedMoves))]
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for action in allowedMoves:
                stateCopy = deepcopy(state)
                stateCopy.nimming(action)
                if self.G[tuple(stateCopy._rows)] >= maxG:
                    next_move = action
                    maxG = self.G[tuple(stateCopy._rows)]

        return next_move

    def update_state_history(self, state, reward):
        self.state_history.append((tuple(state._rows), reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5  # decrease random factor each episode of pla

    def get_policy(self):
        return self.G
