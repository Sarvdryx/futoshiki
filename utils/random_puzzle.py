import random
from model.board import FutoshikiData

def generate_solution(n):
    grid = [[0]*n for _ in range(n)]

    def is_valid(r, c, val):
        for i in range(n):
            if grid[r][i] == val or grid[i][c] == val:
                return False
        return True

    def backtrack():
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    nums = list(range(1, n+1))
                    random.shuffle(nums)
                    for val in nums:
                        if is_valid(r, c, val):
                            grid[r][c] = val
                            if backtrack(): return True
                            grid[r][c] = 0
                    return False
        return True

    backtrack()
    return grid

def generate_constraints(solution, difficulty):
    n = len(solution)
    h = [[0]*(n-1) for _ in range(n)]
    v = [[0]*n for _ in range(n-1)]
    prob = {"easy": 0.15, "medium": 0.25, "hard": 0.35}[difficulty]

    for r in range(n):
        for c in range(n-1):
            if random.random() < prob:
                h[r][c] = 1 if solution[r][c] < solution[r][c+1] else -1
    for r in range(n-1):
        for c in range(n):
            if random.random() < prob:
                v[r][c] = 1 if solution[r][c] < solution[r+1][c] else -1
    return h, v

# --- PHẦN CẢI TIẾN TỐC ĐỘ (Sử dụng Bitmask & MRV) ---

def get_candidates_mask(n, grid, h, v, r, c):
    """Tính toán các giá trị khả thi bằng Bitmask (nhanh hơn vòng lặp)"""
    if grid[r][c] != 0: return 0
    
    # 1. Ràng buộc hàng và cột
    used_mask = 0
    for i in range(n):
        if grid[r][i] != 0: used_mask |= (1 << (grid[r][i] - 1))
        if grid[i][c] != 0: used_mask |= (1 << (grid[i][c] - 1))
    
    candidates = ((1 << n) - 1) & ~used_mask
    
    # 2. Ràng buộc dấu so sánh (Cắt tỉa cực mạnh cho 9x9)
    # LEFT
    if c > 0 and h[r][c-1] != 0 and grid[r][c-1] != 0:
        val_left = grid[r][c-1]
        if h[r][c-1] == 1: candidates &= ~((1 << val_left) - 1) # cur > left
        else: candidates &= (1 << (val_left - 1)) - 1          # cur < left
    # RIGHT
    if c < n-1 and h[r][c] != 0 and grid[r][c+1] != 0:
        val_right = grid[r][c+1]
        if h[r][c] == 1: candidates &= (1 << (val_right - 1)) - 1 # cur < right
        else: candidates &= ~((1 << val_right) - 1)               # cur > right
    # UP
    if r > 0 and v[r-1][c] != 0 and grid[r-1][c] != 0:
        val_up = grid[r-1][c]
        if v[r-1][c] == 1: candidates &= ~((1 << val_up) - 1) # cur > up
        else: candidates &= (1 << (val_up - 1)) - 1           # cur < up
    # DOWN
    if r < n-1 and v[r][c] != 0 and grid[r+1][c] != 0:
        val_down = grid[r+1][c]
        if v[r][c] == 1: candidates &= (1 << (val_down - 1)) - 1 # cur < down
        else: candidates &= ~((1 << val_down) - 1)               # cur > down

    return candidates

def count_solutions(grid, h, v, limit=2):
    """Bộ giải tối ưu sử dụng Heuristic MRV để check tính duy nhất"""
    n = len(grid)
    solutions_found = 0

    def backtrack_fast():
        nonlocal solutions_found
        if solutions_found >= limit: return

        # Tìm ô có ít lựa chọn nhất (MRV)
        best_r, best_c, best_mask = -1, -1, -1
        min_choices = n + 1

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    mask = get_candidates_mask(n, grid, h, v, r, c)
                    count = bin(mask).count('1')
                    if count == 0: return # Không có cách giải
                    if count < min_choices:
                        min_choices = count
                        best_r, best_c, best_mask = r, c, mask
                        if count == 1: break # Tối ưu: Thấy ô 1 lựa chọn thì chọn luôn
            if min_choices == 1: break

        if best_r == -1: # Đã điền hết bảng
            solutions_found += 1
            return

        # Thử các giá trị khả thi từ mask
        for val in range(1, n + 1):
            if best_mask & (1 << (val - 1)):
                grid[best_r][best_c] = val
                backtrack_fast()
                grid[best_r][best_c] = 0
                if solutions_found >= limit: return

    backtrack_fast()
    return solutions_found

# --- CÁC HÀM CÒN LẠI GIỮ NGUYÊN LOGIC CỦA BẠN ---

def remove_numbers_unique(solution, h, v, difficulty):
    n = len(solution)
    puzzle = [row[:] for row in solution]

    # Danh sách các ô và xáo trộn
    cells = [(r, c) for r in range(n) for c in range(n)]
    random.shuffle(cells)

    # Xác định ngưỡng ô trống theo difficulty
    stop_threshold = {"easy": n*n*0.4, "medium": n*n*0.6, "hard": n*n}[difficulty]

    # 1️⃣ Giai đoạn xóa đối xứng
    removed = set()  # để tránh check trùng
    for r, c in cells:
        if puzzle[r][c] == 0 or (r, c) in removed:
            continue

        opp_r, opp_c = n-1-r, n-1-c

        # backup giá trị
        backup = puzzle[r][c]
        backup_opp = puzzle[opp_r][opp_c]

        # xóa thử
        puzzle[r][c] = 0
        puzzle[opp_r][opp_c] = 0

        if count_solutions(puzzle, h, v, 2) != 1:
            # khôi phục
            puzzle[r][c] = backup
            puzzle[opp_r][opp_c] = backup_opp
        else:
            removed.add((r, c))
            removed.add((opp_r, opp_c))

        # Kiểm tra stop threshold
        empty_count = sum(row.count(0) for row in puzzle)
        if difficulty != "hard" and empty_count >= stop_threshold:
            break

    # 2️⃣ Giai đoạn quét sạch các ô lẻ còn sót lại
    random.shuffle(cells)
    for r, c in cells:
        if puzzle[r][c] == 0:
            continue

        backup = puzzle[r][c]
        puzzle[r][c] = 0

        if count_solutions(puzzle, h, v, 2) != 1:
            puzzle[r][c] = backup

        empty_count = sum(row.count(0) for row in puzzle)
        if difficulty != "hard" and empty_count >= stop_threshold:
            break

    return puzzle

def generate_puzzle(size, difficulty, progress_callback=None):
    for attempt in range(50):
        if progress_callback: progress_callback(f"Attempt {attempt+1}...")
        
        solution = generate_solution(size)
        h, v = generate_constraints(solution, difficulty)
        puzzle = remove_numbers_unique(solution, h, v, difficulty)

        data = FutoshikiData(size)
        data.grid = puzzle
        data.h_constraints = h
        data.v_constraints = v
        return data

    raise Exception("Không generate được puzzle")