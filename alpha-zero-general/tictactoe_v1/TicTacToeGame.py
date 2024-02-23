from __future__ import print_function
import sys
from .TicTacToeLogic import myBoard as Board
sys.path.append('/home/jupyter-yguoar/Tic-tac-toe/alpha-zero-general/')
# from tictactoe.TicTacToeGame import TicTacToeGame 
from Game import Game
import numpy as np
import random

"""
Variation of the TicTacToe game with the following features:
1. The board has 9 x 9 squares.
2. After a player chooses an empty square, there is only 1/2 chance that his nought or cross is placed at the chosen square.  
If the player’s choice is not accepted, the player’s move is selected randomly with probability 1/16 by the computer from
the 8 random squares adjacent to the chosen one, with the boundaries ignored.   If the random choice is occupied or outside 
of the board, the player’s move is forfeited.  For example, if the chosen square is at the corner, then with probability = 5/16,
the randomly selected square is outside of the board.


Based on the TicTacToeGame by Evgeny Tyurin, github.com/evg-tyurin. 

"""


class ProbTicTacToeGame(Game):
    def __init__(self, n=9):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n * self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)

        # Apply the new rules

        #After a player chooses an empty square, there is only 1/2 chance that his nought or cross is placed at the chosen square. 
        if random.random() < 0.5:
            b.execute_move(move, player)

        #If the player’s choice is not accepted, the player’s move is selected randomly with probability 1/16 by the computer from
        #  the 8 random squares adjacent to the chosen one, with the boundaries ignored.  
        #  If the random choice is occupied or outside of the board, the player’s move is forfeited.
        else:
            adjacent_moves = [
                (move[0] - 1, move[1]),
                (move[0] + 1, move[1]),
                (move[0], move[1] - 1),
                (move[0], move[1] + 1),
                (move[0] - 1, move[1] - 1),
                (move[0] + 1, move[1] + 1),
                (move[0] - 1, move[1] + 1),
                (move[0] + 1, move[1] - 1),
            ]    
            random.shuffle(adjacent_moves)
            adj_move = adjacent_moves[0]
            if 0 <= adj_move[0] < self.n and 0 <= adj_move[1] < self.n and b.pieces[adj_move] == 0:
                b.execute_move(adj_move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)
    
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        n = board.shape[0]

        print("   ", end="")
        for y in range(n):
            print (y,"", end="")
        print("")
        print("  ", end="")
        for _ in range(n):
            print ("-", end="-")
        print("--")
        for y in range(n):
            print(y, "|",end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece == -1: print("X ",end="")
                elif piece == 1: print("O ",end="")
                else:
                    if x==n:
                        print("-",end="")
                    else:
                        print("- ",end="")
            print("|")

        print("  ", end="")
        for _ in range(n):
            print ("-", end="-")
        print("--")
