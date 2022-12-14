import logging
import random

from collections import namedtuple
from typing import Callable

from copy import deepcopy

import opponents
from opponents import Nim


Nimply = namedtuple("Nimply", "row, num_objects")

logging.getLogger().setLevel(logging.INFO)

NUM_MATCHES = 50
NIM_SIZE = 3


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    return cooked


def ending_game(state: Nim, is_maximizing: bool) -> int:
    if not state:
        if is_maximizing:
            return 1
        else:
            return -1
    else:
        return 0


def minimax_a_b_pruning(state: Nim, is_maximizing=False, alpha=1, beta=-1):
    possible = []
    # if state:
    #     data = cook_status(state)
    #     possible = data["possible_moves"]
    possible = cook_status(state)["possible_moves"]
    if not state:
        return (None, 1) if is_maximizing else (None, -1)

    # val = ending_game(state, is_maximizing)  # 1 if player 0 win, -1 if player 1 win, 0 otherwise

    # if val != 0 or not possible:
    #     return None, val

    evaluations = list()

    for ply in possible:
        state_copy = deepcopy(state)
        state_copy.nimming((ply))
        _, val = minimax_a_b_pruning(state_copy, is_maximizing=not is_maximizing, alpha=alpha, beta=beta)
        evaluations.append((ply, val))
        if is_maximizing:
            alpha = max(alpha, val)
        else:
            beta = min(beta, val)
        if beta <= alpha:
            break
    logging.info(f"evaluations: {evaluations}")
    return max(evaluations, key=lambda x: x[1]) if is_maximizing else min(evaluations, key=lambda x: x[1])


def main():
    nim = Nim(3)
    memory = dict()
    player = 0
    logging.info(f"nim: {nim}")
    while nim:
        logging.info(f"player: {player} -> {nim}")
        if player == 0:
            ply, _ = minimax_a_b_pruning(nim, is_maximizing=True)
            # logging.info(f"ply : {ply}")
        else:
            # ply = opponents.optimal_startegy(nim)
            ply = opponents.pure_random(nim)
        nim.nimming(ply)
        logging.info(f"ply : {ply}")
        player = 1 - player

    if player == 1:
        logging.info(f"victory")
    else:
        logging.info(f"defeat")

    # for k, v in memory.items():
    #     logging.info(f"m : {k} v: {v}")


if __name__ == "__main__":

    main()
