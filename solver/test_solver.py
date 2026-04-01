from solver.backtracking_solver import BacktrackingSolver
from solver.bruteforce_solver import BruteForceSolver
from utils.parse_input import parse_input_file  
def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))
    print()


def test_backtracking(file_path):
    print("=== BACKTRACKING ===")
    data = parse_input_file(file_path)

    solver = BacktrackingSolver(data)
    result = solver.solve()

    if result:
        print_grid(result.grid)
        print("Steps:", solver.steps)
        print("Backtracks:", solver.backtracks)
    else:
        print("No solution")


def test_bruteforce(file_path):
    print("=== BRUTE FORCE ===")
    data = parse_input_file(file_path)

    solver = BruteForceSolver(data)
    result = solver.solve()

    if result:
        print_grid(result.grid)
        print("Steps:", solver.steps)
    else:
        print("No solution")


if __name__ == "__main__":
    file = "input/input_01.txt"

    test_backtracking(file)
    test_bruteforce(file)