import heapq
from solver.expand import expand
from utils.goal import is_goal
from utils.domain import init_state

class AStarSolver:
    def __init__(self, heuristic, is_valid):
        self.heuristic = heuristic
        self.is_valid = is_valid

    def solve(self, data):
        initial_state = init_state(data)

        pq = []
        heapq.heappush(pq, (0, initial_state))

        while pq:
            f, state = heapq.heappop(pq)

            if is_goal(state):
                return state.grid

            for child in expand(state, data, self.is_valid):
                g = cost(child)
                h = self.heuristic.compute(child, data)

                heapq.heappush(pq, (g + h, child))

        return None


def cost(state):
    count = 0
    for row in state.grid:
        count += sum(1 for x in row if x != 0)
    return count