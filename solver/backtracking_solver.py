from copy import deepcopy
from model.board import FutoshikiData
import time
import tracemalloc   

class BacktrackingSolver:
    def __init__(self, data: FutoshikiData, enable_trace = True):
        self.n = data.n
        self.grid = deepcopy(data.grid)
        self.h = data.h_constraints
        self.v = data.v_constraints

        self.steps = 0        
        self.enable_trace = enable_trace
        self.trace = [] if enable_trace else None

    def _log(self, action, r, c, val):
        if self.enable_trace:
            self.trace.append({
                "action": action,
                "cell": (r, c),
                "value": val
            })

    def solve(self, stop_check=None):
        start_time = time.perf_counter()
        tracemalloc.start()

        if self._backtrack(stop_check):
            runtime = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            result = FutoshikiData(self.n)
            result.grid = deepcopy(self.grid)
            result.h_constraints = self.h
            result.v_constraints = self.v

            return result, {
                "runtime": runtime,
                "memory": peak,
                "nodes_expanded": self.steps,
                "trace": self.trace if self.enable_trace else None
            }

        runtime = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return None, {
            "runtime": runtime,
            "memory": peak,
            "nodes_expanded": self.steps,
            "trace": self.trace if self.enable_trace else None
        }

    # ================= CORE =================
    def _backtrack(self, stop_check):
        if stop_check and stop_check():
            return False

        self.steps += 1 

        cell = self._find_empty()
        if not cell:
            return True

        r, c = cell

        for val in range(1, self.n + 1):
            if stop_check and stop_check():
                return False

            self._log("assign", r, c, val)

            if self._is_valid(r, c, val):
                self.grid[r][c] = val

                if self._backtrack(stop_check):
                    return True
                self._log("backtrack", r, c, val)
                self.grid[r][c] = 0

            else:
                self._log("reject", r, c, val) 
                self._log("backtrack", r, c, val)

        return False

    # ================= HELPERS =================
    def _find_empty(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def _is_valid(self, r, c, val):
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