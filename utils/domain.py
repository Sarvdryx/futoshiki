from utils.state import State
from copy import deepcopy

def init_state(data):
    n = data.n
    domains = {}

    for i in range(n):
        for j in range(n):
            if data.grid[i][j] != 0:
                domains[(i, j)] = [data.grid[i][j]]
            else:
                domains[(i, j)] = list(range(1, n + 1))

    return State(deepcopy(data.grid), domains)