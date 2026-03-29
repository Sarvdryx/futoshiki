from fol.symbol import *
from inference.forward_chaining import forward_chaining
from copy import deepcopy
from horn_clauses.build_horn_kb import build_kb

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
    for fact in kb.facts:
        name, i, j, v = parse_fact(fact)

        if name == "Val":
            if NotVal(i, j, v) in kb.facts:
                return True
    return False

def update_domain_from_kb(domain, kb):
    changed = False

    for fact in kb.facts:
        name, i, j, v = parse_fact(fact)

        if name == "NotVal":
            if v in domain[(i, j)]:
                domain[(i, j)].remove(v)
                changed = True

                if len(domain[(i, j)]) == 0:
                    return False, True

        elif name == "Val":
            if domain[(i, j)] != {v}:
                domain[(i, j)] = {v}
                changed = True

    return changed, False

def propagate_singletons(domain, kb):
    added = False

    for (i, j), values in domain.items():
        if len(values) == 1:
            v = next(iter(values))

            fact = Val(i, j, v)
            if fact not in kb.facts:
                kb.facts.add(fact)
                added = True

    return added

def propagate(kb, domain, depth=0):
    step = 0

    while True:
        print(f"\n[Depth {depth}] Step {step}")

        # DEBUG: lưu facts trước
        old_facts = set(kb.facts)

        # 1. forward chaining
        forward_chaining(kb)

        # DEBUG: in fact mới
        print_new_facts(old_facts, kb.facts)

        # ❗ check conflict
        if check_conflict(kb):
            print("  ❌ Conflict detected (Val ∧ NotVal)")
            return False

        # 2. update domain
        print("  Updating domain...")
        changed1, contradiction = update_domain_from_kb(domain, kb)

        print_domain(domain, prefix="  ")

        if contradiction:
            print("  ❌ Domain wiped out → contradiction")
            return False

        # 3. singleton → Val
        print("  Propagate singleton...")
        changed2 = propagate_singletons(domain, kb)

        # DEBUG: show singleton facts
        if changed2:
            print("  + Singleton -> Val added")

        if check_conflict(kb):
            print("  ❌ Conflict after singleton")
            return False

        if not changed1 and not changed2:
            print("  ✔ Fixed point reached")
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

def backtrack(kb, domain, depth=0):
    print(f"\n{'='*40}")
    print(f"BACKTRACK depth = {depth}")
    print_domain(domain)

    # 1. propagate
    if not propagate(kb, domain, depth):
        print(f"[Depth {depth}] ❌ Fail (propagate)")
        return None

    # 2. check solved
    if all(len(v) == 1 for v in domain.values()):
        print(f"[Depth {depth}] ✅ SOLVED")
        return domain

    # 3. MRV
    cell = select_mrv(domain)
    i, j = cell

    print(f"[Depth {depth}] Choose cell ({i},{j}) with {domain[cell]}")

    for v in list(domain[cell]):
        print(f"[Depth {depth}] TRY ({i},{j}) = {v}")

        new_kb = kb.copy()
        new_domain = deepcopy(domain)

        new_domain[(i, j)] = {v}
        new_kb.facts.add(Val(i, j, v))

        result = backtrack(new_kb, new_domain, depth+1)

        if result:
            return result

        print(f"[Depth {depth}] ❌ Backtrack ({i},{j}) = {v}")

    return None

def fc_solve(data):
    # 1. Khởi tạo domain
    domain = domain_init(data)

    # 2. Build KB từ data
    kb = build_kb(data)

    # 3. (optional) chạy forward chaining ban đầu
    # forward_chaining(kb)

    # 4. Gọi backtracking
    result = backtrack(kb, domain)

    # 5. Nếu không có lời giải
    if result is None:
        print("Không có lời giải")
        return None

    # 6. Nếu có lời giải → ghi lại vào grid
    N = data.n
    for i in range(1, N+1):
        for j in range(1, N+1):
            values = result[(i, j)]

            # đảm bảo đã solve hoàn toàn
            if len(values) != 1:
                print("Lỗi: nghiệm chưa hoàn chỉnh")
                return None

            v = next(iter(values))
            data.grid[i-1][j-1] = v

    print("Giải thành công!")
    return data

def print_domain(domain, prefix=""):
    print(prefix + "DOMAIN:")
    for (i, j), values in sorted(domain.items()):
        print(f"  ({i},{j}) = {sorted(values)}")
    print()

def print_new_facts(old_facts, new_facts):
    added = new_facts - old_facts
    if added:
        print("  + New facts:")
        for f in added:
            print("   ", f)

def parse_fact(fact):
    parts = fact.name.split("_")

    name = parts[0]

    if name in ["Val", "NotVal", "Given"]:
        i, j, v = map(int, parts[1:])
        return name, i, j, v

    elif name in ["LessH", "GreaterH", "LessV", "GreaterV", "Less"]:
        i, j = map(int, parts[1:])
        return name, i, j, None

    return name, None, None, None