# bron kerbosch algorithm
import random
import itertools
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)


def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


# {0: {1, 4}, 1: {0, 2, 4}, 2: {1, 3}, 3: {2, 4, 5}, 4: {0, 1, 3}, 5: {3}}


def BronKerbosch1(P, N, R=None, X=None):
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from BronKerbosch1(P=P.intersection(N[v]), N=N, R=R.union([v]), X=X.intersection(N[v]))
        X.add(v)


def main():
    K = 10
    sets = problem(K, 42)
    sets = [list(s) for s in sets]
    sets.sort()
    sets = list(k for k, _ in itertools.groupby(sets))
    sets_dict = {i: set(s) for i, s in enumerate(sets)}
    logging.debug(f"sets_dict {sets_dict}")

    adj = np.zeros((len(sets), len(sets)), dtype=int)

    for k in itertools.permutations(sets_dict.items(), 2):
        if len(k[0][1].intersection(k[1][1])) <= 0:
            logging.debug(f"no intersection between set1 : {k[0][1]} set2 : {k[1][1]}")
            logging.debug(f"k : {k}")
            logging.debug(f"i: {k[0][0]} j: {k[1][0]}")
            adj[k[0][0], k[1][0]] = 1
            adj[k[1][0], k[0][0]] = 1
            logging.debug(f"\n{adj}")

    logging.info(f"{adj}")

    N = {i: set(num for num, j in enumerate(row) if j) for i, row in enumerate(adj)}
    # logging.info(f"N {N}")
    # print(N)
    P = N.keys()
    # logging.info(f"P {P}")
    res = list(BronKerbosch1(P, N))
    logging.info(f"res {res}\n")
    for r in res:
        res_set = set()
        res_list = list()
        logging.debug(f"\nresult {r}\n")
        for s in r:
            logging.debug(f"{sets_dict[s]}")
            res_set = res_set.union(sets_dict[s])
            res_list.append(sets_dict[s])
        # logging.info(f"res_set {res_set}")
        logging.debug(f"res set :  {res_set}\nlen res_set : {len(res_set)}")
        if len(res_set) == K and (sum(len(x)) for x in res_list) == K:
            logging.info(f"global best len: {sum(len(x) for x in res_list)} \nres : {res_list}")


if __name__ == "__main__":
    main()
