from fol.logic import And, Or, Not
from fol.symbol import *

# A1: mỗi ô có ít nhất 1 giá trị
def cnf_A1(N):
    clauses = []
    for i in range(1, N+1):
        for j in range(1, N+1):
            clauses.append(
                Or(*[Val(i,j,v) for v in range(1, N+1)])
            )
    return And(*clauses)


# A2: mỗi ô nhiều nhất 1 giá trị
def cnf_A2(N):
    clauses = []
    for i in range(1, N+1):
        for j in range(1, N+1):
            for v1 in range(1, N+1):
                for v2 in range(v1+1, N+1):
                    clauses.append(
                        Or(
                            Not(Val(i,j,v1)),
                            Not(Val(i,j,v2))
                        )
                    )
    return And(*clauses)


# A3: không trùng hàng
def cnf_A3(N):
    clauses = []
    for i in range(1, N+1):
        for v in range(1, N+1):
            for j1 in range(1, N+1):
                for j2 in range(j1+1, N+1):
                    clauses.append(
                        Or(
                            Not(Val(i,j1,v)),
                            Not(Val(i,j2,v))
                        )
                    )
    return And(*clauses)


# A4: LessH
def cnf_A4(N, lessH_list):
    clauses = []
    for (i,j) in lessH_list:
        for v1 in range(1, N+1):
            for v2 in range(1, N+1):
                if v1 >= v2:
                    clauses.append(
                        Or(
                            Not(LessH(i,j)),
                            Not(Val(i,j,v1)),
                            Not(Val(i,j+1,v2))
                        )
                    )
    return And(*clauses)


# A5: Given
def cnf_A5(givens):
    clauses = []
    for (i,j,v) in givens:
        clauses.append(
            Or(
                Not(Given(i,j,v)),
                Val(i,j,v)
            )
        )
    return And(*clauses)

def cnf_A6(N):
    clauses = []
    for j in range(1, N+1):
        for v in range(1, N+1):
            for i1 in range(1, N+1):
                for i2 in range(i1+1, N+1):
                    clauses.append(
                        Or(Not(Val(i1,j,v)), Not(Val(i2,j,v)))
                    )
    return And(*clauses)

# Ràng buộc Lớn hơn Ngang (i, j) > (i, j+1)
def cnf_A7(N, greaterH_list):
    clauses = []
    for (i, j) in greaterH_list:
        for v1 in range(1, N + 1):
            for v2 in range(1, N + 1):
                # Sai logic cũ: v1 > v2 là đúng, vậy VI PHẠM là khi v1 <= v2
                if v1 <= v2: 
                    clauses.append(Or(Not(GreaterH(i, j)), Not(Val(i, j, v1)), Not(Val(i, j+1, v2))))
    return And(*clauses)

# Ràng buộc Nhỏ hơn Dọc (i, j) < (i+1, j)
def cnf_A8(N, lessV_list):
    clauses = []
    for (i, j) in lessV_list:
        for v1 in range(1, N + 1):
            for v2 in range(1, N + 1):
                if v1 >= v2:
                    # Sửa lỗi: Phải so sánh với ô bên dưới (i+1, j) thay vì (i, j+1)
                    clauses.append(Or(Not(LessV(i, j)), Not(Val(i, j, v1)), Not(Val(i+1, j, v2))))
    return And(*clauses)

# Ràng buộc Lớn hơn Dọc (i, j) > (i+1, j)
def cnf_A9(N, greaterV_list):
    clauses = []
    for (i, j) in greaterV_list:
        for v1 in range(1, N + 1):
            for v2 in range(1, N + 1):
                if v1 <= v2:
                    # Sửa lỗi: Phải so sánh với ô bên dưới (i+1, j)
                    clauses.append(Or(Not(GreaterV(i, j)), Not(Val(i, j, v1)), Not(Val(i+1, j, v2))))
    return And(*clauses)