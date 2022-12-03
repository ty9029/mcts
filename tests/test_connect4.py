import numpy as np

from game.connect4 import Connect4

def test_connect4():
    game = Connect4()

    while not game.end():
        action = np.random.choice(game.legal_actions())
        game = game.next(action)

    assert game.end() == True
