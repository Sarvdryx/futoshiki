from heuristics.base import Heuristic

class Heuristic1(Heuristic):
    def compute(self, state, data):
        grid = state.grid
        n = data.n
        count = 0

        for i in range(n):
            for j in range(n - 1):
                c = data.h_constraints[i][j]
                if c == 0:
                    continue

                a, b = grid[i][j], grid[i][j + 1]

                if a == 0 or b == 0:
                    count += 1
                elif (c == 1 and not (a < b)) or (c == -1 and not (a > b)):
                    count += 1

        for i in range(n - 1):
            for j in range(n):
                c = data.v_constraints[i][j]
                if c == 0:
                    continue

                a, b = grid[i][j], grid[i + 1][j]

                if a == 0 or b == 0:
                    count += 1
                elif (c == 1 and not (a < b)) or (c == -1 and not (a > b)):
                    count += 1

        return count