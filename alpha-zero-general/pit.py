import Arena
from MCTS import MCTS
from tictactoe.TicTacToePlayers import *

from tictactoe_v2.TicTacToeGame import TicTacToeGame_v2 as TicTacToeGame
from tictactoe_v2.keras.NNet import NNetWrapper as NNet

# from tictactoe_v1.TicTacToeGame import ProbTicTacToeGame as TicTacToeGame
# from tictactoe_v1.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = TicTacToeGame()
fout_path = "results_v2_attempt2.txt"

# nnet players
n1 = NNet(g)
n1.load_checkpoint('/home/jupyter-yguoar/Tic-tac-toe/alpha-zero-general/model_v2_attempt2','best.h5')  
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

competitors = ["random",'model-random', "checkpoint_2.h5", 'checkpoint_7.h5','checkpoint_13.h5'] #["random",'checkpoint_6.h5', 'checkpoint_8.h5','checkpoint_17.h5','model-random'] #'human'

for competitor in competitors:
    if competitor == "random":
        player2 = RandomPlayer(g).play
    elif competitor == "human":
        player2 = HumanTicTacToePlayer(g).play
    elif competitor == "model-random":
        n2 = NNet(g)
        args2 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
        mcts2 = MCTS(g, n2, args2)
        player2 = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    else:
        n2 = NNet(g)
        n2.load_checkpoint('/home/jupyter-yguoar/Tic-tac-toe/alpha-zero-general/model_v2_attempt2',competitor)
        args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
        mcts2 = MCTS(g, n2, args2)
        player2 = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))


    arena = Arena.Arena(n1p, player2, g, display=TicTacToeGame.display)

    results = arena.playGames(20, verbose=True)
    print(results)
    with open(fout_path, "a") as fout:
        print("vs competitor:,"+competitor)
        print("competitor:,"+competitor, file=fout)
        print(results, file=fout)
        print("\n\n", file=fout)
