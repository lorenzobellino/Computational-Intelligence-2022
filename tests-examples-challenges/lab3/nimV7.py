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

NUM_MATCHES = 50
NIM_SIZE = 5
POPULATION = 10
NUM_GENERATIONS = 50
OFFSPRING = 7


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    and_list = list()
    or_list = list()
    sum_list = list()
    rshift_list = list()
    lshift_list = list()
    sub_list = list()
    nand_list = list()

    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        and_list.append((m, and_operation(tmp)))
        or_list.append((m, or_operation(tmp)))
        sum_list.append((m, sum(tmp.rows)))
        sub_list.append((m, sub_operation(tmp)))
        # nand_list.append((m, nand_operation(tmp)))
        # rshift_list.append((m, rshift_operation(tmp)))
        # lshift_list.append((m, lshift_operation(tmp)))

    cooked["and"] = and_list
    cooked["or"] = or_list
    cooked["sum"] = sum_list
    cooked["sub"] = sub_list
    # cooked["nand"] = nand_list
    # cooked["r-shift"] = rshift_list
    # cooked["l-shift"] = lshift_list

    return cooked


def sub_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.sub)
    return result


def nand_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, lambda x, y: ~(x & y))
    return result


def rshift_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.rshift)
    return result


def lshift_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.lshift)
    return result


def and_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.and_)
    return result


def or_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.or_)
    return result


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.xor)
    return result


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)
        alpha = genome["alpha"]
        beta = genome["beta"]
        gamma = genome["gamma"]
        delta = genome["delta"]

        res = (
            (a[0], abs(alpha * a[1] + beta * b[1] + gamma * c[1] + delta * d[1]))
            for a, b, c, d in zip(data["and"], data["or"], data["sum"], data["sub"])
        )
        ply = min(res, key=lambda x: x[1])[0]

        return ply

    return evolvable


def evaluate(strategy: Callable, opponent=opponents.pure_random) -> float:
    strategy = (strategy, opponent)
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = strategy[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won


def generate_population(dim: int) -> list:
    r = []
    for _ in range(dim):
        genome = {
            "alpha": random.uniform(-10, 10),
            "beta": random.uniform(-10, 10),
            "gamma": random.uniform(-10, 10),
            "delta": random.uniform(-10, 10),
            # "epsilon": random.uniform(-10, 10),
        }
        strat = make_strategy(genome)
        eval = (
            evaluate(strat, opponents.optimal_startegy),
            evaluate(strat, opponents.pure_random),
            evaluate(strat, opponents.gabriele),
            evaluate(strat, opponents.take_one_never_finish),
        )
        r.append((eval, strat, genome))
    return r


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i[0])


def combine(population, offspring):
    population += offspring
    population = sorted(population, key=lambda i: i[0], reverse=True)[:POPULATION]
    return population


def generate_offspring(population: list, gen: int) -> list:
    offspring = list()
    for i in range(OFFSPRING):
        p = tournament(population)

        p[2]["alpha"] += random.gauss(0, 10 / (gen + 1))
        p[2]["beta"] += random.gauss(0, 10 / (gen + 1))
        p[2]["gamma"] += random.gauss(0, 10 / (gen + 1))
        p[2]["delta"] += random.gauss(0, 10 / (gen + 1))
        # p[2]["epsilon"] += random.gauss(0, 10 / (gen + 1))

        strat = make_strategy(p[2])
        eval = (
            evaluate(strat, opponents.optimal_startegy),
            evaluate(strat, opponents.pure_random),
            evaluate(strat, opponents.gabriele),
            evaluate(strat, opponents.take_one_never_finish),
        )
        offspring.append((eval, strat, p[2]))
    return offspring


def main():
    # ev = evaluate(opponents.my_best_player, opponents.optimal_startegy)
    # logging.info(f"Optimal vs My best: {ev}")
    # input()
    import_population = False

    if import_population and os.path.exists("population.json"):
        with open("population.json", "r") as f:
            loaded_population = json.load(f)
            population = list()
            for i in loaded_population:
                genome = loaded_population[i]["genome"]
                strat = make_strategy(genome)
                eval = (
                    evaluate(strat, opponents.optimal_startegy),
                    evaluate(strat, opponents.pure_random),
                    evaluate(strat, opponents.gabriele),
                    evaluate(strat, opponents.take_one_never_finish),
                )
                population.append((eval, strat, genome))
        logging.info("loaded initial population")
    else:
        population = generate_population(POPULATION)
        logging.info("Generated initial population")

    logging.info(f"Initial population: {[(p[0],p[2]) for p in population]}")
    for _ in range(NUM_GENERATIONS):
        logging.info(f"Generation {_}")
        offspring = generate_offspring(population, _)
        population = combine(population, offspring)
        logging.info(f"best genome: {population[0][2]}")
        logging.info(f"best fitness: {population[0][0]}")
        if population[0][0][0] > 40:
            break

    logging.info(f"best genome: {population[0][2]}")

    with open("population.json", "w") as f:
        pop = {f"individual_{i:02}": {"fitness": p[0], "genome": p[2]} for i, p in enumerate(population)}
        json.dump(pop, f, indent=4)
    logging.info(f"saved population\nlength: {len(population)}")

    best_strat = make_strategy(population[0][2])

    matches = 10

    r1 = (
        sum([evaluate(best_strat, opponents.take_one_never_finish) for _ in range(matches)])
        * 100
        / (NUM_MATCHES * matches)
    )
    logging.info(f"R1 DONE")
    r2 = sum([evaluate(best_strat, opponents.gabriele) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    logging.info(f"R2 DONE")
    r3 = sum([evaluate(best_strat, opponents.pure_random) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    logging.info(f"R3 DONE")
    r4 = sum([evaluate(best_strat, opponents.optimal_startegy) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    logging.info(f"R4 DONE")

    rates = (r1, r2, r3, r4)
    logging.info(f"victories : {rates}")


if __name__ == "__main__":

    main()
