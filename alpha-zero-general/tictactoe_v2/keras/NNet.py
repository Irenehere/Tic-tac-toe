import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
sys.path.append('..')
from utils import *
from NeuralNet import NeuralNet

import argparse
from .TicTacToeNNet import TicTacToeNNet as onnet

"""
NeuralNet wrapper class for the TicTacToeNNet.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on (copy-pasted from) the NNet by SourKream and Surag Nair.
"""

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': False,
    'num_channels': 512,
})

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = onnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))

        batched_boards =  np.asarray([board.pieces for board in input_boards])
        # input_boards = np.asarray(input_boards.pieces)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)

        batched_energies =  np.asarray([[board.energy_points[1], board.energy_points[-1]] for board in input_boards])
        # input_energies = np.asarray([input_boards.energy_points[1], input_boards.energy_points[-1]])

        self.nnet.model.fit(x = [batched_boards, batched_energies], y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs)

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board_pieces = board.pieces[np.newaxis, :, :]
        board_energies = np.asarray([board.energy_points[1], board.energy_points[-1]])
        board_energies = board_energies[np.newaxis, :]

        # run

        # print("board_pieces: ", board_pieces)
        # print("board_energies: ", board_energies)
        pi, v = self.nnet.model.predict((board_pieces, board_energies), verbose=False)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise("No model in path '{}'".format(filepath))
        self.nnet.model.load_weights(filepath)