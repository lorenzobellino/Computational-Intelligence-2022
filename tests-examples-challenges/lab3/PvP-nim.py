import logging
import random
import operator
import json
import os
from collections import namedtuple
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from math import ceil

import opponents
from opponents import Nim


Nimply = namedtuple("Nimply", "row, num_objects")

logging.getLogger().setLevel(logging.DEBUG)

NUM_MATCHES = 1
NIM_SIZE = 3
POPULATION = 10
NUM_GENERATIONS = 100
OFFSPRING = 7

"""
se puoi devi avere due righe alla stessa altezza
"""


def evaluate(strategy: Callable, opponent: Callable, game_size: int) -> float:
    strategy = (strategy, opponent)
    won = 0
    for _ in range(NUM_MATCHES):
        nim = Nim(game_size)
        player = 0
        while nim:

            ply = strategy[player](nim)
            nim.nimming(ply)
            logging.info(f"player : {player} : {str(nim)}")
            player = 1 - player
        if player == 1:
            won += 1
    return won


def main():
    game = 0
    res = 0
    # strategys = (opponents.five_param_5, opponents.optimal_startegy)
    strategys = (opponents.five_param_5, opponents.optimal_startegy)
    logging.info(f"player 0 : {strategys[0].__name__}\nplayer 1 : {strategys[1].__name__}")
    while input() != "q":
        game += 1
        # game_size = random.randint(5, 12)
        # game_size = NIM_SIZE
        game_size = 5
        res += evaluate(strategys[0], strategys[1], game_size)
        logging.info(f"player 0 won {res} out of {game} games = {res*100/game:.02f}%")


if __name__ == "__main__":

    main()
