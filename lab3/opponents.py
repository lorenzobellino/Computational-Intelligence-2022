import logging
import random
import operator
import json
from collections import namedtuple
from itertools import accumulate
from copy import deepcopy
from functools import cache


Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        # self._rows = [i + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        try:
            assert self._rows[row] >= num_objects
        except AssertionError as er:
            logging.debug(f"AssertionError: {er}")
            logging.debug(f"row: {row}, num_objects: {num_objects}")
            logging.debug(f"self : {self}")
            raise er

        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

    def available_moves(self) -> list:
        return [(r, o) for r, c in enumerate(self.rows) for o in range(1, c + 1) if self._k is None or o <= self._k]

    def get_state_and_reward(self):
        return self.rows, self.give_reward()

    def give_reward(self):
        return 1 if sum(self._rows) == 0 else 0


def gabriele(state: Nim) -> Nimply:
    """
    Player that picks always the maximum number of objects from the lowes row
    param state: Nim
    return: Nimply
    """
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def take_one_never_finish(State: Nim) -> Nimply:
    """
    Player that always take one object without finishing a row if it is possible
    param state: Nim
    return: Nimply
    """
    try:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 1][0]
    except IndexError:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 0][0]
    return Nimply(*move)


def pure_random(state: Nim) -> Nimply:
    """
    Pure random player, pick a random move between all the possible moves
    param state: Nim
    return: Nimply
    """
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def nim_sum(state: Nim) -> int:
    """
    Player with the optimal strategy
    param state: Nim
    return: result: int, the nim sum of the state
    """
    *_, result = accumulate(state.rows, operator.xor)
    return result


def brute_force(state: Nim) -> dict:
    """
    Apply the nimSum to all the possible moves and return a dictionary with the possible moves and the nim sum
    param state: Nim
    return: dict
    """
    bf = list()
    data = dict()
    possible_moves = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    for m in possible_moves:
        tmp = deepcopy(state)
        tmp.nimming(m)
        bf.append((m, nim_sum(tmp)))
    data["brute_force"] = bf
    return data


def optimal_startegy(state: Nim) -> Nimply:
    """
    Player with the optimal strategy (nimSum)
    param state: Nim
    return: Nimply
    """
    data = brute_force(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def nim_sum(state: Nim) -> int:
    """
    Perform the nim sum operation between the row's objects
    param state: Nim
    return: result: int, the nim sum operation of the state
    """
    *_, result = accumulate(state.rows, operator.xor)
    return result


def human_player(state: Nim) -> Nimply:
    """Human player
    param state: Nim
    return: Nimply
    """
    logging.info(f"\n{state}")
    row = int(input("row: "))
    num_objects = int(input("num_objects: "))
    return Nimply(row, num_objects)

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

def rl_agent(state: Nim) -> Nimply:
    possibleStates = cook_data(state)["brute_force"]
    G = json.load(open("policy.json"))
    G = {tuple(int(i) for i in k): v for k, v in G.items()}
    ply = max(((s[0], G[s[1].rows]) for s in possibleStates if s[1].rows in G), key=lambda i: i[1])[0]
    return Nimply(ply[0], ply[1])