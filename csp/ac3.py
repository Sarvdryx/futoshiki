from collections import deque
from csp.constraints import revise
def ac3(domains, neighbors, constraints, data):
    queue = deque(constraints)

    while queue:
        xi, xj = queue.popleft()

        if revise(domains, xi, xj, data):
            if not domains[xi]:
                return False

            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return True
def build_graph(data):
    n = data.n

    neighbors = {}
    constraints = []

    # ===== init =====
    for i in range(n):
        for j in range(n):
            neighbors[(i, j)] = set()

    # ===== ROW constraints (all-different) =====
    for i in range(n):
        for j1 in range(n):
            for j2 in range(n):
                if j1 != j2:
                    xi = (i, j1)
                    xj = (i, j2)

                    neighbors[xi].add(xj)
                    constraints.append((xi, xj))

    # ===== COLUMN constraints (all-different) =====
    for j in range(n):
        for i1 in range(n):
            for i2 in range(n):
                if i1 != i2:
                    xi = (i1, j)
                    xj = (i2, j)

                    neighbors[xi].add(xj)
                    constraints.append((xi, xj))

    # ===== HORIZONTAL inequality =====
    for i in range(n):
        for j in range(n - 1):
            if data.h_constraints[i][j] != 0:
                xi = (i, j)
                xj = (i, j + 1)

                neighbors[xi].add(xj)
                neighbors[xj].add(xi)

                constraints.append((xi, xj))
                constraints.append((xj, xi))

    # ===== VERTICAL inequality =====
    for i in range(n - 1):
        for j in range(n):
            if data.v_constraints[i][j] != 0:
                xi = (i, j)
                xj = (i + 1, j)

                neighbors[xi].add(xj)
                neighbors[xj].add(xi)

                constraints.append((xi, xj))
                constraints.append((xj, xi))

    return neighbors, constraints