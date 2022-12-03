from operator import attrgetter
import random
import numpy as np
import copy


def uct(sum_n, n, w):
    return -w / n +  (2 * np.log(sum_n) / n) ** 0.5


def playout(state):
    if state.end():
        if state.lose():
            return -1
        else:
            return 0
    action = np.random.choice(state.legal_actions())
    return -playout(state.next(action))


class Node:
    def __init__(self, state, expand_base=10):
        self.state = state
        self.w = 0
        self.n = 0
        self.expand_base = expand_base
        self.child_nodes = {}

    def get_action(self):
        actions = {k: -n.w / n.n for k, n in self.child_nodes.items()}
        action = random.choice([key for key in actions if actions[key] == max(actions.values())])

        return action

    def select_child_node(self):
        for child in self.child_nodes.values():
            if child.n == 0:
                return child

        sum_n = sum(map(attrgetter("n"), self.child_nodes.values()))
        ucb1_dict = {action: uct(sum_n, child.n, child.w) for action, child in self.child_nodes.items()}

        action = random.choice([key for key in ucb1_dict if ucb1_dict[key] == max(ucb1_dict.values())])

        return self.child_nodes[action]

    def expand(self):
        self.child_nodes = {action: Node(self.state.next(action), self.expand_base) for action in self.state.legal_actions()}

    def evaluate(self):
        if self.state.end():
            if self.state.lose():
                value = -1
            else:
                value = 0

            self.w += value
            self.n += 1

            return value

        if not self.child_nodes:
            value = playout(copy.deepcopy(self.state))

            self.w += value
            self.n += 1
            if self.n == self.expand_base:
                self.expand()

            return value
        else:
            value = -self.select_child_node().evaluate()

            self.w += value
            self.n += 1

            return value
