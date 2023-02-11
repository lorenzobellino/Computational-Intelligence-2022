from opponents import pure_random
from RLAgent import *
from collections import namedtuple
from typing import Callable
import logging
import sys

NIM_SIZE = 4
NUM_MATCHES = 100
TRAINING_TIME = 10000
Nimply = namedtuple("Nimply", "row, num_objects")
logging.getLogger().setLevel(logging.DEBUG)


def evaluate(strategy: Callable, opponent: Callable = pure_random) -> int:
    strategy = (strategy, opponent)
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = strategy[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won


if __name__ == "__main__":
    nim = Nim(NIM_SIZE)
    opponent = pure_random
    logging.debug("start training of RL Agent")
    agent = Agent(nim, alpha=0.2, random_factor=0.5)
    opponent = pure_random
    print(f"training {0} / {TRAINING_TIME}", end="")
    for i in range(TRAINING_TIME):

        stateCopy = deepcopy(nim)
        while stateCopy:
            possiblePlies = cook_data(stateCopy)["possible_moves"]
            action = agent.choose_action(stateCopy, possiblePlies)
            stateCopy.nimming(action)
            # give a 0 reward if I am winning, -10 if I am losing, and -0.5 if not in a deterministic state
            reward = -10 if sum(i > 0 for i in stateCopy._rows) == 1 else -0.5 * int(sum(stateCopy._rows) > 0)

            agent.update_state_history(stateCopy, reward)

            if sum(stateCopy._rows) == 0:
                break
            stateCopy.nimming(opponent(stateCopy))

        agent.learn()
        sys.stdout.flush()
        print(f"\rtraining {i+1} / {TRAINING_TIME}", end="")

    policy = agent.get_policy()
    print("\n")
    # policy = learning(nim)
    logging.debug("finished training\nstarting tests...")
    print("-------------------")
    for _ in range(10):
        result = evaluate(RLAgent(policy), opponent)
        logging.info(f"after {NUM_MATCHES} matches, player 0 won {result} times ==> {result / NUM_MATCHES * 100}%")
    print("-------------------")
    # nim = Nim()
    # robot = Agent(nim, alpha=0.1, random_factor=0.4)
    # moveHistory = []
    # indices = []

    # for i in range(5000):

    #     while not nim:
    #         state, _ = maze.get_state_and_reward()  # get the current state
    #         state = nim.rows
    #         choose an action (explore or exploit)
    #         action = robot.choose_action(state, nim.available_moves())
    #         nim.nimming(action)
    #         maze.update_maze(action)  # update the maze according to the action

    #         state, reward = nim.get_state_and_reward()  # get the new state and reward
    #         state, reward = maze.get_state_and_reward()  # get the new state and reward
    #         update the robot memory with state and reward
    #         robot.update_state_history(state, reward)
    #         if maze.steps > 1000:
    #             # end the robot if it takes too long to find the goal
    #             maze.robot_position = (5, 5)
    #     robot.learn()  # robot should learn after every episode
    #     get a history of number of steps taken to plot later
    #     if i % 50 == 0:
    #         print(f"{i}: {nim.steps}")
    #         moveHistory.append(nim.steps)
    #         indices.append(i)
    #     nim = Nim()  # reinitialize the maze
