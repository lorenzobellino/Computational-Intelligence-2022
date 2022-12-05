import logging
import random
from collections import namedtuple
from typing import Callable
from copy import deepcopy
from itertools import accumulate
import operator
from math import ceil


logging.getLogger().setLevel(logging.DEBUG)

NUM_MATCHES = 100
NIM_SIZE = 11
POPULATION = 7
NUM_GENERATIONS = 20
OFFSPRING = 4
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
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    # cooked["r-shift"] = lshift_operation(Nim)
    and_list = list()
    or_list = list()
    sum_list = list()
    rshift_list = list()
    lshift_list = list()
    brute_force = list()

    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        and_list.append((m, and_operation(tmp)))
        or_list.append((m, or_operation(tmp)))
        sum_list.append((m, sum(tmp.rows)))
        rshift_list.append((m, rshift_operation(tmp)))
        lshift_list.append((m, lshift_operation(tmp)))

        # brute_force.append((m, nim_sum(tmp)))
    # cooked["brute_force"] = brute_force
    cooked["and"] = and_list
    cooked["or"] = or_list
    cooked["sum"] = sum_list
    cooked["r-shift"] = rshift_list
    cooked["l-shift"] = lshift_list

    return cooked


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


def nand_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.nand)
    return result


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.xor)
    return result


def make_strategy(genome: dict) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        # logging.debug(f"and operation = {data['and']}")
        # logging.debug(f"or operation = {data['or']}")

        # alpha beta gamma
        # return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]

        alpha = genome["alpha"]
        beta = genome["beta"]
        gamma = genome["gamma"]
        delta = genome["delta"]
        epsilon = genome["epsilon"]

        # res = (alpha * a[1] for a in data["and"])

        res = (
            (a[0], abs(alpha * a[1] + beta * b[1] + gamma * c[1] + delta * d[1] + epsilon * e[1]))
            for a, b, c, d, e in zip(data["and"], data["or"], data["sum"], data["r-shift"], data["l-shift"])
        )

        # for a, b, g, d, e in zip(data["and"], data["or"], data["sum"], data["r-shift"], data["l-shift"]):
        #     res = (
        #         (a[0], alpha * a[1] + beta * b[1] + gamma * g[1] + delta * d[1] + epsilon * e[1])
        #         for a, b, g in zip(data["and"], data["or"], data["sum"])
        #     )

        # for r in res:
        #     print(r)

        # logging.debug(f"res = {[x for x in res]}")

        # ply = next(r[0] for r in res if r[1] == 0)
        ply = min(res, key=lambda x: x[1])[0]
        # ply = (0, 1)
        # logging.debug(f"ply = {ply}")
        # input()
        return ply

    return evolvable


def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
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


def optimal_startegy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def evaluate(strategy: Callable) -> float:
    strategy = (strategy, pure_random)
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
            "alpha": random.uniform(-2, 2),
            "beta": random.uniform(-2, 2),
            "gamma": random.uniform(-2, 2),
            "delta": random.uniform(-2, 2),
            "epsilon": random.uniform(-2, 2),
        }
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
        p[2]["alpha"] += random.uniform(-0.1, 0.1)
        p[2]["beta"] += random.uniform(-0.1, 0.1)
        p[2]["gamma"] += random.uniform(-0.1, 0.1)
        p[2]["delta"] += random.uniform(-0.1, 0.1)
        p[2]["epsilon"] += random.uniform(-0.1, 0.1)

        # p[2]["aggression"] = min(1, abs(p[2]["aggression"] + random.gauss(0, 0.1)))
        # p[2]["finisher"] = min(1, abs(p[2]["finisher"] + random.gauss(0, 0.1)))
        strat = make_strategy(p[2])
        offspring.append((evaluate(strat), strat, p[2]))
    return offspring


def evaluate_with_opponent(strategy: Callable, opponent: Callable) -> float:
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


def main():
    population = generate_population(POPULATION)
    logging.info(f"Initial population: {[p[2] for p in population]}")
    for _ in range(NUM_GENERATIONS):
        logging.info(f"Generation {_}")
        offspring = generate_offspring(population)
        population = combine(population, offspring)
        logging.info(f"best genome: {population[0][2]}")
        logging.info(f"best fitness: {population[0][0]}")

    logging.info(f"best genome: {population[0][2]}")

    # g1 = {"alpha": 0.16674059884417405, "beta": 0.5579600063711714, "gamma": -0.6762883733032438}
    # g2 = {"alpha": 0.7006602735647531, "beta": -0.8007556378776335, "gamma": 0.5085499446714038}
    # strat1 = make_strategy(g1)
    # strat2 = make_strategy(g2)

    strat = make_strategy(population[0][2])
    matches = 1

    r1 = (
        sum([evaluate_with_opponent(strat, take_one_never_finish) for _ in range(matches)])
        * 100
        / (NUM_MATCHES * matches)
    )
    logging.info(f"R1 DONE")
    r2 = sum([evaluate_with_opponent(strat, gabriele) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    logging.info(f"R2 DONE")
    r3 = sum([evaluate_with_opponent(strat, pure_random) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    logging.info(f"R3 DONE")

    rates = (r1, r2, r3)
    logging.info(f"victories : {rates}")

    # # r4 = sum([evaluate_with_opponent(strat, optimal_startegy) for _ in range(matches)]) * 100 / (NUM_MATCHES * matches)
    # # logging.info(f"R4 DONE")

    # rates = (r1, r2, r3)

    # res = evaluate_with_opponent(gabriele, pure_random)

    # logging.info(f"res: {res}")

    # BEST PERFORMER SO FAR
    # g = {"alpha": 0.7006602735647531, "beta": -0.8007556378776335, "gamma": 0.5085499446714038}
    # strat = make_strategy(g)


if __name__ == "__main__":

    main()
