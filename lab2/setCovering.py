import random
import logging

PROBLEM_SIZE = 500
POPULATION_SIZE = 5
OFFSPRING_SIZE = 3

NUM_GENERATIONS = 100

DEBUG = True
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)


def problem(N, seed=None):
    """Creates an instance of the problem"""

    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def setCovering(N, problem):
    return [[0]]


def main():
    for N in [5, 10, 20, 50, 100, 200, 500, 1000]:
        solution = setCovering(N, problem(N, seed=42))
        logging.info(
            f" Solution for N={N:,}: "
            + f"w={sum(len(_) for _ in solution):,} "
            + f"(bloat={(sum(len(_) for _ in solution)-N)/N*100:.0f}%)"
        )


if __name__ == "__main__":
    main()
