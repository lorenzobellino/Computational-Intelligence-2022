import logging
import random
from collections import namedtuple
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor


logging.getLogger().setLevel(logging.DEBUG)

NUM_MATCHES = 1000
NIM_SIZE = 11
Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["nim_sum"] = nim_sum(state)
    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked


def optimal_startegy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)
        if random.random() < genome["p"]:
            ply = Nimply(data["shortest_row"], random.randint(1, state.rows[data["shortest_row"]]))
        else:
            ply = Nimply(data["longest_row"], random.randint(1, state.rows[data["longest_row"]]))

        return ply

    return evolvable


def evaluate(strategy: Callable) -> float:
    strategy = (strategy, pure_random)
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = strategy[player](nim)
            nim.nimming(ply)
            # logging.debug(f"status: After player {player} -> {nim}")
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    # x = Nim(3)
    # cook_status(x)
    # strategy = (pure_random, evolvable)
    # strategy = (make_strategy({"p": 0.5}), make_strategy({"p": 0.8}))
    # strategy = make_strategy({"p": 0.99})
    # eval = evaluate(strategy=strategy)
    # logging.info(f"Eval: {eval}")
    # nim = Nim(11)
    # logging.debug(f"status: Initial board  -> {nim}")
    # player = 0
    # while nim:
    #     ply = strategy[player](nim)
    #     nim.nimming(ply)
    #     logging.debug(f"status: After player {player} -> {nim}")
    #     player = 1 - player
    # winner = 1 - player
    # logging.info(f"status: Player {winner} won!")

    logging.info(f"{evaluate(optimal_startegy)}")

    # strategy = (make_strategy({"p": 0.1}), optimal_startegy)
    # nim = Nim(11)
    # logging.debug(f"status: Initial board  -> {nim}")
    # player = 0
    # while nim:
    #     ply = strategy[player](nim)
    #     nim.nimming(ply)
    #     logging.debug(f"status: After player {player} -> {nim}")
    #     player = 1 - player
    # winner = 1 - player
    # logging.info(f"status: Player {winner} won!")


if __name__ == "__main__":
    main()
