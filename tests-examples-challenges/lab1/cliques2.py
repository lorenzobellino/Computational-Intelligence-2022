from pydoc import cli
import random
from itertools import groupby,permutations,combinations
import logging
# from types import NoneType
import networkx as nx
from threading import Thread

K = 10
SEED = 42
BEST_W = K**K

logging.basicConfig(level=logging.INFO)

def problem(N, seed=None):
    random.seed(seed)
    return [list(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2)))) for n in range(random.randint(N,N*5))]

def k_cliques(graph):
    # 2-cliques
    cliques = [{i, j} for i, j in graph.edges() if i != j]
    k = 2

    while cliques:
        # result
        yield k, cliques

        # merge k-cliques into (k+1)-cliques
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            # if(BEST_W == K):
            #     break
            w = u ^ v
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))

        # remove duplicates
        cliques = list(map(set, cliques_1))
        k += 1

def cliques(graph,sets_dict):
    # logging.debug(f"cliques for size {size_k}")
    clq = {}
    threads = []
    for k, cliques in k_cliques(graph):
        # if k == size_k:
        #     # print('%d-cliques = %d, %s.' % (k, len(cliques), cliques))
        #     return cliques
        # logging.debug(f"cliques of size {k}: {cliques}")
        if(BEST_W == K):
            break
        logging.debug(f"k = {k}")
        t = Thread(target = task, args = (k,cliques,sets_dict))
        threads.append(t)
        t.start()
        clq[k]=cliques
    
    for t in threads:
        t.join()
    return clq

def task(k,cliques,sets_dict):
    global BEST_W
    logging.debug(f"cliques of size {k}")
    res_set = set()
    res_list = list()
    # logging.info(f"cliques of sixe k : {k}")
    # logging.info(f"checking {len(cliques)} possible solution")
    # best_w = K**K
    for s in cliques:
        res_set = set()
        res_list = list()
        for i in s:
            res_set = res_set.union(sets_dict[i])
            res_list.append(sets_dict[i])
        logging.debug(f"res_set: {res_set}")
        logging.debug(f"res_list: {res_list}")
        coverage = len(res_set)
        logging.debug(f"coverage: {coverage}")
        weight = sum(len(x) for x in res_list)
        if(coverage == K):
            if(weight < BEST_W):
                BEST_W = weight
                if(BEST_W == K):
                    found = True
                    logging.info(f"new best weight : {BEST_W}")
                    logging.info(f"global best len: {sum(len(x) for x in res_list)} \nres : {res_list}")
                    break
                BEST_W = weight
                logging.info(f"new best weight : {BEST_W}")
                logging.info(f"local best len: {sum(len(x) for x in res_list)} \nres : {res_list}")
logging.info(f"no solution with weight = {K} found for k = {K}")


def main():

    sets = problem(K, SEED)
    # sets = [[1,2,3,4],[0,1,2,3],[0,1,3,4]]
    sets = [list(s) for s in sets]
    sets.sort()
    sets = list(k for k,_ in groupby(sets))
    sets_dict = {i: set(s) for i, s in enumerate(sets)}
    graph = nx.Graph()
    graph.add_nodes_from(range(len(sets)))

    for z in permutations(sets_dict.items(), 2):
        if(len(z[0][1].intersection(z[1][1])) <= 5):
            graph.add_edge(z[0][0],z[1][0])
            graph.add_edge(z[1][0],z[0][0])
    logging.debug(f"edges : {graph.edges()}")
    logging.debug(f"sets_dict: {sets_dict}")
    partial_res = cliques(graph,sets_dict)
    # found = False
    # c = 1
    # best_w = K**K

    # partial_res = cliques(graph,sets_dict)
    # logging.info(f"keys: {partial_res.keys()}")
    # if partial_res is not None and not found:
    #     # logging.debug(f"partial_res: {partial_res.items()}")
    #     for k,c in partial_res.items():
    #         res_set = set()
    #         res_list = list()
    #         logging.info(f"cliques of sixe k : {k}")
    #         logging.info(f"checking {len(c)} possible solution")
    #         for s in c:
    #             res_set = set()
    #             res_list = list()
    #             for i in s:
    #                 res_set = res_set.union(sets_dict[i])
    #                 res_list.append(sets_dict[i])
    #             logging.debug(f"res_set: {res_set}")
    #             logging.debug(f"res_list: {res_list}")
    #             coverage = len(res_set)
    #             weight = sum(len(x) for x in res_list)
    #             if(coverage == K):
    #                 if(weight < best_w):
    #                     best_w = weight
    #                     if(best_w == K):
    #                         found = True
    #                         logging.info(f"new best weight : {best_w}")
    #                         logging.info(f"global best len: {sum(len(x) for x in res_list)} \nres : {res_list}")
    #                         exit()
    #                     best_w = weight
    #                     logging.info(f"new best weight : {best_w}")
    #                     logging.info(f"local best len: {sum(len(x) for x in res_list)} \nres : {res_list}")
    #     logging.info(f"no solution with weight = K found")


if __name__ == '__main__':
    main()