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
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

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


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.xor)
    return result


def brute_force(state: Nim) -> dict:
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
    data = brute_force(state)
    # logging.info(f"brute_force: {[bf for bf in data['brute_force'] if bf[1] == 0]}")
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def sub_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, operator.sub)
    return result


def nand_operation(state: Nim) -> int:
    *_, result = accumulate(state.rows, lambda x, y: ~(x & y))
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


def cook_data(state: Nim) -> dict:
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
    print(state)
    row = int(input("row: "))
    num_objects = int(input("num_objects: "))
    return Nimply(row, num_objects)


def five_param_5(state: Nim) -> Nimply:
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
    # logging.info(f"res: {r}")

    return ply


def four_param_5(state: Nim) -> Nimply:
    """
    My best player with 4 parameters
    param state: Nim
    return: Nimply
    """
    genome = {
        "alpha": 12.812770589035535,
        "beta": -16.051123920350758,
        "gamma": -0.20956437443764508,
        "delta": -8.234717910949916,
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


def five_param_generalized(state: Nim) -> Nimply:
    """
    My best player with 5 parameters
    param state: Nim
    return: Nimply
    """
    genome = {
        "alpha": 44.79077594400001,
        "beta": 9.579669386437583,
        "gamma": -5.209762203134689,
        "delta": -9.489475946977137,
        "epsilon": -31.18441371362716,
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
    # logging.info(f"res: {r}")

    return ply


def four_param_generalized(state: Nim) -> Nimply:
    """
    My best player with 4 parameters
    param state: Nim
    return: Nimply
    """
    # genome = {
    #     "alpha": 14.325827789108999,
    #     "beta": -5.726164045356429,
    #     "gamma": -31.566080375138124,
    #     "delta": 13.98406203443887,
    # }
    genome = {
        "alpha": 15.945309194204931,
        "beta": -3.2707966609771746,
        "gamma": -25.708257470959275,
        "delta": 14.81947128092396,
    }
    # genome = {
    #     "alpha": -4.645104370303834,
    #     "beta": 47.72918882837766,
    #     "gamma": 43.87787924034255,
    #     "delta": -24.54257046414698,
    # }
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


# g = {
#         "alpha": 27.351780660982282,
#         "beta": -28.237181399793418,
#         "gamma": 0.9860754279733916,
#         "delta": -14.512063824459766,
#         "epsilon": -0.8929601820986557,
#     }
# g2 = {
#     "alpha": 5.037826023749055,
#     "beta": -10.02468726136403,
#     "gamma": -17.368288381365883,
#     "delta": -2.410386155997915,
#     "epsilon": 12.070941357941306,
# }

# g = {
#     "alpha": -44.27662494134977,
#     "beta": 16.015621798236584,
#     "gamma": -24.56222874316719,
#     "delta": -9.810647648567455,
#     "epsilon": -45.866381222978845,
# }
# g = {
#     "alpha": -48.75023496900495,
#     "beta": 14.68781293493512,
#     "gamma": -35.44699332992186,
#     "delta": -30.678349749800727,
#     "epsilon": -40.7035928942382,
# }
# g = {
#     "alpha": -83.06433328890463,
#     "beta": 76.1920177881244,
#     "gamma": -48.281040978815525,
#     "delta": -44.23878759913666,
#     "epsilon": -28.141856716301803,
# }
# g = {
#     "alpha": -42.5399485484396,
#     "beta": 114.60961375796023,
#     "gamma": -52.64808867035252,
#     "delta": 0.49668038593870456,
#     "epsilon": 18.15686871650329,
# }
# g = {
#         "alpha": -48.670844702347786,
#         "beta": 53.66983929673961,
#         "gamma": -13.982427278443428,
#         "delta": 10.898632957633824,
#         "epsilon": -2.766685298738114,
#     }

# g = {
#     "alpha": -0.3450015759969851,
#     "beta": -20.616277242751178,
#     "gamma": 12.110141311979866,
#     "delta": 2.5664402069601033,
# }
# genome = {
#         "alpha": 26.97877500272968,
#         "beta": 17.850212657051426,
#         "gamma": 11.554805573206878,
#         "delta": 8.903361191261782,
#     }
