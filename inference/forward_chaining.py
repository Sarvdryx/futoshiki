def forward_chaining(kb, depth=0):
    while kb.agenda:
        p = kb.agenda.pop()

        if p not in kb.index:
            continue

        for rule in kb.index[p]:
            if rule.count <= 0:
                continue
            rule.count -= 1

            if rule.count == 0:
                concl = rule.conclusion
                if concl not in kb.facts:
                    kb.add_fact(concl)

    return kb