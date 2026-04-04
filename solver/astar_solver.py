import heapq
from utils.expand import expand
from utils.goal import is_goal
from utils.domain import init_state
from copy import deepcopy
import time

class AStarSolver:
    def __init__(self, heuristic, is_valid):
        self.heuristic = heuristic
        self.is_valid = is_valid

    def solve(self, data, stop_check=None):
        start_time = time.perf_counter()

        initial_state = init_state(data)
        pq = []
        heapq.heappush(pq, (0, initial_state))

        while pq:

            if stop_check and stop_check():
                return None, time.perf_counter() - start_time

            f, state = heapq.heappop(pq)

            if is_goal(state):
                runtime = time.perf_counter() - start_time
                data.grid = deepcopy(state.grid)
                return data, runtime

            for child in expand(state, data, self.is_valid):

                if stop_check and stop_check():
                    return None, time.perf_counter() - start_time

                g = cost(child)
                h = self.heuristic.compute(child, data)

                heapq.heappush(pq, (g + h, child))

        return None, time.perf_counter() - start_time


def cost(state):
    count = 0
    for row in state.grid:
        count += sum(1 for x in row if x != 0)
    return count