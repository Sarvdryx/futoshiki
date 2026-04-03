from csp.constraints import is_consistent_pair

def is_goal(state):
    for row in state.grid:
        if any(x == 0 for x in row):
            return False
    return True

def is_valid(state, data, i, j, val):
    xi = (i, j)

    for (ni, nj), domain in state.domains.items():
        if (ni, nj) == xi:
            continue

        if state.grid[ni][nj] != 0:
            y = state.grid[ni][nj]

            if not is_consistent_pair(val, y, xi, (ni, nj), data):
                return False

    return True