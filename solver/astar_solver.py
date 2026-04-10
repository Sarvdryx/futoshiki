import heapq
from utils.expand import expand
from utils.goal import is_goal
from utils.domain import init_state
from copy import deepcopy
import time
import tracemalloc 


class AStarSolver:
    def __init__(self, heuristic, is_valid, enable_trace=True):
        self.heuristic = heuristic
        self.is_valid = is_valid

        self.enable_trace = enable_trace
        self.trace = [] if enable_trace else None
        self.steps = 0

    # ================= TRACE =================
    def _log(self, action, state=None, info=None):
        if self.enable_trace:
            self.trace.append({
                "action": action,
                "grid": deepcopy(state.grid) if state else None,
                "info": info
            })

    # ================= SOLVE =================
    def solve(self, data, stop_check=None):
        start_time = time.perf_counter()
        tracemalloc.start()  

        initial_state = init_state(data)

        pq = []
        heapq.heappush(pq, (0, initial_state))

        self._log("push", initial_state, {"f": 0})

        while pq:

            if stop_check and stop_check():
                return self._finish(None, start_time)

            f, state = heapq.heappop(pq)
            self.steps += 1

            self._log("pop", state, {"f": f})

            if is_goal(state):
                self._log("goal", state)
                return self._finish(state, start_time, data)

            self._log("expand", state)

            for child in expand(state, data, self.is_valid):

                if stop_check and stop_check():
                    return self._finish(None, start_time)

                g = cost(child)
                h = self.heuristic.compute(child, data)
                f_child = g + h
                
                self._log("push", child, {"g": g, "h": h, "f": f_child})

                heapq.heappush(pq, (f_child, child))

        return self._finish(None, start_time)

    # ================= FINISH =================
    def _finish(self, state, start_time, data=None):
        runtime = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if state and data:
            data.grid = deepcopy(state.grid)

        return (data if state else None), {
            "runtime": runtime,
            "memory": peak,
            "nodes_expanded": self.steps,
            "trace": self.trace if self.enable_trace else None
        }


# ================= COST =================
def cost(state):
    count = 0
    for row in state.grid:
        count += sum(1 for x in row if x != 0)
    return count