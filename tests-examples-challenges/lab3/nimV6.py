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


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    cooked["minimum-moves"] = len([r for r in state.rows if r > 0])

    return cooked


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        row = 0
        num_objects = 0

        ply = (row, num_objects)

        return ply

    return evolvable


def evaluate(strategy: Callable, opponent=opponents.pure_random) -> float:
    strategy = (strategy, opponent)
    won = 0
    for _ in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:

            ply = strategy[player](nim)
            nim.nimming(ply)
            logging.info(f"player : {player} : {str(nim)}")
            player = 1 - player
        if player == 1:
            won += 1
    return won


def generate_population(dim: int) -> list:
    p = list()
    return p


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i[0])


def combine(population, offspring):
    population += offspring
    population = sorted(population, key=lambda i: i[0], reverse=True)[:POPULATION]
    return population


def generate_offspring(population: list, gen: int) -> list:
    offspring = list()
    for _ in range(OFFSPRING):
        p = tournament(population)

        strat = make_strategy(p)
        eval = (
            evaluate(strat, opponents.optimal_startegy),
            evaluate(strat, opponents.pure_random),
            evaluate(strat, opponents.gabriele),
            evaluate(strat, opponents.take_one_never_finish),
        )
        offspring.append((eval, strat, p[2]))
    return offspring


def main():
    game = 0
    res = 0
    while input() != "q":
        game += 1
        res += evaluate(opponents.my_best_player, opponents.optimal_startegy)
        logging.info(f"my bes player won {res}/{game} = {res*100/game:.2f} % of the time")
        # input()

    # import_population = False

    # if import_population and os.path.exists("population.json"):
    #     with open("population.json", "r") as f:
    #         loaded_population = json.load(f)
    #         population = list()
    #         for i in loaded_population:
    #             genome = loaded_population[i]["genome"]
    #             strat = make_strategy(genome)
    #             eval = (
    #                 evaluate(strat, opponents.optimal_startegy),
    #                 evaluate(strat, opponents.pure_random),
    #                 evaluate(strat, opponents.gabriele),
    #                 evaluate(strat, opponents.take_one_never_finish),
    #             )
    #             population.append((eval, strat, genome))
    #     logging.info("loaded initial population")

    # else:
    #     population = generate_population(POPULATION)
    #     logging.info("Generated initial population")

    # logging.info(f"Initial population: {[(p[0],p[2]) for p in population]}")
    # for _ in range(NUM_GENERATIONS):
    #     logging.info(f"Generation {_}")
    #     offspring = generate_offspring(population, _)
    #     population = combine(population, offspring)
    #     logging.info(f"best genome: {population[0][2]}")
    #     logging.info(f"best fitness: {population[0][0]}")
    #     if population[0][0][0] > 0:
    #         break

    # logging.info(f"best genome: {population[0][2]}")

    # with open("population.json", "w") as f:
    #     pop = {f"individual_{i:02}": {"fitness": p[0], "genome": p[2]} for i, p in enumerate(population)}
    #     json.dump(pop, f, indent=4)
    # logging.info(f"saved population\nlength: {len(population)}")
    # best_strat = make_strategy(population[0][2])

    # matches = 10

    # r1 = (
    #     sum([evaluate(best_strat, opponents.take_one_never_finish) for _ in range(matches)])
    #     * 100
    #     / (NUM_MATCHES * matches)
    # )
    # logging.info(f"R1 DONE")
    # r2 = sum([evaluate(best_strat, opponents.gabriele) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    # logging.info(f"R2 DONE")
    # r3 = sum([evaluate(best_strat, opponents.pure_random) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    # logging.info(f"R3 DONE")
    # r4 = sum([evaluate(best_strat, opponents.optimal_startegy) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    # logging.info(f"R4 DONE")
    # rates = (r1, r2, r3, r4)
    # logging.info(f"victories : {rates}")


if __name__ == "__main__":

    main()
