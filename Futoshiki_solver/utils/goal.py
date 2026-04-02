def is_goal(state):
    for row in state.grid:
        if any(x == 0 for x in row):
            return False
    return True