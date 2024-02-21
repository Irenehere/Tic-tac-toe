# TicTacToe Modified Version 1

An implementation of a simple game provided to check extendability of the framework. Main difference of this game comparing to Othello is that it allows draws, i.e. the cases when nobody won after the game ended. To support such outcomes ```Arena.py``` and ```Coach.py``` classes were modified. Neural network architecture was copy-pasted from the game of Othello, so possibly it can be simplified. 

To train a model for TicTacToe, change the imports in ```main.py``` to:
```python
from Coach import Coach
from tictactoe_v1.TicTacToeGame import ProbTicTacToeGame as TicTacToeGame
from tictactoe_v1.keras.NNet import NNetWrapper as nn
from utils import *
```


To start training a model for TicTacToe:
```bash
python main.py
```
To start a tournament of 100 episodes with the model-based player against a random player:
```bash
python pit.py
```
You can play againt the model by switching to HumanPlayer in ```pit.py```

### Experiments
I trained a Keras model for 3x3 TicTacToe (3 iterations, 25 episodes, 10 epochs per iteration and 25 MCTS simulations per turn). This took about 30 minutes on an i5-4570 without CUDA. The pretrained model (Keras) can be found in ```pretrained_models/tictactoe/keras/```. You can play a game against it using ```pit.py```. 

### Testing the Codes

To run the test scripts, first, you need to install pytest:

```bash
pip install pytest
```


- Unit test 

This unit test script includes test cases for checking the board size, action size, initial board, winning conditions, move execution, and getting next state. You can run the tests by executing the following command:
```bash
pytest test_prob_tictactoe.py
```

- Regression tests 

- Integration tests

Integration tests focus on testing the interaction between different components of the application. In the case of the TicTacToe game variation, we can test the interaction between the ProbTicTacToeGame and myBoard classes. To run integration tests, execute:
```bash
pytest test_prob_tictactoe.py
```


