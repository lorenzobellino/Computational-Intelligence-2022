import logging
import random
import operator
from collections import namedtuple
from itertools import accumulate
from copy import deepcopy


Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        # self._rows = [i + 1 for i in range(num_rows)]
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


def gabriele(state: Nim) -> Nimply:
    """
    Player that picks always the maximum number of objects from the lowes row
    param state: Nim
    return: Nimply
    """
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def take_one_never_finish(State: Nim) -> Nimply:
    """
    Player that always take one object without finishing a row if it is possible
    param state: Nim
    return: Nimply
    """
    try:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 1][0]
    except IndexError:
        move = [(r, o) for r, o in enumerate(State.rows) if o > 0][0]
    return Nimply(*move)


def pure_random(state: Nim) -> Nimply:
    """
    Pure random player, pick a random move between all the possible moves
    param state: Nim
    return: Nimply
    """
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def nim_sum(state: Nim) -> int:
    """
    Player with the optimal strategy
    param state: Nim
    return: result: int, the nim sum of the state
    """
    *_, result = accumulate(state.rows, operator.xor)
    return result


def brute_force(state: Nim) -> dict:
    """
    Apply the nimSum to all the possible moves and return a dictionary with the possible moves and the nim sum
    param state: Nim
    return: dict
    """
    bf = list()
    data = dict()
    possible_moves = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    for m in possible_moves:
        tmp = deepcopy(state)
        tmp.nimming(m)
        bf.append((m, nim_sum(tmp)))
    data["brute_force"] = bf
    return data


def optimal_startegy(state: Nim) -> Nimply:
    """
    Player with the optimal strategy (nimSum)
    param state: Nim
    return: Nimply
    """
    data = brute_force(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def sub_operation(state: Nim) -> int:
    """
    Perform the sub operation between the row's objects
    param state: Nim
    return: result: int, the sub operation of the state
    """
    *_, result = accumulate(state.rows, operator.sub)
    return result


def nand_operation(state: Nim) -> int:
    """
    Perform the nand operation between the row's objects
    param state: Nim
    return: result: int, the nand operation of the state
    """
    *_, result = accumulate(state.rows, lambda x, y: ~(x & y))
    return result


def and_operation(state: Nim) -> int:
    """
    Perform the and operation between the row's objects
    param state: Nim
    return: result: int, the and operation of the state
    """
    *_, result = accumulate(state.rows, operator.and_)
    return result


def or_operation(state: Nim) -> int:
    """
    Perform the or operation between the row's objects
    param state: Nim
    return: result: int, the or operation of the state
    """
    *_, result = accumulate(state.rows, operator.or_)
    return result


def nim_sum(state: Nim) -> int:
    """
    Perform the nim sum operation between the row's objects
    param state: Nim
    return: result: int, the nim sum operation of the state
    """
    *_, result = accumulate(state.rows, operator.xor)
    return result


def cook_data(state: Nim) -> dict:
    """
    Apply all the possible operation to the state and return a dictionary with the possible moves and the result of the operations
    param state: Nim
    return: dict
    """
    data = dict()
    and_list = list()
    or_list = list()
    sum_list = list()
    sub_list = list()
    nand_list = list()
    possible_moves = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state._k is None or o <= state._k
    ]
    for m in possible_moves:
        tmp = deepcopy(state)
        tmp.nimming(m)
        and_list.append((m, and_operation(tmp)))
        or_list.append((m, or_operation(tmp)))
        sum_list.append((m, sum(tmp.rows)))
        sub_list.append((m, sub_operation(tmp)))
        nand_list.append((m, nand_operation(tmp)))

    data["and"] = and_list
    data["or"] = or_list
    data["sum"] = sum_list
    data["sub"] = sub_list
    data["nand"] = nand_list

    return data


def human_player(state: Nim) -> Nimply:
    """Human player
    param state: Nim
    return: Nimply
    """
    logging.info(f"\n{state}")
    row = int(input("row: "))
    num_objects = int(input("num_objects: "))
    return Nimply(row, num_objects)


def five_parameters_player(state: Nim) -> Nimply:
    """
    My best player with 5 parameters
    param state: Nim
    return: Nimply
    """
    genome = {
        "alpha": -42.5399485484396,
        "beta": 114.60961375796023,
        "gamma": -52.64808867035252,
        "delta": 0.49668038593870456,
        "epsilon": 18.15686871650329,
    }
    data = cook_data(state)
    res = (
        (
            a[0],
            abs(
                genome["alpha"] * a[1]
                + genome["beta"] * b[1]
                + genome["gamma"] * c[1]
                + genome["delta"] * d[1]
                + genome["epsilon"] * e[1]
            ),
        )
        for a, b, c, d, e in zip(data["and"], data["or"], data["sum"], data["sub"], data["nand"])
    )
    ply, r = min(res, key=lambda x: x[1])
    logging.info(f"res: {r}")

    return ply


def four_parameters_player(state: Nim) -> Nimply:
    """
    My best player with 4 parameters
    param state: Nim
    return: Nimply
    """
    genome = {
        "alpha": 26.97877500272968,
        "beta": 17.850212657051426,
        "gamma": 11.554805573206878,
        "delta": 8.903361191261782,
    }
    data = cook_data(state)
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
