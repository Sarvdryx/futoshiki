from copy import deepcopy
from model.board import FutoshikiData
import time

class BruteForceSolver:
    def __init__(self, data: FutoshikiData):
        self.n = data.n
        self.grid = deepcopy(data.grid)
        self.h = data.h_constraints
        self.v = data.v_constraints

        self.steps = 0

    def solve(self, stop_check=None) -> FutoshikiData:
        start_time = time.time()
        if self._solve_all(stop_check):
            end_time = time.time()
            runtime = end_time - start_time

            result = FutoshikiData(self.n)
            result.grid = self.grid
            result.h_constraints = self.h
            result.v_constraints = self.v
            return result, runtime
        
        end_time = time.time()
        runtime = end_time - start_time
        return None, runtime

    #CORE 

    def _solve_all(self, stop_check):
        if stop_check and stop_check():
            return False
        self.steps += 1

        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == 0:
                    for val in range(1, self.n + 1):
                        if stop_check and stop_check():
                            return False
                        self.grid[r][c] = val

                        if self._is_valid_partial():
                            if self._solve_all():
                                return True

                        self.grid[r][c] = 0

                    return False

        return self._is_valid_full()

    #CHECK

    def _is_valid_partial(self):
        # check row + col (không trùng)
        for r in range(self.n):
            seen = set()
            for val in self.grid[r]:
                if val != 0:
                    if val in seen:
                        return False
                    seen.add(val)

        for c in range(self.n):
            seen = set()
            for r in range(self.n):
                val = self.grid[r][c]
                if val != 0:
                    if val in seen:
                        return False
                    seen.add(val)

        return True

    def _is_valid_full(self):
        # check inequality khi full
        for r in range(self.n):
            for c in range(self.n - 1):
                if self.h[r][c] == 1 and not (self.grid[r][c] < self.grid[r][c + 1]):
                    return False
                if self.h[r][c] == -1 and not (self.grid[r][c] > self.grid[r][c + 1]):
                    return False

        for r in range(self.n - 1):
            for c in range(self.n):
                if self.v[r][c] == 1 and not (self.grid[r][c] < self.grid[r + 1][c]):
                    return False
                if self.v[r][c] == -1 and not (self.grid[r][c] > self.grid[r + 1][c]):
                    return False

        return True