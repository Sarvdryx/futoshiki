from copy import deepcopy
from model.board import FutoshikiData
import time
import tracemalloc   # 👈 đo memory

class BruteForceSolver:
    def __init__(self, data: FutoshikiData):
        self.n = data.n
        self.grid = deepcopy(data.grid)
        self.h = data.h_constraints
        self.v = data.v_constraints

        self.steps = 0   # 👈 nodes expanded

    def solve(self, stop_check=None):
        start_time = time.perf_counter()
        tracemalloc.start()   # 👈 bắt đầu đo memory

        if self._solve_all(stop_check):
            runtime = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            result = FutoshikiData(self.n)
            result.grid = self.grid
            result.h_constraints = self.h
            result.v_constraints = self.v

            return result, {
                "runtime": runtime,
                "memory": peak,
                "nodes_expanded": self.steps
            }

        runtime = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return None, {
            "runtime": runtime,
            "memory": peak,
            "nodes_expanded": self.steps
        }

    # CORE
    def _solve_all(self, stop_check):
        if stop_check and stop_check():
            return False

        self.steps += 1   # 👈 mỗi lần gọi recursion = 1 node expand

        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == 0:
                    for val in range(1, self.n + 1):
                        if stop_check and stop_check():
                            return False

                        self.grid[r][c] = val

                        if self._is_valid_partial():
                            if self._solve_all(stop_check):
                                return True

                        self.grid[r][c] = 0

                    return False

        return self._is_valid_full()

    # CHECK
    def _is_valid_partial(self):
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