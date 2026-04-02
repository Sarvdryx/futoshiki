from csp.constraints import is_consistent_pair
from parser import parse_input_file
from solver.astar import AStarSolver
from heuristics.h1_inequality import Heuristic1
from heuristics.h2_ac3 import Heuristic2

def is_valid(state, data, i, j, val):
    xi = (i, j)

    for (ni, nj), domain in state.domains.items():
        if (ni, nj) == xi:
            continue

        if state.grid[ni][nj] != 0:
            y = state.grid[ni][nj]

            if not is_consistent_pair(val, y, xi, (ni, nj), data):
                return False

    return True


def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    data = parse_input_file("input/input_01.txt")

    print("=== Heuristic 1 ===")
    solver1 = AStarSolver(Heuristic1(), is_valid)
    sol1 = solver1.solve(data)
    if sol1 is None:
        print("No solution found using Heuristic 1")
    else:
        print_grid(sol1)

    print("\n=== Heuristic 2 ===")
    solver2 = AStarSolver(Heuristic2(), is_valid)
    sol2 = solver2.solve(data)
    if sol2 is None:
        print("No solution found using Heuristic 2")
    else:
        print_grid(sol2)