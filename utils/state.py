class State:
    def __init__(self, grid, domains):
        self.grid = grid
        self.domains = domains

    def __lt__(self, other):
        return True  # để heapq không crash