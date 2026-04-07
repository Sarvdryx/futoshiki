import heapq
from utils.expand import expand
from utils.goal import is_goal
from utils.domain import init_state
from copy import deepcopy
import time
import tracemalloc 

class AStarSolver:
    def __init__(self, heuristic, is_valid):
        self.heuristic = heuristic
        self.is_valid = is_valid

    def solve(self, data, stop_check=None):
        start_time = time.perf_counter()
        tracemalloc.start()  

        nodes_expanded = 0

        initial_state = init_state(data)
        pq = []
        heapq.heappush(pq, (0, initial_state))

        while pq:

            if stop_check and stop_check():
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                return None, {
                    "runtime": time.perf_counter() - start_time,
                    "memory": peak,
                    "nodes_expanded": nodes_expanded
                }

            f, state = heapq.heappop(pq)
            nodes_expanded += 1   

            if is_goal(state):
                runtime = time.perf_counter() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                data.grid = deepcopy(state.grid)

                return data, {
                    "runtime": runtime,
                    "memory": peak,
                    "nodes_expanded": nodes_expanded
                }

            for child in expand(state, data, self.is_valid):

                if stop_check and stop_check():
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    return None, {
                        "runtime": time.perf_counter() - start_time,
                        "memory": peak,
                        "nodes_expanded": nodes_expanded
                    }

                g = cost(child)
                h = self.heuristic.compute(child, data)

                heapq.heappush(pq, (g + h, child))

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return None, {
            "runtime": time.perf_counter() - start_time,
            "memory": peak,
            "nodes_expanded": nodes_expanded
        }


def cost(state):
    count = 0
    for row in state.grid:
        count += sum(1 for x in row if x != 0)
    return count