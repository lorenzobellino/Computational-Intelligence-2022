import logging
import random
from collections import namedtuple

POPULATION_SIZE = 300
OFFSPRING_SIZE = 200

NUM_GENERATIONS = 100

DEBUG = False
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
# basic data structure for an individual in order to access its parameters
Individual = namedtuple("Individual", ["genome", "fitness"])


def problem(N, seed=None):
    """Creates an instance of the problem"""
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def fitness(genome, N, maxlen):
    """
    calculate the fitness of a genome
    param genome: the genome to calculate the fitness of
    param N: the size of the problem
    param maxlen: the maximum length of a list
    return: the fitness of the genome
    the fitness is a tuple containing:
        the actual fitness calculated as covered elements - a penalty for duplicates
        the number of covered elements
        the number of duplicates as a negative value (the less duplicates the better)
    """

    covered = len(set(loci for gene in genome for loci in gene))
    duplicates = len([loci for gene in genome for loci in gene]) - covered
    fitness = covered - (duplicates * N / maxlen)
    return (fitness, covered, -duplicates)


def tournament(population, tournament_size=2):
    """
    default tournament with k = 2
    select a random individual from the population
    and compare it with another random individual
    return the fittest individual
    """
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def cross_over(g1, g2):
    """
    Crossover two genomes by slicing them at a random point
    param g1: genome 1
    param g2: genome 2
    return: a new genome
    with probabiiity 0.5 the first part of g1 is combined with the second part of g2
    with probability 0.5 the first part of g2 is combined with the second part of g1
    with probability 0.3 the genome is shortened by a random amount
    """
    logging.debug(f"crossover lenghts : {len(g1)} and {len(g2)}")
    cut = random.randint(0, min(len(g1), len(g2)))
    if random.random() < 0.5:
        o = g1[:cut] + g2[cut:]
    else:
        o = g2[:cut] + g1[cut:]
    if random.random() < 0.3:
        o = o[: -random.randint(1, len(o))]
    return o


def mutation(g, all_lists):
    """
    mutate a genome by adding a random gene from all_lists
    param g: genome to mutate
    param all_lists: list of all genes
    return: mutated genome
    with probsbility 0.3 a random list is added to the genome
    with probability 0.7 a random list is substituted with another random list
    with a probability of 0.3 the genome is shortened by a random amount
    """
    logging.debug(f"mutation lenght : {len(g)}")
    point = random.randint(0, len(g) - 1)
    if random.random() < 0.3:
        o = g[:point] + (random.choice(all_lists),) + g[point:]
    else:
        o = g[:point] + (random.choice(all_lists),) + g[point + 1 :]
    if random.random() < 0.3:
        o = o[: -random.randint(1, len(o))]
    return o


def generate_population(N, all_lists, maxlen):
    """
    generate a population of POPULATION_SIZE individuals
    param N: the size of the problem
    param all_lists: the list of all possible lists
    param maxlen: the maximum length of a list
    return:
        a list of POPULATION_SIZE individuals
    """
    population = list()
    for genome in [
        tuple([random.choice(all_lists) for _ in range(random.randint(1, N // 3))]) for _ in range(POPULATION_SIZE)
    ]:
        population.append(Individual(genome, fitness(genome, N, maxlen)))
    return population


def generate_offspring(population, all_lists, N, maxlen):
    """
    param population: the current population
    param all_lists: the list of all possible lists
    param N: the size of the problem
    param maxlen: the maximum length of a list
    return: a list of offspring

    apply mutation with a probability of 0.4
    apply crossover with a probability of 0.6
    """
    offspring = list()
    for i in range(OFFSPRING_SIZE):
        if random.random() < 0.4:
            p = tournament(population)
            o = mutation(p.genome, all_lists)
        else:
            p1 = tournament(population)
            p2 = tournament(population)
            o = cross_over(p1.genome, p2.genome)
        # sometimes crossover or mutation can produce an empty genome
        if len(o) > 0:
            f = fitness(o, N, maxlen)
            offspring.append(Individual(o, f))
    return offspring


def combine(population, offspring):
    """
    combine the current population and a new one into a new population
    """
    population += offspring
    population = sorted(population, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
    return population


def setCovering(N, all_lists):
    """
    Solve the set covering problem using a genetic algorithm
    for each generation generate offspring and combine them with the population
    and then select the best individuals
    if a steady state is reached where the best_fitness doesn't change
    for 7 iteration than a reshuffle and combination with a new population is performed
    return:
        the fittest individual after NUM_GENERATIONS
    """
    maxlen = sum(len(l) for l in all_lists)
    population = generate_population(N, all_lists, maxlen)
    bestfit = population[0].fitness
    steady = 0
    for individual in population:
        logging.debug(f"Genome: {individual.genome}, Fitness: {individual.fitness}")

    for _ in range(NUM_GENERATIONS):
        offspring = generate_offspring(population, all_lists, N, maxlen)
        population = combine(population, offspring)
        steady += 1
        if population[0].fitness > bestfit:
            bestfit = population[0].fitness
            steady = 0
        if steady == 7:
            population = combine(population, generate_population(N, all_lists, maxlen))
            steady = 0

    return population[0].genome


def main():
    """
    main function used to iterate over the various problem space
    for N = [5, 10, 20, 50, 100, 200, 500, 1000]
    and logging each result found
    """
    solutions = list()
    for N in [5, 10, 20, 50, 100, 200, 500, 1000]:

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
