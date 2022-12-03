import numpy as np
from scipy import signal


def win_rule(state):
    filters = [
        np.ones((1, 4)),
        np.ones((4, 1)),
        np.identity(4),
        np.fliplr(np.identity(4))
    ]

    result = False
    for filter in filters:
        r = np.any(signal.convolve2d(state, filter, "valid") == 4)
        result = result or r

    return result


class Connect4:
    def __init__(
        self,
        state=np.zeros((6, 7)),
        enemy_state=np.zeros((6, 7)),
        first=True):

        self.state = state
        self.enemy_state = enemy_state
        self.first = first

    def next(self, action):
        all_state = self.state + self.enemy_state
        col_state, = np.where(all_state[:, action] == 0)
        y = np.max(col_state)

        action_state = np.zeros((6, 7))
        action_state[y][action] = 1

        return Connect4(self.enemy_state, self.state + action_state, first=not self.first)

    def lose(self):
        return win_rule(self.enemy_state)

    def draw(self):
        return np.all(self.state + self.enemy_state)

    def end(self):
        return self.draw() or self.lose()

    def legal_actions(self):
        all_state = self.state + self.enemy_state

        cols, = np.where(all_state[0, :] == 0)

        return cols

    def get_state(self):
        return np.concatenate([self.state, self.enemy_state], axis=2)
