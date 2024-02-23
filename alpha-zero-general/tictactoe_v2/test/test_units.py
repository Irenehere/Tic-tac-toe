import pytest
import numpy as np
import random
import sys
sys.path.append('/home/jupyter-yguoar/Tic-tac-toe/alpha-zero-general/tictactoe_v2')
from TicTacToeGame import TicTacToeGame_v2, Board

def test_init():
    game = TicTacToeGame_v2()
    assert game.n == 9
    assert game.initial_energy == 10
    assert game.energy_size == 11

def test_getInitBoard():
    game = TicTacToeGame_v2()
    board = game.getInitBoard()
    assert isinstance(board, Board)
    assert board.pieces.shape == (9, 9)
    assert board.energy_points == {1: 100, -1: 100}

def test_getBoardSize():
    game = TicTacToeGame_v2()
    board_size = game.getBoardSize()
    assert board_size == (9, 9)

def test_getActionSize():
    game = TicTacToeGame_v2()
    action_size = game.getActionSize()
    assert action_size == 9 * 9 * 11 + 1

def test_getNextState():
    game = TicTacToeGame_v2()
    board = game.getInitBoard()
    player = 1
    action = 0
    next_state, next_player = game.getNextState(board, player, action)
    assert isinstance(next_state, Board)
    assert next_player == -1

def test_init():
    board = Board()
    assert board.n == 3
    assert board.initial_energy == 10
    assert board.energy_states == 11
    assert board.energy_points == {1: 100, -1: 100}
    assert np.all(board.pieces == np.zeros((3, 3)))

def test_get_position():
    board = Board()
    assert board.get_position(0, 0) == 0

def test_set_position():
    board = Board()
    board.set_position(0, 0, 1)
    assert board.get_position(0, 0) == 1

def test_get_legal_moves():
    board = Board()
    legal_moves = board.get_legal_moves(1)
    assert len(legal_moves) == 3 * 3 * 11
    assert (0, 0, 0) in legal_moves
    assert (2, 2, 10) in legal_moves

def test_has_legal_moves():
    board = Board()
    assert board.has_legal_moves()

def test_is_win():
    board = Board(n=4)
    assert not board.is_win(1)
    board.set_position(0, 0, 1)
    board.set_position(1, 1, 1)
    board.set_position(2, 2, 1)
    board.set_position(3, 3, 1)
    assert board.is_win(1)

def test_execute_move():
    board = Board()
    board.execute_move((0, 0, 5), 1)
    assert board.get_position(0, 0) == 1
    assert board.energy_points[1] == 95