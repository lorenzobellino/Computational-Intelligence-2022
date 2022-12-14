import logging
import random

from collections import namedtuple
from typing import Callable

from copy import deepcopy

import opponents
from opponents import Nim


Nimply = namedtuple("Nimply", "row, num_objects")

logging.getLogger().setLevel(logging.DEBUG)

NUM_MATCHES = 50
NIM_SIZE = 3


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    return cooked


def minmax(state: Nim, player: bool, depth: int) -> Nimply:
    # logging.info(f"depth: {depth}")
    if not state:
        return not player
    possible_moves = cook_status(state)["possible_moves"]
    if player:
        for move in possible_moves:
            new_state = deepcopy(state)
            new_state.nimming(move)
            v = minmax(new_state, False, depth + 1)
            if v:
                return v
        return False
    else:
        for move in possible_moves:
            new_state = deepcopy(state)
            new_state.nimming(move)
            v = minmax(new_state, True, depth + 1)
            if not v:
                return v
        return True


def minmax_choice(state: Nim, player: bool, depth: int) -> Nimply:
    possible_moves = cook_status(state)["possible_moves"]
    choices = []
    for move in possible_moves:
        new_state = deepcopy(state)
        new_state.nimming(move)
        result = minmax(new_state, not player, 0)
        choices.append((result, move))
    logging.info(f"choices: {choices}")
    for choice in choices:
        if choice[0]:
            return choice[1]
    return random.choice(choices)[1]


def main():
    nim = Nim(3)

    player = 0
    """0 1 2"""
    # nim.nimming((0, 1))
    # nim.nimming((1, 2))
    # nim.nimming((2, 3))

    """0 2 3"""
    nim.nimming((0, 1))
    nim.nimming((1, 1))
    nim.nimming((2, 2))
    logging.info(f"nim: {nim}")
    while nim:
        logging.info(f"player: {player} -> {nim}")
        if player == 0:
            ply = minmax_choice(nim, True, 0)
        else:
            ply = opponents.optimal_startegy(nim)
        nim.nimming(ply)
        logging.info(f"ply : {ply}")
        player = 1 - player

    if player == 1:
        logging.info(f"victory")
    else:
        logging.info(f"defeat")


if __name__ == "__main__":

    main()
