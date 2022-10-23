
from pydoc import cli
import random
from itertools import groupby,permutations,combinations
import logging
from types import NoneType
import matplotlib.pyplot as plt
import networkx as nx

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
            w = u ^ v
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))

        # remove duplicates
        cliques = list(map(set, cliques_1))
        k += 1


def cliques(graph, size_k):
    # logging.debug(f"cliques for size {size_k}")
    for k, cliques in k_cliques(graph):
        if k == size_k:
            # print('%d-cliques = %d, %s.' % (k, len(cliques), cliques))
            return cliques

def main():
    K = 5
    sets = problem(K, 42)
    sets = [list(s) for s in sets]
    sets.sort()
    sets = list(k for k,_ in groupby(sets))
    sets_dict = {i: set(s) for i, s in enumerate(sets)}
    graph = nx.Graph()
    graph.add_nodes_from(range(len(sets)))
    
    for z in permutations(sets_dict.items(), 2):
        if(len(z[0][1].intersection(z[1][1])) <= 0):
            graph.add_edge(z[0][0],z[1][0])
            graph.add_edge(z[1][0],z[0][0])
    found = False
    c = 1
    best_w = K*K

    # nx.draw(graph)
    # plt.draw()
    # plt.how()
    while not found and c < K:
        c+=1
        
        partial_res = cliques(graph, c)
        if partial_res is not None:
            logging.debug(f"for c = {c} found {len(partial_res)} cliques")
            logging.debug(f"partial res = {partial_res}")
        else:
                logging.debug(f"for c = {c} found 0 cliques")
        if partial_res is not None:
            for r in partial_res:
                logging.debug(f"r = {r}")
                res_set = set()
                res_list = list()
                # logging.debug(f"\nresult {r}\n")
                for s in r:
                    # logging.debug(f"{sets_dict[s]}")
                    res_set = res_set.union(sets_dict[s])
                    res_list.append(sets_dict[s])
                # logging.info(f"res_set {res_set}")
                # logging.debug(f"{res_list}")
                # logging.debug(f"{sum(len(x) for x in res_list)}")
                # if(len(res_set) == K and (sum(len(x) for x in res_list)) == K):
                if(len(res_set) == K and (sum(len(x) for x in res_list)) < best_w):
                    logging.info(f"global best len: {sum(len(x) for x in res_list)} \nres : {res_list}")
                    best_w = sum(len(x) for x in res_list)
                    if best_w == K:
                        found = True
                        break
                    #found = True
                    #break
    
    logging.info(f"c : {c}")

if __name__ == '__main__':
    main()