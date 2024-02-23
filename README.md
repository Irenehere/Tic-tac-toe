# Playing Variations on Tic-Tac-Toe with the AlphaZero Algorithm 

### Requirments
The codes are implemented under python==3.9, Tensorflow==2.5.0, numpy==1.21.0

### Train the model for modified version 1: Probabilistic Tic-Tac-Toe
```bash
python main_v1.py
```

### Train the model for modified version 2: TicTacToe with Energy
```bash
python main_v2.py
```

### Evaluation: playing the models in arena
To compete the models in arena, modify the directory of the n1.load_checkpoint() and the competitors, and run 
```bash
python pit.py
```

### Testing the Codes

To run the test scripts, first, you need to install pytest:

```bash
pip install pytest
```


- Unit test 

This unit test script includes test cases for checking the functions in the game and board classes. You can run the tests by executing the following command:
```bash
# for version 1 
cd tictactoe_v1/test
pytest test_prob_tictactoe.py

# for version 2
cd tictactoe_v2/test
pytest test_units.py
```


- Integration tests
The integration test suite plays two quick games using an untrained neural network (randomly initialized) against a random player for each combination of game and ML framework. To run integration tests, execute:
```bash
# for version 1 
cd tictactoe_v1/test
pytest test_integration.py

# for version 2
cd tictactoe_v2/test
pytest test_integration.py
```


- Regression tests 

To run regression test, run
```bash
# for version 1 
cd tictactoe_v1/test
pytest test_regression.py
``` 

### Acknowledgement
The codes are modified from the [alpha-zero-general](https://github.com/suragnair/alpha-zero-general) repository.
