import numpy as np

from game.tictactoe import TicTacToe

def test_tictactoe():
    game = TicTacToe()

    while not game.end():
        action = np.random.choice(game.legal_actions())
        game = game.next(action)

    assert game.end() == True
