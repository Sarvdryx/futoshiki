import os
import pandas as pd
from copy import deepcopy
from solver.fc_solver import fc_solve
from solver.backtracking_solver import BacktrackingSolver
from solver.brutefrorce_solver import BruteForceSolver
from solver.astar_solver import AStarSolver
from heuristics.h1_inequality import Heuristic1
from heuristics.h2_ac3 import Heuristic2
from utils.goal import is_valid
from utils.parse import parse_input_file
import time

def make_stop_check(time_limit=300):  # 5 phút
    start = time.perf_counter()

    def check():
        return time.perf_counter() - start > time_limit

    return check

def run_solver(method, data, stop_check):
    if method == "Forward Chaining":
        return fc_solve(data, stop_check=stop_check)

    elif method == "A* (Heuristic 1)":
        solver = AStarSolver(Heuristic1(), is_valid)
        return solver.solve(data, stop_check=stop_check)

    elif method == "A* (Heuristic 2)":
        solver = AStarSolver(Heuristic2(), is_valid)
        return solver.solve(data, stop_check=stop_check)

    elif method == "Brute Force":
        solver = BruteForceSolver(data)
        return solver.solve(stop_check=stop_check)

    elif method == "Backtracking":
        solver = BacktrackingSolver(data)
        return solver.solve(stop_check=stop_check)

    return None, None


def benchmark_one(input_file):
    methods = [
        "Forward Chaining",
        "A* (Heuristic 1)",
        "A* (Heuristic 2)",
        "Brute Force",
        "Backtracking"
    ]

    results = []

    print(f"\n===== Running {input_file} =====")

    data = parse_input_file(input_file)

    for method in methods:
        print(f"→ {method}")

        data_copy = deepcopy(data)
        stop_check = make_stop_check(300)

        try:
            result, stats = run_solver(method, data_copy, stop_check)
            timed_out = stop_check()

            results.append({
                "input": os.path.basename(input_file),
                "method": method,
                "runtime": stats["runtime"],
                "memory": stats["memory"],
                "nodes_expanded": stats["nodes_expanded"],
                "solved": result is not None,
                "timeout": timed_out
            })

        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "input": os.path.basename(input_file),
                "method": method,
                "runtime": None,
                "memory": None,
                "nodes_expanded": None,
                "solved": False,
                "timeout": timed_out
            })

    df = pd.DataFrame(results)
    df["memory_mb"] = df["memory"] / (1024 * 1024)
    return df