import random
import logging
from collections import namedtuple

# PROBLEM_SIZE = 500
POPULATION_SIZE = 100
OFFSPRING_SIZE = 50

NUM_GENERATIONS = 20

DEBUG = False
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)


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


def reduceSize(population, N):
    Individual = namedtuple("Individual", ["genome", "fitness"])
    new_population = list()
    for individual in population:
        randPoint = random.randint(0, len(individual.genome) - 1)
        o = individual.genome[:randPoint] + individual.genome[randPoint + 1 :]
        new_population.append(Individual(genome=o, fitness=fitness(o, N)))
    return sorted(new_population, key=lambda i: i.fitness, reverse=True)


def fitness(genome, N):
    covered = len(set(loci for gene in genome for loci in gene))
    # logging.debug(f"Covered: {covered}")
    duplicates = len([loci for gene in genome for loci in gene]) - covered
    # logging.debug(f"Duplicates: {duplicates}")
    l = len([loci for gene in genome for loci in gene])
    # logging.debug(f"Length: {l}")
    # return covered - ((duplicates * 100) // N)
    return (covered, -duplicates)


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def cross_over(g1, g2):
    """Crossover two genomes by slicing them at a random point"""
    # cut = random.randint(0, PROBLEM_SIZE)
    cut = random.randint(0, min(len(g1), len(g2)))
    o = g1[:cut] + g2[cut:]
    # if random.random() < 0.7:
    #     o = g1[:cut] + g2[cut:]
    # else:
    #     o = g1 + g2
    return o


def mutation(g, all_lists):
    """Mutate a genome  by swapping a random list from the original problem"""
    point = random.randint(0, len(g) - 1)
    o = g[:point] + (random.choice(all_lists),) + g[point + 1 :]
    # if random.random() < 0.3:
    #     o = g[:point] + (random.choice(all_lists),) + g[point + 1 :]
    # else:
    #     o = g[:point] + (random.choice(all_lists),) + g[point:]
    return o


def setCovering(N, all_lists):
    Individual = namedtuple("Individual", ["genome", "fitness"])
    population = list()
    fitness_log = [(0, i.fitness) for i in population]
    for genome in [
        tuple([random.choice(all_lists) for _ in range(random.randint(1, N // 2))]) for _ in range(POPULATION_SIZE)
    ]:
        population.append(Individual(genome, fitness(genome, N)))
    for individual in population:
        logging.debug(f"Genome: {individual.genome}, Fitness: {individual.fitness}")
    for g in range(NUM_GENERATIONS):
        offspring = list()
        for i in range(OFFSPRING_SIZE):
            # if random.random() < 0.3:
            #     p1 = tournament(population)
            #     p2 = tournament(population)
            #     p1_mutation = mutation(p1.genome, all_lists)
            #     p2_mutation = mutation(p2.genome, all_lists)
            #     o = cross_over(p1_mutation, p2_mutation)
            # else:
            #     p = tournament(population)
            #     o = mutation(p.genome, all_lists)

            if random.random() < 0.4:
                p = tournament(population)
                o = mutation(p.genome, all_lists)
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = cross_over(p1.genome, p2.genome)
            f = fitness(o, N)
            # logging.debug(f"Fitness: {f}")
            fitness_log.append((g + 1, f))

            offspring.append(Individual(o, f))
        population += offspring
        population = sorted(population, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
        logging.debug(f"Generation: {g}")
        printPop(population)
        if population[0].fitness[1] == 0:
            break
        if population[0].fitness[1] < -N // 2:
            logging.debug("Reducing size")
            population = reduceSize(population, N)

    # for individual in population:
    #     logging.info(f"Genome: {individual.genome}, Fitness: {individual.fitness}")
    return population[0].genome


def main():
    # for N in [5, 10, 20, 50, 100, 200, 500, 1000]:
    solutions = list()
    for N in [5, 10, 20, 50, 100, 200, 500, 1000]:
        solution = setCovering(N, problem(N, seed=42))
        # solution = setCovering(N,problem(N,seed=42))
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
