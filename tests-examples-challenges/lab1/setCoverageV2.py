import logging
from queue import PriorityQueue
import random
from collections import deque
from utility import *
from typing import Callable
from copy import deepcopy
N = 20
seed = 42

class State:
    def __init__(self, data: tuple):
        self._data = deepcopy(data)
        #self._data.flags.writeable = False

    def __hash__(self):
        return hash(bytes(self._data))

    def __eq__(self, other):
        return bytes(self._data) == bytes(other._data)

    def __lt__(self, other):
        return bytes(self._data) < bytes(other._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    @property
    def data(self):
        return self._data

    def copy_data(self):
        return deepcopy(self._data)

class Key:
    def __init__(self, state: State):
        self.data = state.data[0]
    def __hash__(self):
        return hash(bytes(self.data))
    def __eq__(self, other):
        return self.data == other.data


def goal_test(state : State, goal:list):
    # flat_list = [item for sublist in state for item in sublist]
    #s = state.data()
    fl = set(state.data[0])
    # return set(goal) == set(flat_list)
    return set(goal) == fl

def problem(N, seed=None):
    random.seed(seed)
    bag = [list(set(random.randint(0,N-1) for n in range(random.randint(N // 5, N // 2)))) for n in range(random.randint(N,N*5))]
    goal = [_ for _ in range(N)]
    s = State(((),tuple(bag)))
    return s,goal

def possible_actions(state: State):
    return state.data[1]

def result(state: State, action):
    new_state = state.copy_data()
    new_state[0] += (action,)
    new_state[1] = tuple([a for a in new_state[1] if a != action])
    return State(new_state)

def search(
    initial_state: State,
    goal: list,
    goal_test: Callable,
    parent_state: dict,
    state_cost: dict,
    priority_function: Callable,
    unit_cost: Callable,
):
    '''initial_state: the initial state of the problem
    goal_test: a function that takes a state and returns True if the state is a goal state
    parent_state: a dictionary that maps a state to its parent state
    state_cost: a dictionary that maps a state to its cost
    priority_function: a function that takes a state and returns its priority
    unit_cost: a function that takes two states and returns the cost of moving from the first state to the second state'''

    frontier = PriorityQueue()
    parent_state.clear()
    state_cost.clear()
    k = Key(initial_state)
    state = initial_state
    logging.debug(f"{type(state)}")
    parent_state[k] = None
    state_cost[k] = 0
    print(type(initial_state))
    print(goal_test(state, goal))
   
    while state is not None and not goal_test(state, goal):
        for a in possible_actions(state):
            new_state = result(state, a)
            cost = unit_cost(a)
            if new_state not in state_cost and new_state not in frontier:
                parent_state[new_state] = state
                state_cost[new_state] = state_cost[state] + cost
                frontier.push(new_state, p=priority_function(new_state))
                logging.debug(f"Added new node to frontier (cost={state_cost[new_state]})")
            elif new_state in frontier and state_cost[new_state] > state_cost[state] + cost:
                old_cost = state_cost[new_state]
                parent_state[new_state] = state
                state_cost[new_state] = state_cost[state] + cost
                logging.debug(f"Updated node cost in frontier: {old_cost} -> {state_cost[new_state]}")
        if frontier:
            state = frontier.pop()
        else:
            state = None
    path = list()
    s = state
    while s:
        path.append(s.copy_data())
        s = parent_state[s]

    logging.info(f"Found a solution in {len(path):,} steps; visited {len(state_cost):,} states")
    return list(reversed(path))
    
def main():
    logging.basicConfig(level=logging.DEBUG)
    initial_state,goal = problem(N, seed)
    logging.debug(f"\nproblem : {initial_state}\ngoal : {goal}")
    parent = dict()
    cost = dict()
    search(initial_state,goal,goal_test,parent,cost,lambda s: len(cost), lambda a: 1)

if __name__ == '__main__':
    main()
