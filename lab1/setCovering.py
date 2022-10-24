import random
import logging
from itertools import groupby
from queue import PriorityQueue
from time import perf_counter_ns
from math import ceil

SEED = 42

logging.basicConfig(format="%(message)s", level=logging.INFO)


def problem(N, seed=None):
    """Generate a random problem given a seed
    ...
    Attributes :
        N : int
            The number of elements in the universe
        seed : int
            The seed for the random number generator
            default value = 42
    """
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def calculate_weight(result, goal, set_=set(), threshold=1):
    """Calculate the weight of a set
    ...
    Attributes :
        result : set
            The set of elements already covered
        goal : set
            The set of elements to cover
        set_ : set
            The set to evaluate
            default value = set()
        threshold : float
            The threshold for the weight
            default value = 1
    """
    # weight = the percentage of new elements covered by the set in respect to the state of the solution
    weight = ceil(100 * sum(x in goal - result for x in set_) / len(set_))
    # return 0 if weight >= threshold * 100 else 100 - weight
    return 100 if weight >= threshold * 100 else weight


def search(sets, goal, N, threshold=1):
    """Search for a solution to the set covering problem
    ...
    Attributes :
        sets : list
            The list of sets
        goal : set
            The set of elements to cover
        N : int
            The number of elements in the universe
        threshold : float
            The threshold for the weight
            default value = 1
    """
    discovered_state = 0
    options = PriorityQueue()
    unused = PriorityQueue()
    # added a precomputing step:
    # remove empty lists and remove duplicates
    sets = [s for s in sets if s]
    sets = list(sets for sets, _ in groupby(sets))

    for element in sets:
        options.put((100 - int(100 * len(element) / N), element))
    result = [options.get()[-1]]
    result_set = set().union(result[0])
    while result is not None and not result_set == goal:
        while not options.empty():  # until i have options extract an element
            discovered_state += 1
            s = options.get()[-1]
            coverage = calculate_weight(result_set, goal, s, threshold)
            if coverage == 100:  # if all the elements in the set are new to the solution
                result.append(s)  # add it to the solution
                result_set = result_set.union(s)
                while not unused.empty():  # reinsert unused sets in the options queue
                    options.put(unused.get())
                break
            if coverage != 0:  # if the coverage is > 0% insert it in the unused queue
                unused.put((100 - coverage, s))
        else:  # after checking all options
            if unused.empty():  # if there are no unused sets a result can not be reached
                result = None
                break
            local_best = unused.get()[-1]  # extract the locally best unused set
            result.append(local_best)  # append it to the solution
            result_set = result_set.union(local_best)
            while not unused.empty():
                options.put(unused.get())  # reinsert unused sets in the options queue
    logging.info(f"explored state: {discovered_state}")
    return result


def main():
    """Main function"""
    for n in [5, 10, 20, 50, 100, 500, 1000]:
        sets = problem(n, SEED)
        goal = set(_ for _ in range(n))
        logging.info(f"N = {n}")
        start_time_ns = perf_counter_ns()
        result = search(sets, goal, n, threshold=1)
        end_time_ns = perf_counter_ns()
        logging.info(f"Time: {end_time_ns-start_time_ns} ns")
        if result is None:
            logging.info("No solution found")
        else:
            logging.info(f"the weight of the solution is: {sum(len(s) for s in result)}")


if __name__ == "__main__":
    main()
