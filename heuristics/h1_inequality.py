from heuristics.base import Heuristic

class Heuristic1(Heuristic):
    def compute(self, state, data):
        grid = state.grid
        n = data.n
        count = 0

        for i in range(n):
            for j in range(n):
                # Bỏ qua các ô của đề bài ban đầu
                if data.grid[i][j] != 0:
                    continue
                violated = False

                # --- kiểm tra ngang: (i, j) với (i, j+1)
                if j < n - 1:
                    c = data.h_constraints[i][j]
                    if c != 0:
                        a, b = grid[i][j], grid[i][j + 1]
                        if a == 0 or b == 0:
                            violated = True
                        elif (c == 1 and not (a < b)) or (c == -1 and not (a > b)):
                            violated = True

                # --- kiểm tra ngang: (i, j-1) với (i, j)
                if j > 0 and not violated:
                    c = data.h_constraints[i][j - 1]
                    if c != 0:
                        a, b = grid[i][j - 1], grid[i][j]
                        if a == 0 or b == 0:
                            violated = True
                        elif (c == 1 and not (a < b)) or (c == -1 and not (a > b)):
                            violated = True

                # --- kiểm tra dọc: (i, j) với (i+1, j)
                if i < n - 1 and not violated:
                    c = data.v_constraints[i][j]
                    if c != 0:
                        a, b = grid[i][j], grid[i + 1][j]
                        if a == 0 or b == 0:
                            violated = True
                        elif (c == 1 and not (a < b)) or (c == -1 and not (a > b)):
                            violated = True

                # --- kiểm tra dọc: (i-1, j) với (i, j)
                if i > 0 and not violated:
                    c = data.v_constraints[i - 1][j]
                    if c != 0:
                        a, b = grid[i - 1][j], grid[i][j]
                        if a == 0 or b == 0:
                            violated = True
                        elif (c == 1 and not (a < b)) or (c == -1 and not (a > b)):
                            violated = True

                if violated:
                    count += 1

        return count