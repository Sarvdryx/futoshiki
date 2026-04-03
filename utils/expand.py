from copy import deepcopy
from utils.state import State

def select_unassigned_variable(state):
    best = None
    min_domain = float('inf')

    for var, domain in state.domains.items():
        i, j = var
        if state.grid[i][j] == 0:
            if len(domain) < min_domain:
                min_domain = len(domain)
                best = var

    return best


def expand(state, data, is_valid):
    var = select_unassigned_variable(state)
    if var is None:
        return []

    i, j = var
    children = []

    for val in state.domains[var]:
        if is_valid(state, data, i, j, val):
            new_grid = deepcopy(state.grid)
            new_domains = deepcopy(state.domains)

            new_grid[i][j] = val
            new_domains[var] = [val]

            
            children.append(State(new_grid, new_domains))

    return children