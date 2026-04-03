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

    def solve(self, data):
        start_time = time.perf_counter()   # ⏱ bắt đầu

        initial_state = init_state(data)

        pq = []
        heapq.heappush(pq, (0, initial_state))

        while pq:
            f, state = heapq.heappop(pq)

            if is_goal(state):
                runtime = time.perf_counter() - start_time  # ⏱ kết thúc

                data.grid = deepcopy(state.grid)
                return data, runtime

            for child in expand(state, data, self.is_valid):
                g = cost(child)
                h = self.heuristic.compute(child, data)

                heapq.heappush(pq, (g + h, child))

        runtime = time.perf_counter() - start_time  # ⏱ nếu không tìm được
        return None, runtime


def cost(state):
    count = 0
    for row in state.grid:
        count += sum(1 for x in row if x != 0)
    return count