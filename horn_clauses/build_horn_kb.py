from fol.kb import KnowledgeBase
from fol.rule import Rule
from fol.symbol import *

def build_kb(data):
    kb = KnowledgeBase()
    N = data.n

    # =====================
    # 1. GIVEN → FACT
    # =====================
    for i in range(N):
        for j in range(N):
            v = data.grid[i][j]
            if v != 0:
                kb.add_fact(Given(i+1, j+1, v)) 

    # =====================
    # 2. INEQUALITY → FACT
    # =====================
    for i in range(N):
        for j in range(N-1):
            if data.h_constraints[i][j] == 1:
                kb.add_fact(LessH(i+1, j+1))
            elif data.h_constraints[i][j] == -1:
                kb.add_fact(GreaterH(i+1, j+1))

    for i in range(N-1):
        for j in range(N):
            if data.v_constraints[i][j] == 1:
                kb.add_fact(LessV(i+1, j+1))
            elif data.v_constraints[i][j] == -1:
                kb.add_fact(GreaterV(i+1, j+1))

    # =====================
    # 3. GIVEN ⇒ VAL (FIX)
    # =====================
    # ❗ chỉ tạo rule cho GIVEN thật
    for i in range(N):
        for j in range(N):
            v = data.grid[i][j]
            if v != 0:
                kb.add_rule(
                    Rule(
                        premises=[Given(i+1, j+1, v)],
                        conclusion=Val(i+1, j+1, v)
                    )
                )

    # =====================
    # 4. ROW constraint
    # =====================
    for i in range(1, N+1):
        for v in range(1, N+1):
            for j in range(1, N+1):
                for k in range(1, N+1):
                    if j != k:
                        kb.add_rule(
                            Rule(
                                premises=[Val(i, j, v)],
                                conclusion=NotVal(i, k, v)
                            )
                        )

    # =====================
    # 5. COLUMN constraint
    # =====================
    for j in range(1, N+1):
        for v in range(1, N+1):
            for i in range(1, N+1):
                for k in range(1, N+1):
                    if i != k:
                        kb.add_rule(
                            Rule(
                                premises=[Val(i, j, v)],
                                conclusion=NotVal(k, j, v)
                            )
                        )

    # =====================
    # 6. HORIZONTAL inequality (FIX)
    # =====================
    for i in range(1, N+1):
        for j in range(1, N):

            if LessH(i, j) in kb.facts:
                for v1 in range(1, N+1):
                    for v2 in range(1, N+1):
                        if v2 <= v1:
                            # A -> B
                            kb.add_rule(
                                Rule(
                                    premises=[LessH(i, j), Val(i, j, v1)],
                                    conclusion=NotVal(i, j+1, v2)
                                )
                            )

                            # B -> A
                            kb.add_rule(
                                Rule(
                                    premises=[LessH(i, j), Val(i, j+1, v2)],
                                    conclusion=NotVal(i, j, v1)
                                )
                            )

            if GreaterH(i, j) in kb.facts:
                for v1 in range(1, N+1):
                    for v2 in range(1, N+1):
                        if v2 >= v1:
                            # A -> B
                            kb.add_rule(
                                Rule(
                                    premises=[GreaterH(i, j), Val(i, j, v1)],
                                    conclusion=NotVal(i, j+1, v2)
                                )
                            )

                            # B -> A
                            kb.add_rule(
                                Rule(
                                    premises=[GreaterH(i, j), Val(i, j+1, v2)],
                                    conclusion=NotVal(i, j, v1)
                                )
                            )

    # =====================
    # 7. VERTICAL inequality (FIX)
    # =====================
    for i in range(1, N):
        for j in range(1, N+1):

            if LessV(i, j) in kb.facts:
                for v1 in range(1, N+1):
                    for v2 in range(1, v1+1):   # v2 <= v1

                        # A -> B
                        kb.add_rule(
                            Rule(
                                premises=[LessV(i, j), Val(i, j, v1)],
                                conclusion=NotVal(i+1, j, v2)
                            )
                        )

                        # B -> A
                        kb.add_rule(
                            Rule(
                                premises=[LessV(i, j), Val(i+1, j, v2)],
                                conclusion=NotVal(i, j, v1)
                            )
                        )

            if GreaterV(i, j) in kb.facts:
                for v1 in range(1, N+1):
                    for v2 in range(v1, N+1):   # v2 >= v1

                        # A -> B
                        kb.add_rule(
                            Rule(
                                premises=[GreaterV(i, j), Val(i, j, v1)],
                                conclusion=NotVal(i+1, j, v2)
                            )
                        )

                        # B -> A
                        kb.add_rule(
                            Rule(
                                premises=[GreaterV(i, j), Val(i+1, j, v2)],
                                conclusion=NotVal(i, j, v1)
                            )
                        )

    return kb