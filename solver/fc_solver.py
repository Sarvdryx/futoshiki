from fol.symbol import *
from inference.forward_chaining import forward_chaining
from copy import deepcopy
from horn_clauses.build_horn_kb import build_kb
import time
import tracemalloc

nodes_expanded = 0

def domain_init(data):
    N = data.n
    domain = {
        (i, j): set(range(1, N+1))
        for i in range(1, N+1)
        for j in range(1, N+1)
    }
    for i in range(1, N+1):
        for j in range(1, N+1):
            val = data.grid[i-1][j-1]
            if val != 0:
                domain[(i, j)] = {val}
    return domain

def check_conflict(kb):
    fact_names = {f.name for f in kb.facts}

    for fact in kb.facts:
        name, i, j, v = parse_fact(fact)

        if name == "Val":
            not_val_name = f"NotVal_{i}_{j}_{v}"

            if not_val_name in fact_names:
                # print(f"❌ Conflict: Val({i},{j},{v}) & NotVal({i},{j},{v})")
                return True

    return False

def update_domain_from_kb(domain, kb, log_func=None):
    changed = False

    for fact in kb.facts:
        name, i, j, v = parse_fact(fact)

        if name == "NotVal":
            if v in domain[(i, j)]:
                domain[(i, j)].remove(v)
                changed = True

                # 🔥 LOG REDUCE
                if log_func:
                    log_func("reduce", (i-1, j-1), v)

                if len(domain[(i, j)]) == 0:
                    return False, True

        elif name == "Val":
            if domain[(i, j)] != {v}:
                domain[(i, j)] = {v}
                changed = True

                # 🔥 LOG ASSIGN TỪ PROPAGATE
                if log_func:
                    log_func("assign", (i-1, j-1), v)

    return changed, False

def propagate_singletons(domain, kb, log_func=None):
    added = False

    for (i, j), values in domain.items():
        if len(values) == 1:
            v = next(iter(values))
            fact = Val(i, j, v)

            if fact not in kb.facts:
                kb.add_fact(fact)
                added = True

                if log_func:
                    log_func("assign", (i-1, j-1), v)

    return added

def propagate(kb, domain, depth=0, stop_check=None, log_func = None):
    step = 0

    while True:
        if stop_check and stop_check():
            # print(f"[PROP] ⛔ Stopped at depth {depth}")
            return False
        # if depth <= 2:
        #     print(f"\n[PROP][D{depth}] Step {step}")
        #     print(f"Facts: {len(kb.facts)} | Agenda: {len(kb.agenda)}")

        old_domain = {k: set(v) for k, v in domain.items()}

        # 1. forward chaining
        forward_chaining(kb, depth)

        # 2. conflict
        if check_conflict(kb):
            # print(f"❌ Conflict at depth {depth}")
            return False

        # 3. update domain
        changed_domain, contradiction = update_domain_from_kb(domain, kb, log_func)

        # if depth <= 2:
        #     print("Domain snapshot:")
        #     print_domain(domain)

        if contradiction:
            # print(f"❌ Domain wipe at depth {depth}")
            return False

        # 4. singleton
        changed_singleton = propagate_singletons(domain, kb, log_func)

        # if changed_singleton and depth <= 2:
        #     print("   + Singleton → Val")

        if domain == old_domain and not changed_singleton:
            # if depth <= 2:
            #     print("✔ Fixed point")
            break

        step += 1

    return True

def select_mrv(domain):
    best_cell = None
    best_size = float('inf')
    for cell, values in domain.items():
        if len(values) > 1 and len(values) < best_size:
            best_size = len(values)
            best_cell = cell
    return best_cell

def backtrack(kb, domain, depth=0, stop_check=None, trace=None, enable_trace=True):
    def _log(action, cell=None, value=None):
        if enable_trace and trace is not None:
            trace.append({
                "action": action,
                "cell": cell,
                "value": value
            })

    if stop_check and stop_check():
        return None

    global nodes_expanded
    nodes_expanded += 1

    # ===== PROPAGATE =====
    if not propagate(kb, domain, depth, stop_check, _log):
        _log("fail")
        return None

    # ===== GOAL =====
    if all(len(v) == 1 for v in domain.values()):
        for (i, j), values in domain.items():
            _log("assign", (i-1, j-1), next(iter(values)))
        _log("goal")
        return domain

    # ===== CHỌN BIẾN =====
    cell = select_mrv(domain)
    if not cell:
        return None

    i, j = cell

    values = list(sorted(domain[cell]))
    for v in values:
        if stop_check and stop_check():
            return None

        _log("assign", (i-1, j-1), v)

        new_kb = kb.copy()
        new_domain = deepcopy(domain)

        new_domain[(i, j)] = {v}
        new_kb.add_fact(Val(i, j, v))

        result = backtrack(
            new_kb,
            new_domain,
            depth + 1,
            stop_check,
            trace,
            enable_trace
        )

        if result:
            return result

        _log("backtrack", (i-1, j-1), v)

    return None

def fc_solve(data, stop_check=None, enable_trace=True):
    global nodes_expanded
    nodes_expanded = 0

    # 🔥 AUTO DISABLE TRACE
    if data.n >= 5:
        enable_trace = False

    trace = [] if enable_trace else None

    tracemalloc.start()
    start_time = time.perf_counter()

    domain = domain_init(data)
    kb = build_kb(data)

    result = backtrack(
        kb,
        domain,
        depth=0,
        stop_check=stop_check,
        trace=trace,
        enable_trace=enable_trace
    )

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result is None:
        return None, {
            "runtime": end_time - start_time,
            "memory": peak,
            "nodes_expanded": nodes_expanded,
            "trace": trace
        }

    for (i, j), values in result.items():
        data.grid[i-1][j-1] = next(iter(values))

    return data, {
        "runtime": end_time - start_time,
        "memory": peak,
        "nodes_expanded": nodes_expanded,
        "trace": trace
    }

def parse_fact(fact):
    parts = fact.name.split("_")
    name = parts[0]
    if name in ["Val", "NotVal", "Given"]:
        return name, int(parts[1]), int(parts[2]), int(parts[3])
    return name, None, None, None

def print_domain(domain):
    for (i, j), vals in sorted(domain.items()):
        print(f"({i},{j}):{sorted(vals)}", end="  ")
        if j == int(len(domain)**0.5):
            print()
    print()