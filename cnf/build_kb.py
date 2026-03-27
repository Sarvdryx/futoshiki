from fol.logic import And
from fol.axiom import cnf_A1, cnf_A2, cnf_A3, cnf_A4, cnf_A5, cnf_A6, cnf_A7, cnf_A8, cnf_A9
from fol.symbol import Given, LessH, GreaterH, LessV, GreaterV

def generate_kb(board_data):
    """
    Tự động tạo Knowledge Base (KB) dưới dạng một câu logic AND khổng lồ.
    """
    N = board_data.n
    kb = And()

    # 1. Thêm các quy tắc cơ bản của trò chơi (Luật Futoshiki)
    kb.add(cnf_A1(N))  # Mỗi ô có ít nhất 1 giá trị
    kb.add(cnf_A2(N))  # Mỗi ô có tối đa 1 giá trị
    kb.add(cnf_A3(N))  # Không trùng hàng (bạn có thể viết thêm cnf_A3_col cho cột)
    kb.add(cnf_A6(N))


    # 2. Thêm các giá trị đã cho sẵn trên bàn cờ
    givens = []
    for i in range(N):
        for j in range(N):
            val = board_data.grid[i][j]
            if val != 0:
                # Tọa độ trong logic thường bắt đầu từ 1
                givens.append((i + 1, j + 1, val))
                # Khai báo rằng Given(i,j,v) là ĐÚNG
                kb.add(Given(i + 1, j + 1, val)) 
    
    if givens:
        kb.add(cnf_A5(givens)) # Áp dụng tiên đề Given => Val

    # --- 3. Ràng buộc ngang (Horizontal) ---
    lh, gh = [], []
    for i in range(N):
        for j in range(N-1):
            constraint = board_data.h_constraints[i][j]
            if constraint == 1: # Left < Right
                lh.append((i+1, j+1))
                kb.add(LessH(i+1, j+1))
            elif constraint == -1: # Left > Right
                gh.append((i+1, j+1))
                kb.add(GreaterH(i+1, j+1))
    
    if lh: kb.add(cnf_A4(N, lh)) # cnf_A4 chính là cnf_LessH
    if gh: kb.add(cnf_A7(N, gh))

    # --- 4. Ràng buộc dọc (Vertical) ---
    lv, gv = [], []
    for i in range(N-1):
        for j in range(N):
            constraint = board_data.v_constraints[i][j]
            if constraint == 1: # Top < Bottom
                lv.append((i+1, j+1))
                kb.add(LessV(i+1, j+1))
            elif constraint == -1: # Top > Bottom
                gv.append((i+1, j+1))
                kb.add(GreaterV(i+1, j+1))
                
    if lv: kb.add(cnf_A8(N, lv))
    if gv: kb.add(cnf_A9(N, gv))

    return kb