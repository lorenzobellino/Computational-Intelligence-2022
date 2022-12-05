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
NIM_SIZE = 5
POPULATION = 10
NUM_GENERATIONS = 100
OFFSPRING = 7

"""
se puoi devi avere due righe alla stessa altezza
"""


def evaluate(strategy: Callable, opponent=opponents.pure_random) -> float:
    strategy = (strategy, opponent)
    won = 0
    for _ in range(NUM_MATCHES):
        nim = Nim(random.randint(5, 15))
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
    while input() != "q":
        game += 1
        res += evaluate(opponents.five_parameters_player_nim_5_rand, opponents.optimal_startegy)
        logging.info(f"my bes player won {res}/{game} = {res*100/game:.2f} % of the time")


if __name__ == "__main__":

    main()
