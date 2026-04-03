from heuristics.base import Heuristic
from copy import deepcopy
from csp.ac3 import ac3, build_graph

class Heuristic2(Heuristic):
    def compute(self, state, data):
        domains = deepcopy(state.domains)

        neighbors, constraints = build_graph(data)

        if not ac3(domains, neighbors, constraints, data):
            return float('inf')

        count = 0
        for d in domains.values():
            if len(d) == 0:
                count += 1

        return count