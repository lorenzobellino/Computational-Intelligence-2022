# Python program to print DFS traversal for complete graph
from collections import defaultdict
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Graph:
    # Constructor
    def __init__(self, num_of_nodes, directed=True):
        self.m_num_of_nodes = num_of_nodes
        self.m_nodes = range(self.m_num_of_nodes)
		
        # Directed or Undirected
        self.m_directed = directed
		
        # Graph representation - Adjacency list
        # We use a dictionary to implement an adjacency list
        self.m_adj_list = {node: set() for node in self.m_nodes}      
	
    # Add edge to the graph
    def add_edge(self, node1, node2, weight=1):
        self.m_adj_list[node1].add((node2, weight))

        if not self.m_directed:
            self.m_adj_list[node2].add((node1, weight))
    
    # Print the graph representation
    def print_adj_list(self):
        for key in self.m_adj_list.keys():
            logging.debug(f"node {key} is connected to {self.m_adj_list[key]}")

def dfs(self, start, target, path = [], visited = set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    for (neighbour, weight) in self.m_adj_list[start]:
        if neighbour not in visited:
            result = self.dfs(neighbour, target, path, visited)
            if result is not None:
                return result
    path.pop()
    return None 

def problem(N, seed=None):
    random.seed(seed)
    return [list(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2)))) for n in range(random.randint(N,N*5))]

def main():
    sets = problem(5, 42)
    graph = Graph(len(sets), directed=False)
    sets = [set(s) for s in sets]
    set_dict = {''.join(str(s)): i for i, s in enumerate(sets)}
    print(set_dict.values())
    print(set_dict)
    # for s1 in sets:
    #     for s2 in sets:
    #         logging.debug(f"set1 {s1} set2 {s2}")
    #         if s1.intersection(s2) == 0:
    #             logging.debug(f"adding edge between {s1} and {s2}")
    #             graph.add_edge(''.join(str(_) for _ in s1), ''.join(str(_) for _ in s2))
    # graph.print_adj_list() 


if __name__ == '__main__':
    main()


# def dfs(graph, start, visited=None):
#     if visited is None:
#         visited = set()
#     visited.add(start)

#     print(start)

#     for next in graph[start] - visited:
#         dfs(graph, next, visited)
#     return visited


# graph = {'0': set(['1', '2']),
#          '1': set(['0', '3', '4']),
#          '2': set(['0']),
#          '3': set(['1']),
#          '4': set(['2', '3'])}

# dfs(graph, '0')