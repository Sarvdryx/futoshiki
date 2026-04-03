def revise(domains, xi, xj, data):
    """
    domains: dict {(i,j): [values]}
    xi, xj: tuple (i,j)
    data: FutoshikiData
    """

    revised = False
    i1, j1 = xi
    i2, j2 = xj

    new_domain = []

    for x in domains[xi]:
        ok = False

        for y in domains[xj]:
            if is_consistent_pair(x, y, xi, xj, data):
                ok = True
                break

        if ok:
            new_domain.append(x)
        else:
            revised = True

    domains[xi] = new_domain
    return revised

def is_consistent_pair(x, y, xi, xj, data):
    i1, j1 = xi
    i2, j2 = xj

    # ===== ROW constraint (all-different) =====
    if i1 == i2:
        if x == y:
            return False

    # ===== COLUMN constraint (all-different) =====
    if j1 == j2:
        if x == y:
            return False

    # ===== HORIZONTAL inequality =====
    if i1 == i2 and abs(j1 - j2) == 1:
        row = i1
        col = min(j1, j2)

        c = data.h_constraints[row][col]

        if c != 0:
            if j1 < j2:  # xi bên trái xj
                if c == 1 and not (x < y):
                    return False
                if c == -1 and not (x > y):
                    return False
            else:  # xi bên phải xj
                if c == 1 and not (y < x):
                    return False
                if c == -1 and not (y > x):
                    return False

    # ===== VERTICAL inequality =====
    if j1 == j2 and abs(i1 - i2) == 1:
        col = j1
        row = min(i1, i2)

        c = data.v_constraints[row][col]

        if c != 0:
            if i1 < i2:  # xi ở trên xj
                if c == 1 and not (x < y):
                    return False
                if c == -1 and not (x > y):
                    return False
            else:  # xi ở dưới xj
                if c == 1 and not (y < x):
                    return False
                if c == -1 and not (y > x):
                    return False

    return True