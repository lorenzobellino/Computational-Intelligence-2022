from itertools import permutations
import logging
import random

logging.basicConfig(level=logging.DEBUG)
winning_states = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6], [0, 4, 8]]


def won(state):
    return any(list(p) in winning_states for p in permutations(state, 3))


def eval_terminal(x, o):
    if won(x):
        return 1
    elif won(o):
        return -1
    else:
        return 0


def minmax(board):
    val = eval_terminal(*board)
    possible = list(set(range(9)) - set(board[0]) - set(board[1]))
    if val != 0 or not possible:
        return None, val
    evaluation = list()
    for ply in possible:
        _, val = minmax((board[1], board[0] | {ply}))
        evaluation.append((ply, -val))
    return max(evaluation, key=lambda x: x[1])


def end_game(board):
    if eval_terminal(*board) != 0:
        return True
    if len(board[0]) + len(board[1]) == 9:
        return True


def draw_board(drawing):
    logging.info(
        f"game-board:\n{' | '.join(drawing[0])}\n----------\n{' | '.join(drawing[1])}\n----------\n{' | '.join(drawing[2])}"
    )


def choose_move(board):
    move = int(input("your move: "))
    while {move} & board[1] or {move} & board[0] or move > 8 or move < 0:
        logging.info(f"invalid move")
        move = int(input("your move: "))
    return move


def terminate(board, drawing):
    logging.info(f"final board")
    logging.info(f"X: {board[0]}")
    logging.info(f"O: {board[1]}")
    draw_board(drawing=drawing)
    w = eval_terminal(*board)
    if w == 0:
        logging.info(f"winner: game tied")
    elif w == 1:
        logging.info(f"winner: X")
    else:
        logging.info(f"winner: O")


def main():
    drawing = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    board = (set(), set())
    if random.random() < 0.5:
        move = choose_move(board)
        board = (board[0], board[1] | {move})
        drawing[move // 3][move % 3] = "O"
        draw_board(drawing)
    else:
        logging.info(f"computer starts")
    while not end_game(board):
        # logging.info(f"board: {board}")
        move, val = minmax(board)
        board = (board[0] | {move}, board[1])
        drawing[move // 3][move % 3] = "X"
        draw_board(drawing)
        if not end_game(board):
            # logging.info(f"my move: {move}")
            # logging.info(f"board: {board}")
            move = choose_move(board)
            board = (board[0], board[1] | {move})
            drawing[move // 3][move % 3] = "O"
            draw_board(drawing)
    terminate(board, drawing)


if __name__ == "__main__":
    main()
