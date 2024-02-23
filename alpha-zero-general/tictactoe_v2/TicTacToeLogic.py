'''
Board class for the game of TicTacToe.
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''
# from bkcharts.attributes import color
import numpy as np
 

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n=3, initial_energy=10, energy_states = 11):
        "Set up initial board configuration."

        # print("create board")

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n
        
        self.pieces = np.array(self.pieces)

        # print("create self.pieces: ", self.pieces)
        
        self.initial_energy = initial_energy
        self.energy_states = energy_states

        self.energy_points = {1: initial_energy * (energy_states-1), -1: initial_energy * (energy_states-1)}
        


    # add [][] indexer syntax to the Board
    # def __getitem__(self, index): 
    #     # print("index: ", index)
    #     return self.pieces[index]

    def get_position(self, x, y):
        

        return self.pieces[x][y]
    
    def set_position(self, x, y, value):

        # compute the index of the 1D array
        # set the value
        self.pieces[x][y] = value
        

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                # if self[x][y]==0:
                if self.get_position(x, y)==0:
                    newmove = (x,y)
                    for e in range(0, self.energy_states):
                        if e <= self.energy_points[color]:
                            moves.add((x, y, e))
                    # moves.add(newmove)
        return list(moves)

    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                # if self[x][y]==0:
                if self.get_position(x, y)==0:
                    return True
               
        return False
    
    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        win = 4
        # check y-strips
        for y in range(self.n):
            count = 0
            for x in range(self.n):
                # if self[x][y]==color:
                if self.get_position(x, y)==color:
                    count += 1
                else:
                    count = 0
                if count==win:
                    return True

        # check x-strips
        for x in range(self.n):
            count = 0
            for y in range(self.n):
                # if self[x][y]==color:
                if self.get_position(x, y)==color:
                    count += 1
                else:
                    count = 0
                if count==win:
                    return True
        # check two diagonal strips
        
        for x in range(self.n):
            for y in range(self.n):
                count = 0
                for i in range(win):
                    if x+i<self.n and y+i<self.n:
                        # if self[x+i][y+i]==color:
                        if self.get_position(x+i, y+i)==color:
                            count += 1
                        else:
                            count = 0
                        if count==win:
                            return True
        
        for x in range(self.n):
            for y in range(self.n):
                count = 0
                for i in range(win):
                    if x+i<self.n and y-i>=0:
                        # if self[x+i][y-i]==color:
                        if self.get_position(x+i, y-i)==color:
                            count += 1
                        else:
                            count = 0
                        if count==win:
                            return True
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x,y, energy_cost) = move

        # Add the piece to the empty square.

        # assert self[x][y] == 0, str(self.pieces)+"\n"+str(move)
        assert self.get_position(x, y) == 0, str(self.pieces)+"\n"+str(move)
        assert energy_cost <= self.energy_points[color], str(self.energy_points[color]) + " " + str(energy_cost)

        self.energy_points[color] -= energy_cost
        # self[x][y] = color
        self.set_position(x, y, color)

