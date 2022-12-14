import logging
import random
import json
import os
from collections import namedtuple
from typing import Callable

import opponents
from opponents import Nim


Nimply = namedtuple("Nimply", "row, num_objects")

logging.getLogger().setLevel(logging.DEBUG)

NUM_MATCHES = 50
NIM_SIZE = 5
POPULATION = 10
NUM_GENERATIONS = 25
OFFSPRING = 7


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = opponents.cook_data(state)

        alpha = genome["alpha"]
        beta = genome["beta"]
        gamma = genome["gamma"]
        delta = genome["delta"]
        epsilon = genome["epsilon"]

        res = (
            (a[0], abs(alpha * a[1] + beta * b[1] + gamma * c[1] + delta * d[1] + epsilon * e[1]))
            for a, b, c, d, e in zip(data["and"], data["or"], data["sum"], data["sub"], data["nand"])
        )
        ply = min(res, key=lambda x: x[1])[0]

        return ply

    return evolvable


def evaluate(strategy: Callable, opponent=opponents.pure_random) -> float:
    strategy = (strategy, opponent)
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(random.randint(5, 12))
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
            "epsilon": random.uniform(-10, 10),
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

        p[2]["alpha"] += random.gauss(0, 20 / (gen + 1))
        p[2]["beta"] += random.gauss(0, 20 / (gen + 1))
        p[2]["gamma"] += random.gauss(0, 20 / (gen + 1))
        p[2]["delta"] += random.gauss(0, 20 / (gen + 1))
        p[2]["epsilon"] += random.gauss(0, 20 / (gen + 1))

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
    # if you want to import a population from a previous run, set this to True
    import_population = False

    if import_population and os.path.exists("populationV8.json"):
        with open("populationV8.json", "r") as f:
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
        logging.info(f"generating initial population of {POPULATION} individuals")
        population = generate_population(POPULATION)
        logging.info("Generated initial population")

    for _ in range(NUM_GENERATIONS):
        logging.info(f"Generation {_}")
        offspring = generate_offspring(population, _)
        population = combine(population, offspring)
        logging.debug(f"best genome: {population[0][2]}")
        logging.debug(f"best fitness: {population[0][0]}")
        if population[0][0][0] > 20:
            break

    logging.info(f"best genome: {population[0][2]}")

    with open("populationV8.json", "w") as f:
        pop = {f"individual_{i:02}": {"fitness": p[0], "genome": p[2]} for i, p in enumerate(population)}
        json.dump(pop, f, indent=4)
    logging.info(f"saved population\nlength: {len(population)}")


if __name__ == "__main__":

    main()
