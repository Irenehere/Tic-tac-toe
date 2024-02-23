from __future__ import print_function
import sys
import numpy as np
import random
import copy
from TicTacToeLogic import Board
sys.path.append('/home/jupyter-yguoar/Tic-tac-toe/')
from Game import Game


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

class TicTacToeGame_v2(Game):
    def __init__(self, n=9, initial_energy=10, energy_states = 11):
        self.n = n
        # self.energy_points = {1: initial_energy, -1: initial_energy}
        # self.energy_size = energy_size
        # self.initial_energy = initial_energy

        self.total_energy = (energy_states-1) * initial_energy
        self.initial_energy = initial_energy
        self.energy_size = energy_states

    def getInitBoard(self):
        # return initial board 
        b = Board(self.n, self.initial_energy, self.energy_size)
        return b

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n*self.energy_size + 1

    def getNextState(self, board, player, action):
        x = int(action / (self.n * self.energy_size))
        y = int(action/self.energy_size) % self.n
        energy_used = (action % self.energy_size)

        
        
        if action == self.n * self.n * self.energy_size:
            return (board, -player)

        # print("action: ", action)
        # print("energy_points[player]: ", board.energy_points[player])
        # print("energy_used: ", energy_used)
        # print("valid moves: ", self.getValidMoves(board, player))
        
     
        # self.energy_points[player] = self.energy_points[player] - energy_used   

        b = copy.deepcopy(board)
        # # deep copy board 
        # b = Board(self.n)

        
        move = (x,y, energy_used)

        # Normalize the energy used to from 0 to 1
        normalized_energy = energy_used / self.energy_size

        # Apply the new rules
        if normalized_energy == 0:
            if random.random() < 1/9:
                b.execute_move(move, player)
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
                    move_with_energy = (adj_move[0], adj_move[1], energy_used)
                    b.execute_move(move_with_energy, player)

        else:
            prob_accept = 1/9 + 6/9 * normalized_energy
            if random.random() < prob_accept:
                b.execute_move(move, player)
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
                    adj_move_with_energy = (adj_move[0], adj_move[1], energy_used)
                    b.execute_move(adj_move_with_energy, player)
                    # b.execute_move(adj_move, player)
        return (b, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()

        b = copy.deepcopy(board)

        # b = Board(self.n)
        # b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y, e in legalMoves:
            
            valids[ self.n * self.energy_size * x + self.energy_size * y + e] = 1
        
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        # b = Board(self.n)
        # b.pieces = np.copy(board)
        b = copy.deepcopy(board)

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
        # print("board type", type(board))

        if player == 1:

            # print("board type", type(board))
            return board
        
        elif player == -1:
            # print("board type", type(board))

            new_board = copy.deepcopy(board)
            # new_board = np.copy(board)
            new_board.pieces = -1 * board.pieces
            new_board.energy_points = {1: board.energy_points[-1], -1: board.energy_points[1]}
            return new_board
    

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.getActionSize())  # 1 for pass


        pi_board = np.reshape(pi[:-1], (self.n, self.n, self.energy_size))
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
        return str(np.array(board.pieces)) + str(board.energy_points[1]) + str(board.energy_points[-1])

    @staticmethod
    def display(board):
        n = board.pieces.shape[0]

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
                piece = board.pieces[y][x]    # get the piece to print
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


