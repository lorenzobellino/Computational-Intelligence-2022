import random
import logging
from collections import namedtuple

# PROBLEM_SIZE = 500
POPULATION_SIZE = 1500
OFFSPRING_SIZE = 1000

NUM_GENERATIONS = 100

DEBUG = False
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

Individual = namedtuple("Individual", ["genome", "fitness"])
"""
1000 GENERATIONS
INFO:root: Solution for N=5: w=5 (bloat=0%)
INFO:root: Solution for N=10: w=10 (bloat=0%)
INFO:root: Solution for N=20: w=24 (bloat=20%)
INFO:root: Solution for N=50: w=81 (bloat=62%)
INFO:root: Solution for N=100: w=185 (bloat=85%)
INFO:root: Solution for N=200: w=460 (bloat=130%)
INFO:root: Solution for N=500: w=1,444 (bloat=189%)
INFO:root: Solution for N=1,000: w=3,465 (bloat=246%)
"""


def printPop(population):
    for individual in population:
        # logging.debug(f"Genome: {individual.genome}, Fitness: {individual.fitness}")
        logging.debug(f"Fitness: {individual.fitness}")


def problem(N, seed=None):
    """Creates an instance of the problem"""
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def fitness(genome, N, maxlen):
    covered = len(set(loci for gene in genome for loci in gene))
    duplicates = len([loci for gene in genome for loci in gene]) - covered
    fitness = covered - (duplicates * N / maxlen)
    # fitness = covered - duplicates
    # return (covered, -duplicates)
    # if covered != N:
    #     fitness -= 1
    return fitness


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def cross_over(g1, g2):
    """Crossover two genomes by slicing them at a random point"""
    g = g1 + g2
    point = random.randint(1, len(g) - 1)
    if random.random() < 0.5:
        o = g[:point]
    else:
        o = g[point:]
    return o


def mutation(g, all_lists):
    point = random.randint(0, len(g) - 1)
    if random.random() < 0.7:
        o = g[:point] + (random.choice(all_lists),) + g[point:]
    else:
        o = g[:point] + (random.choice(all_lists),) + g[point + 1 :]
    return o


def generate_population(N, all_lists, maxlen):
    population = list()
    for genome in [
        tuple([random.choice(all_lists) for _ in range(random.randint(1, N))]) for _ in range(POPULATION_SIZE)
    ]:
        population.append(Individual(genome, fitness(genome, N, maxlen)))
    return population


def generate_offspring(population, all_lists, N, maxlen):
    offspring = list()
    for i in range(OFFSPRING_SIZE):
        if random.random() < 0.4:
            p = tournament(population)
            o = mutation(p.genome, all_lists)
        else:
            p1 = tournament(population)
            p2 = tournament(population)
            o = cross_over(p1.genome, p2.genome)
        f = fitness(o, N, maxlen)

        offspring.append(Individual(o, f))
    return offspring


def combine(population, offspring):
    population += offspring
    population = sorted(population, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
    return population


def reshuflle(population, all_lists, N, maxlen):
    new_population = list()
    for i in population:
        new_len = random.randint(1, len(i.genome))
        # logging.info(f"new_len: {new_len}")
        try:
            o = tuple(random.sample(i.genome, new_len))
        except ValueError:
            logging.info(f"ValueError: {i.genome}")
            # o = i.genome
        new_population.append(Individual(o, fitness(o, N, maxlen)))
    return new_population


def setCovering(N, all_lists):
    """Solve the set covering problem using a genetic algorithm"""
    maxlen = sum(len(l) for l in all_lists)
    population = generate_population(N, all_lists, maxlen)

    for individual in population:
        logging.debug(f"Genome: {individual.genome}, Fitness: {individual.fitness}")

    for _ in range(NUM_GENERATIONS):
        offspring = generate_offspring(population, all_lists, N, maxlen)
        population = combine(population, offspring)
        logging.debug(f"best fitness: {population[0].fitness}")
        # if population[0].fitness[0] == N and population[0].fitness[1] == 0:
        #     break

    return population[0].genome


def main():
    solutions = list()
    for N in [5, 10, 20, 50, 100, 200, 500, 1000]:
        # for N in [20]:
        solution = setCovering(N, problem(N, seed=42))
        solutions.append(solution)
        logging.info(
            f" Solution for N={N:,}: "
            + f"w={sum(len(_) for _ in solution):,} "
            + f"(bloat={(sum(len(_) for _ in solution)-N)/N*100:.0f}%)"
        )
    for s in solutions:
        flat = [i for a in s for i in a]
        logging.debug(f"Solution: {sorted(flat)}")


if __name__ == "__main__":
    main()
