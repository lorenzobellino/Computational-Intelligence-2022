import logging
import random
from collections import namedtuple
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor
from math import ceil


logging.getLogger().setLevel(logging.DEBUG)

NUM_MATCHES = 100
NIM_SIZE = 11
POPULATION = 20
NUM_GENERATIONS = 100
OFFSPRING = 7
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
    try:
        cooked["1_left"] = [x for x in enumerate(state.rows) if x[1] == 1][0][0]
    except IndexError:
        cooked["1_left"] = [x for x in enumerate(state.rows) if x[1] >= 1][0][0]
    try:
        cooked["many_left"] = [x for x in enumerate(state.rows) if x[1] > 1][0][0]
    except IndexError:
        cooked["many_left"] = [x for x in enumerate(state.rows) if x[1] >= 1][0][0]

    return cooked


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if random.random() < genome["aggression"]:
            # seleziono righe con 1 solo elemento
            ply = Nimply(data["1_left"], 1)
        else:
            # seleziono righe con più di 1 elemento
            row = data["many_left"]
            num_objects = state.rows[row]
            if random.random() < genome["finisher"]:
                ply = Nimply(row, num_objects)
            else:
                ply = Nimply(row, num_objects - 1)
        # if random.random() < genome["p_rule"]:
        #     ply = Nimply(data["shortest_row"], max(1, int((1 - genome["p_row"]) * state.rows[data["shortest_row"]])))
        # else:
        #     ply = Nimply(data["longest_row"], max(1, int(genome["p_row"] * state.rows[data["longest_row"]])))
        # logging.debug(f"ply: {ply}")
        # logging.debug(f"")
        # logging.debug(f"p_rule: {genome['p_rule']}")
        # logging.debug(f"p_row: {genome['p_row']}")
        return ply

    return evolvable


def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]

    # r = [(r,o) for r,o in state.rows if o >= state.k]
    # try:
    #     return Nimply(r[0][0],state.k)
    # except IndexError:
    #     r1 = [(r,o) for r,o in state.rows if o >= 1]
    #     return Nimply(r1[0][0],r1[0][1])

    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def take_one_never_finish(State: Nim) -> Nimply:
    try:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 1][0]
    except IndexError:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 0][0]
    return Nimply(*move)


def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def evaluate(strategy: Callable) -> float:
    strategy = (strategy, take_one_never_finish)
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
        # genome = {"p_rule": random.random(), "p_row": random.random()}
        genome = {"aggression": random.random(), "finisher": random.random()}
        strat = make_strategy(genome)
        eval = evaluate(strat)
        r.append((eval, strat, genome))
    return r


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i[0])


def combine(population, offspring):
    population += offspring
    population = sorted(population, key=lambda i: i[0], reverse=True)[:5]
    return population


def generate_offspring(population: list) -> list:
    offspring = list()
    for i in range(OFFSPRING):
        p = tournament(population)
        p[2]["aggression"] = min(1, abs(p[2]["aggression"] + random.gauss(0, 0.1)))
        p[2]["finisher"] = min(1, abs(p[2]["finisher"] + random.gauss(0, 0.1)))
        # try:
        #     assert p[2]["p_row"] <= 1
        # except AssertionError:
        #     p[2]["p_row"] = 1
        # try:
        #     assert p[2]["p_row"] >= 0
        # except AssertionError:
        #     p[2]["p_row"] = 0
        strat = make_strategy(p[2])
        offspring.append((evaluate(strat), strat, p[2]))
    return offspring


def reevaluate(population: list) -> list:
    logging.info("Reevaluating population")
    new_population = list()
    for i in population:
        new_population.append((evaluate(i[1]), i[1], i[2]))
    return new_population


def main():
    best_fit = 0
    steady = 0
    population = generate_population(POPULATION)
    logging.info(f"Initial population: {[p[2] for p in population]}")
    for _ in range(NUM_GENERATIONS):
        logging.info(f"Generation {_}")
        offspring = generate_offspring(population)
        population = combine(population, offspring)
        logging.info(f"best genome: {population[0][2]}")
        logging.info(f"best fitness: {population[0][0]}")
        # if best_fit == population[0][0]:
        #     steady += 1
        # else:
        #     best_fit = population[0][0]
        # if steady > 7:
        #     population = reevaluate(population)
        #     steady = 0
    logging.info(f"best genome: {population[0][2]}")
    g = population[0][2]
    strat = make_strategy(g)
    rates = [evaluate(strat) for _ in range(100)]
    logging.info(f"mean rates: {sum(rates) / len(rates)}")
    # pop = generate_population(POPULATION)
    # for p in pop:
    #     logging.info(f"genome: {p[2]}")
    #     logging.info(f"fitness: {p[0]}")
    # combined = combine(pop, pop)
    # for _ in range(NUM_GENERATIONS):
    #     logging.info(f"{evaluate(combined[0][1])}")


if __name__ == "__main__":

    # g = {"aggression": 0.7010645143707598, "finisher": 0.8498425365499036}
    # s = make_strategy(g)
    # rates = [evaluate(s) for _ in range(1000)]
    # logging.info(f"mean rates: {sum(rates) / len(rates)}")
    main()
