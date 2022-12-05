import logging
import random
from collections import namedtuple
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor
from math import ceil


logging.getLogger().setLevel(logging.INFO)

NUM_MATCHES = 100
NIM_SIZE = 11
POPULATION = 50
NUM_GENERATIONS = 10
OFFSPRING = 20
evaluation = 0
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
        try:
            assert self._rows[row] >= num_objects
        except AssertionError as er:
            logging.debug(f"AssertionError: {er}")
            logging.debug(f"row: {row}, num_objects: {num_objects}")
            logging.debug(f"self : {self}")
            raise er

        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]

    return cooked


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)
        if random.random() < genome["p_rule"]:
            ply = Nimply(data["shortest_row"], max(1, int((1 - genome["p_row"]) * state.rows[data["shortest_row"]])))
        else:
            ply = Nimply(data["longest_row"], max(1, int(genome["p_row"] * state.rows[data["longest_row"]])))
        logging.debug(f"ply: {ply}")
        logging.debug(f"")
        logging.debug(f"p_rule: {genome['p_rule']}")
        logging.debug(f"p_row: {genome['p_row']}")
        return ply

    return evolvable


def take_one_never_finish(State: Nim) -> Nimply:
    try:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 1][0]
    except IndexError:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 0][0]
    return Nimply(*move)


def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def evaluate(strategy: Callable) -> float:
    strategy = (strategy, take_one_never_finish)
    global evaluation
    evaluation += 1
    won = 0
    for m in range(NUM_MATCHES):
        # evaluation += 1
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = strategy[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def generate_population(dim: int) -> list:
    r = []
    for _ in range(dim):
        genome = {"p_rule": random.random(), "p_row": random.random()}
        strat = make_strategy(genome)
        eval = evaluate(strat)
        r.append((eval, strat, genome))
    return r


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i[0])


def combine(population, offspring):
    population += offspring
    population = sorted(population, key=lambda i: i[0], reverse=True)[:POPULATION]
    return population


def generate_offspring(population: list) -> list:
    offspring = list()
    for i in range(OFFSPRING):
        p = deepcopy(tournament(population))
        p[2]["p_rule"] += random.gauss(0, 0.2)
        p[2]["p_row"] += random.gauss(0, 0.2)
        try:
            assert p[2]["p_row"] <= 1
        except AssertionError:
            p[2]["p_row"] = 1
        try:
            assert p[2]["p_row"] >= 0
        except AssertionError:
            p[2]["p_row"] = 0
        strat = make_strategy(p[2])
        offspring.append((evaluate(strat), strat, p[2]))
    return offspring


def evaluate_rand(strategy: Callable) -> float:
    strategy = (strategy, pure_random)
    global evaluation
    evaluation += 1
    won = 0
    for m in range(NUM_MATCHES):
        # evaluation += 1
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = strategy[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def main():
    global evaluation
    population = generate_population(POPULATION)
    logging.info(f"Initial population: {[p[2] for p in population]}")
    for _ in range(NUM_GENERATIONS):
        logging.info(f"Generation {_}")
        # logging.info(f"{evaluation} evaluations")
        offspring = generate_offspring(population)
        population = combine(population, offspring)
        # logging.info(f"best genome: {population[0][2]}")
        logging.info(f"best fitness: {population[0][0]}")
    logging.info(f"best genome: {population[0][2]}")
    g = population[0][2]
    strat = make_strategy(g)
    logging.info(f"victory rate: {evaluate_rand(strat)}")
    logging.info(f"evaluations: {evaluation}")


if __name__ == "__main__":
    # x = Nim(5)
    # d = cook_status(x)
    # logging.info(f"status: {d}")
    # logging.info(f"longest row: {d['longest_row']}")
    main()
