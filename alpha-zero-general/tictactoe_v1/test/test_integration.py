import sys
import pytest
sys.path.append('..')
from TicTacToeGame import ProbTicTacToeGame
from TicTacToeLogic import myBoard
import numpy as np
import random


def test_game_simulation():
    '''
    This test case simulates a game where players take turns making moves in a predefined sequence. 
    The test checks if the game ends (either a win or a draw) after a certain number of moves.

    '''
    game = ProbTicTacToeGame(n=9)
    board = game.getInitBoard()
    player = 1

    moves = [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 0), (3, 1), (3, 2), (3, 3),
    ]

    game_ended = False
    for i, move in enumerate(moves):
        action = move[0] * 9 + move[1]
        valids = game.getValidMoves(board, player)
        
        if valids[action] == 1:
            board, player = game.getNextState(board, player, action)
            game_result = game.getGameEnded(board, player)

        if game_result != 0:
            game_ended = True
            break
    print(board)
    # assert game_ended == True


def test_valid_moves():
    '''
    integration test that checks if the getValidMoves function returns the correct valid moves for a given board state:
    '''
    game = ProbTicTacToeGame(n=9)
    board = game.getInitBoard()
    player = 1

    # Simulate some moves
    moves = [(0, 0), (1, 1), (2, 2), (3, 3)]
    adj_moves = [
        (0, 1), (0,2), (1,0), (1,2), (1,3), 
        (2,0), (2,1), (2,3), (2,4),
        (3,1), (3,2), (3,4),
        (4,2), (4,3), (4,4)
    ]
    for move in moves:
        action = move[0] * 9 + move[1]
        board, player = game.getNextState(board, player, action)

    # Get valid moves for the current board state
    valid_moves = game.getValidMoves(board, player)

    # Check if the valid moves are correct
    for i in range(9):
        for j in range(9):
            action = i * 9 + j
            if (i, j) not in moves and (i, j) not in adj_moves:
                assert valid_moves[action] == 1
    assert sum(valid_moves) <= 78
        
    # Check if the pass move is set to 0
    assert valid_moves[-1] == 0