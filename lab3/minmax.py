import logging
import random

from collections import namedtuple
from typing import Callable

from copy import deepcopy

import opponents
from opponents import Nim


Nimply = namedtuple("Nimply", "row, num_objects")

logging.getLogger().setLevel(logging.DEBUG)

NIM_SIZE = 5


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    return cooked


def minmax(state: Nim, player: bool, depth: int = None, memory: dict = {}) -> Nimply:
    """
    recursive minmax function
    parameters:
        state: the current state of the game
        player: True if the player is the maximizing player
        depth: the depth of the search tree
        memory: a dictionary of states and their values
    returns:
        True if the player can win from this state
        False if the player can't win from this state
    """
    if not state:
        return not player

    if (state, player) in memory:
        return memory[(state, player)]

    if depth is not None and depth == -1:
        return True

    possible_moves = cook_status(state)["possible_moves"]
    if player:
        for move in possible_moves:
            new_state = deepcopy(state)
            new_state.nimming(move)
            v = minmax(new_state, False, depth - 1 if depth is not None else None, memory)
            if v:
                # if player is maximising and v is True, then we can win from this state
                break
        if (state, player) not in memory:
            memory[(state, player)] = v
        return v
    else:
        for move in possible_moves:
            new_state = deepcopy(state)
            new_state.nimming(move)
            v = minmax(new_state, True, depth - 1 if depth is not None else None, memory)
            if not v:
                # if player is minimising and v is False, then we can't win from this state
                break
        if (state, player) not in memory:
            memory[(state, player)] = v
        return v


def minmax_choice(state: Nim, player: bool, memory: dict) -> Nimply:
    """
    returns the best move for the player implementing minmax
    parameters:
        state: the current state of the game
        player: True if the player is the maximizing player
        memory: a dictionary of states and their values
            memory -> key = (state, player)
                   -> value = True if first player can win from this state, False otherwise
    returns:
        Nimply: the best move for the player
    """
    possible_moves = cook_status(state)["possible_moves"]
    # choices = []

    # for values of NIM_SIZE > 6, we need to limit the depth of the search tree
    maxdepth = None
    for move in possible_moves:
        new_state = deepcopy(state)
        new_state.nimming(move)
        result = minmax(new_state, not player, maxdepth, memory)
        if result:
            return move
        # choices.append((result, move))

    # return next((c[1] for c in choices if c[0]), random.choice(choices)[1])


def main():
    nim = Nim(NIM_SIZE)
    player = 0
    logging.info(f"nim: {nim}")
    while nim:
        logging.info(f"player: {player} -> {nim}")
        if player == 0:
            ply = minmax_choice(nim, True, {})
        else:
            ply = opponents.pure_random(nim)
        nim.nimming(ply)
        logging.info(f"ply : {ply}")
        player = 1 - player

    if player == 1:
        logging.info(f"victory")
    else:
        logging.info(f"defeat")


if __name__ == "__main__":

    main()
