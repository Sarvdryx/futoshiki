from fol.symbol import *

def backward_chain(kb, goal, visited=None, memo=None):
    if visited is None:
        visited = set()
    if memo is None:
        memo = {}

    # MEMO
    if goal in memo:
        return memo[goal]

    # LOOP PREVENTION
    if goal in visited:
        return False

    visited.add(goal)

    try:
        # FACT
        if goal in kb.facts:
            memo[goal] = True
            return True

        # RULE MATCH
        for rule in kb.conclusion_index.get(goal, []):
            ok = True

            for premise in rule.premises:
                if not backward_chain(kb, premise, visited, memo):
                    ok = False
                    break

            if ok:
                memo[goal] = True
                return True

        memo[goal] = False
        return False

    finally:
        visited.remove(goal)

def is_possible_value(kb, i, j, v, memo=None):
    if backward_chain(kb, NotVal(i, j, v), memo=memo):
        return False

    return True

def query_val(kb, i, j, N, memo=None):
    if memo is None:
        memo = {}

    results = []

    for v in range(1, N+1):
        if not backward_chain(kb, NotVal(i, j, v), memo=memo):
            results.append(v)

    return results