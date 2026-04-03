from copy import deepcopy
from model.board import FutoshikiData
import time

class BacktrackingSolver:
    def __init__(self, data: FutoshikiData):
        self.n = data.n
        self.grid = deepcopy(data.grid)
        self.h = data.h_constraints
        self.v = data.v_constraints

        # thống kê (cho report)
        self.steps = 0
        self.backtracks = 0

    def solve(self) -> FutoshikiData:
        start_time = time.time()

        if self._backtrack():
            end_time = time.time()
            runtime = end_time - start_time   

            result = FutoshikiData(self.n)
            result.grid = deepcopy(self.grid)
            result.h_constraints = self.h
            result.v_constraints = self.v

            return result, runtime

        end_time = time.time()
        runtime = end_time - start_time

        return None, runtime
    # ================= CORE =================

    def _backtrack(self):
        self.steps += 1

        cell = self._find_empty()
        if not cell:
            return True

        r, c = cell

        for val in range(1, self.n + 1):
            if self._is_valid(r, c, val):
                self.grid[r][c] = val

                if self._backtrack():
                    return True

                self.grid[r][c] = 0
                self.backtracks += 1

        return False

    # ================= HELPERS =================

    def _find_empty(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def _is_valid(self, r, c, val):
        # Row + Column
        for i in range(self.n):
            if self.grid[r][i] == val:
                return False
            if self.grid[i][c] == val:
                return False

        # LEFT
        if c > 0 and self.h[r][c - 1] != 0 and self.grid[r][c - 1] != 0:
            if self.h[r][c - 1] == 1 and not (self.grid[r][c - 1] < val):
                return False
            if self.h[r][c - 1] == -1 and not (self.grid[r][c - 1] > val):
                return False

        # RIGHT
        if c < self.n - 1 and self.h[r][c] != 0 and self.grid[r][c + 1] != 0:
            if self.h[r][c] == 1 and not (val < self.grid[r][c + 1]):
                return False
            if self.h[r][c] == -1 and not (val > self.grid[r][c + 1]):
                return False

        # UP
        if r > 0 and self.v[r - 1][c] != 0 and self.grid[r - 1][c] != 0:
            if self.v[r - 1][c] == 1 and not (self.grid[r - 1][c] < val):
                return False
            if self.v[r - 1][c] == -1 and not (self.grid[r - 1][c] > val):
                return False

        # DOWN
        if r < self.n - 1 and self.v[r][c] != 0 and self.grid[r + 1][c] != 0:
            if self.v[r][c] == 1 and not (val < self.grid[r + 1][c]):
                return False
            if self.v[r][c] == -1 and not (val > self.grid[r + 1][c]):
                return False

        return True