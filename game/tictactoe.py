import numpy as np


def win_rule(state):
    win_state = np.zeros(8)
    win_state[0:3] = np.sum(state, axis=0)
    win_state[3:6] = np.sum(state, axis=1)
    win_state[6] = np.sum(np.diagonal(state))
    win_state[7] = np.sum(np.diagonal(np.fliplr(state)))
    win_state = np.any(win_state == 3)

    return win_state


class TicTacToe:
    def __init__(
        self,
        state=np.zeros((3, 3)),
        enemy_state=np.zeros((3, 3)),
        first=True):

        self.state = state
        self.enemy_state = enemy_state
        self.first = first

    def next(self, action):
        row, col = action // 3, action % 3
        action = np.zeros((3, 3))
        action[row][col] = 1

        return TicTacToe(self.enemy_state, self.state + action, first=not self.first)

    def lose(self):
        return win_rule(self.enemy_state)

    def draw(self):
        return np.all(self.state + self.enemy_state)

    def end(self):
        return self.draw() or self.lose()

    def legal_actions(self):
        all_state = self.state + self.enemy_state

        rows, cols = np.where(all_state == 0)

        return rows * 3 + cols

    def get_state(self):
        return np.concatenate([self.state, self.enemy_state], axis=2)
