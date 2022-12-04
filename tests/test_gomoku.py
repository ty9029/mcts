import numpy as np

from game.gomoku import Gomoku

def test_connect4():
    game = Gomoku()

    while not game.end():
        action = np.random.choice(game.legal_actions())
        game = game.next(action)

    assert game.end() == True
