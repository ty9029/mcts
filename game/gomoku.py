import numpy as np
from scipy import signal


def win_rule(state):
    filters = [
        np.ones((1, 5)),
        np.ones((5, 1)),
        np.identity(5),
        np.fliplr(np.identity(5))
    ]

    result = False
    for filter in filters:
        r = np.any(signal.convolve2d(state, filter, "valid") == 5)
        result = result or r

    return result


class Gomoku:
    def __init__(
        self,
        state=np.zeros((15, 15)),
        enemy_state=np.zeros((15, 15)),
        first=True):

        self.state = state
        self.enemy_state = enemy_state
        self.first = first

    def next(self, action):
        row, col = action // 15, action % 15
        action = np.zeros((15, 15))
        action[row][col] = 1

        return Gomoku(self.enemy_state, self.state + action, first=not self.first)

    def lose(self):
        return win_rule(self.enemy_state)

    def draw(self):
        return np.all(self.state + self.enemy_state)

    def end(self):
        return self.draw() or self.lose()

    def legal_actions(self):
        all_state = self.state + self.enemy_state

        rows, cols = np.where(all_state == 0)

        return rows * 15 + cols

    def get_state(self):
        return np.concatenate([self.state, self.enemy_state], axis=2)
