class FutoshikiData:
    def __init__(self, n):
        self.n = n
        self.grid = [[0] * n for _ in range(n)]
        self.h_constraints = [] # Ma trận N x (N-1)
        self.v_constraints = [] # Ma trận (N-1) x N