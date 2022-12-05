import operator
import logging
from opponents import Nim, Nimply

# from operator import and_, or_, sub
from itertools import accumulate
from copy import deepcopy

logging.basicConfig(level=logging.INFO)


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
    logging.info(f"res: {r}")

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
    logging.info(f"res: {r}")

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
