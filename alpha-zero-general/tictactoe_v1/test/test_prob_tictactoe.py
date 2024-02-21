import sys
import pytest
sys.path.append('..')
from TicTacToeGame import ProbTicTacToeGame
from TicTacToeLogic import myBoard
import numpy as np
import random


def test_board_size():
    game = ProbTicTacToeGame(n=9)
    board_size = game.getBoardSize()
    assert board_size == (9, 9)

def test_action_size():
    game = ProbTicTacToeGame(n=9)
    action_size = game.getActionSize()
    assert action_size == 82

def test_initial_board():
    game = ProbTicTacToeGame(n=9)
    init_board = game.getInitBoard()
    assert init_board.shape == (9, 9)
    assert (init_board == 0).all()

def test_my_board_is_win():
    board = myBoard(n=9)

    # Test horizontal win
    for i in range(4):
        board[0][i] = 1
    assert board.is_win(1) == True

    # Test vertical win
    for i in range(4):
        board[i][0] = -1
    assert board.is_win(-1) == True

    # Test diagonal win
    for i in range(4):
        board[i][i] = 1
    assert board.is_win(1) == True

    # Test anti-diagonal win
    for i in range(4):
        board[i][8 - i] = -1
    assert board.is_win(-1) == True

    # Test no win
    board[0][0] = -1
    assert board.is_win(1) == False

def test_my_board_execute_move():
    board = myBoard(n=9)
    board.execute_move((4, 4), 1)
    assert board[4][4] == 1
    board.execute_move((4, 5), -1)
    assert board[4][5] == -1


def test_get_next_state():
    '''This test case checks if the next state is updated correctly after a player makes a move. 
    Note that due to the probabilistic nature of the game, it's not possible to test the exact next state. 
    Instead, we can test if the next state is a valid outcome based on the rules.
    '''

    #case 1
    game = ProbTicTacToeGame(n=9)
    init_board = game.getInitBoard()
    player = 1

    next_board, next_player = game.getNextState(init_board, player, 40)
    assert next_player == -1

    # Check if the chosen square or one of the adjacent squares is occupied
    chosen_square = (4, 4)
    adjacent_squares = [
        (3, 4), (5, 4), (4, 3), (4, 5),
        (3, 3), (5, 5), (3, 5), (5, 3)
    ]

    occupied = False
    if next_board[chosen_square] == player:
        occupied = True
    else:
        for square in adjacent_squares:
            if next_board[square] == player:
                occupied = True
                break

    assert occupied == True

    # case 2
    game = ProbTicTacToeGame(n=9)
    init_board = game.getInitBoard()
    player = -1

    next_board, next_player = game.getNextState(init_board, player, 80)
    assert next_player == 1

    # Check if the chosen square or one of the adjacent squares is occupied
    chosen_square = (8,8)
    adjacent_squares = [
        (7, 8), (8, 7), (7, 7)
    ]
    occupied = False
    if next_board[chosen_square] == player:
        occupied = True
    else:
        for square in adjacent_squares:
            if next_board[square] == player:
                occupied = True
                break

    # case 3 
    game = ProbTicTacToeGame(n=9)
    init_board = game.getInitBoard()
    player = -1

    next_board, next_player = game.getNextState(init_board, player, 81)
    assert next_player == 1
    assert (next_board == init_board).all()


    


if __name__ == "__main__":
    pytest.main()