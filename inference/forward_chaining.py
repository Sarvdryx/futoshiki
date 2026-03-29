def forward_chaining(kb):
    facts = kb.facts              # set
    rules = kb.rules              # list

    # =====================
    # 1. Build index: premise → rules
    # =====================
    index = {}  # dict: premise -> list of rules

    for rule in rules:
        for p in rule.premises:
            if p not in index:
                index[p] = []
            index[p].append(rule)

    # =====================
    # 2. Agenda (queue các fact mới)
    # =====================
    agenda = list(facts)

    # =====================
    # 3. Forward chaining loop
    # =====================
    while agenda:
        fact = agenda.pop()

        # Nếu fact không nằm trong index → không ảnh hưởng rule nào
        if fact not in index:
            continue

        # Chỉ xét các rule có chứa fact này
        for rule in index[fact]:

            # Kiểm tra đủ premise chưa
            if all(p in facts for p in rule.premises):

                conclusion = rule.conclusion

                # Nếu là fact mới → thêm vào KB
                if conclusion not in facts:
                    facts.add(conclusion)
                    agenda.append(conclusion)

    return kb