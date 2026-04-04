from model.board import FutoshikiData
import copy
import time

class Board:
    def __init__(self, data: FutoshikiData):
        self.grid = data.grid
        self.h_constraints = data.h_constraints
        self.v_constraints = data.v_constraints
        self.n = data.n

        self.domains = self.reset_domains()
        self.forward_checking(self.get_variables())

    def get_variables(self):
        variables = []
        for i in range(self.n):
            for j in range(self.n):
                variables.append((i, j))
        return variables

    def reset_domains(self):
        domains = {}

        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    domains[(i, j)] = list(range(1, self.n + 1))
                else:
                    domains[(i, j)] = [self.grid[i][j]]

        self.domains = domains
        return domains

    def forward_checking(self, reassigned_variables):
        for (row, col) in reassigned_variables:
            assigned_value = self.grid[row][col]

            if assigned_value == 0:
                continue

            # =========================
            # ROW constraint
            # =========================
            for j in range(self.n):
                if j != col:
                    if assigned_value in self.domains[(row, j)]:
                        self.domains[(row, j)].remove(assigned_value)

            # =========================
            # COLUMN constraint
            # =========================
            for i in range(self.n):
                if i != row:
                    if assigned_value in self.domains[(i, col)]:
                        self.domains[(i, col)].remove(assigned_value)

            # =========================
            # INEQUALITY - RIGHT
            # =========================
            if col < self.n - 1:
                c = self.h_constraints[row][col]

                if c == '1':  # (row,col) < (row,col+1)
                    if self.grid[row][col+1] != 0:
                        if assigned_value >= self.grid[row][col+1]:
                            return None
                    self.domains[(row, col+1)] = [
                        v for v in self.domains[(row, col+1)]
                        if v > assigned_value
                    ]

                elif c == '-1':  # (row,col) > (row,col+1)
                    if self.grid[row][col+1] != 0:
                        if assigned_value <= self.grid[row][col+1]:
                            return None
                    self.domains[(row, col+1)] = [
                        v for v in self.domains[(row, col+1)]
                        if v < assigned_value
                    ]

            # =========================
            # INEQUALITY - LEFT
            # =========================
            if col > 0:
                c = self.h_constraints[row][col-1]

                if c == '1':  # (row,col-1) < (row,col)
                    if self.grid[row][col-1] != 0:
                        if self.grid[row][col-1] >= assigned_value:
                            return None
                    self.domains[(row, col-1)] = [
                        v for v in self.domains[(row, col-1)]
                        if v < assigned_value
                    ]

                elif c == '-1':  # (row,col-1) > (row,col)
                    if self.grid[row][col-1] != 0:
                        if self.grid[row][col-1] <= assigned_value:
                            return None
                    self.domains[(row, col-1)] = [
                        v for v in self.domains[(row, col-1)]
                        if v > assigned_value
                    ]

            # =========================
            # INEQUALITY - DOWN
            # =========================
            if row < self.n - 1:
                c = self.v_constraints[row][col]

                if c == '1':  # (row,col) < (row+1,col)
                    if self.grid[row+1][col] != 0:
                        if assigned_value >= self.grid[row+1][col]:
                            return None
                    self.domains[(row+1, col)] = [
                        v for v in self.domains[(row+1, col)]
                        if v > assigned_value
                    ]

                elif c == '-1':  # (row,col) > (row+1,col)
                    if self.grid[row+1][col] != 0:
                        if assigned_value <= self.grid[row+1][col]:
                            return None
                    self.domains[(row+1, col)] = [
                        v for v in self.domains[(row+1, col)]
                        if v < assigned_value
                    ]

            # =========================
            # INEQUALITY - UP
            # =========================
            if row > 0:
                c = self.v_constraints[row-1][col]

                if c == '1':  # (row-1,col) < (row,col)
                    if self.grid[row-1][col] != 0:
                        if self.grid[row-1][col] >= assigned_value:
                            return None
                    self.domains[(row-1, col)] = [
                        v for v in self.domains[(row-1, col)]
                        if v < assigned_value
                    ]

                elif c == '-1':  # (row-1,col) > (row,col)
                    if self.grid[row-1][col] != 0:
                        if self.grid[row-1][col] <= assigned_value:
                            return None
                    self.domains[(row-1, col)] = [
                        v for v in self.domains[(row-1, col)]
                        if v > assigned_value
                    ]
        
        # =========================
        # KIỂM TRA TOÀN BỘ CONSTRAINT CHO TẤT CẢ CÁC Ô ĐÃ GÁN
        # =========================
        for i in range(self.n):
            for j in range(self.n-1):
                if self.grid[i][j] != 0 and self.grid[i][j+1] != 0:
                    if self.h_constraints[i][j] == 1 and not (self.grid[i][j] < self.grid[i][j+1]):
                        return None
                    if self.h_constraints[i][j] == -1 and not (self.grid[i][j] > self.grid[i][j+1]):
                        return None
        for i in range(self.n-1):
            for j in range(self.n):
                if self.grid[i][j] != 0 and self.grid[i+1][j] != 0:
                    if self.v_constraints[i][j] == 1 and not (self.grid[i][j] < self.grid[i+1][j]):
                        return None
                    if self.v_constraints[i][j] == -1 and not (self.grid[i][j] > self.grid[i+1][j]):
                        return None

        # =========================
        # CHECK FAILURE
        # =========================
        if any(len(self.domains[var]) == 0 for var in self.domains):
            return None

        return self
    
    def select_unassigned_variable(self):
        unassigned_vars = [
            (i, j)
            for (i, j) in self.domains
            if self.grid[i][j] == 0
        ]

        if not unassigned_vars:
            return None

        # MRV: chọn ô có domain nhỏ nhất
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def is_complete(self):
        return all(
            self.grid[i][j] != 0
            for i in range(self.n)
            for j in range(self.n)
        )
    

def debug_forward_checking(board, var, value):
    i, j = var
    print(f"Assigning ({i},{j}) = {value}")
    
    print("Grid:")
    for row in board.grid:
        print(row)
    
    print("Domains:")
    for key in sorted(board.domains):
        print(f"{key}: {board.domains[key]}")
    
    # Kiểm tra tất cả bất đẳng thức
    for r in range(board.n):
        for c in range(board.n-1):
            if board.h_constraints[r][c] == '1':
                if board.grid[r][c] != 0 and board.grid[r][c+1] != 0:
                    if not board.grid[r][c] < board.grid[r][c+1]:
                        print(f"Violation H: ({r},{c}) < ({r},{c+1})")
            if board.h_constraints[r][c] == '-1':
                if board.grid[r][c] != 0 and board.grid[r][c+1] != 0:
                    if not board.grid[r][c] > board.grid[r][c+1]:
                        print(f"Violation H: ({r},{c}) > ({r},{c+1})")
    for r in range(board.n-1):
        for c in range(board.n):
            if board.v_constraints[r][c] == '1':
                if board.grid[r][c] != 0 and board.grid[r+1][c] != 0:
                    if not board.grid[r][c] < board.grid[r+1][c]:
                        print(f"Violation V: ({r},{c}) < ({r+1},{c})")
            if board.v_constraints[r][c] == '-1':
                if board.grid[r][c] != 0 and board.grid[r+1][c] != 0:
                    if not board.grid[r][c] > board.grid[r+1][c]:
                        print(f"Violation V: ({r},{c}) > ({r+1},{c})")
    
    print("======================")

def backtracking(board, stop_check):
    if stop_check and stop_check():
        return None
    if(board.is_complete()):
        return board
    
    var = board.select_unassigned_variable()

    if not var:
        return None
    
    domain_values = list(board.domains[var])
    for value in domain_values:
        if stop_check and stop_check():
            return None
        original_grid = copy.deepcopy(board.grid)
        original_domains = {k: list(v) for k, v in board.domains.items()}

        i, j = var
        board.grid[i][j] = value              # gán giá trị
        result = board.forward_checking([var])  # forward checking
        debug_forward_checking(board, (i,j), value)

        if result:  # Forward checking succeeded
            # print(f"Forward checking passed for {var} = {value}")
            # Recursive call
            new_result = backtracking(board, stop_check)   
            if new_result:  # Solution found
                return new_result
            
        board.grid = original_grid
        board.domains = original_domains
    
    # print(f"No valid value found for {var}, backtracking...")
    return None

def solve_board(data: FutoshikiData, stop_check=None):

    board = Board(data)
    start_time = time.time()
    # board.domains = board.reset_domains()  # Initialize domains once
    solved_board = backtracking(board, stop_check)
    runtime = time.time() - start_time

    if solved_board:
        data.grid = solved_board.grid
        return solved_board, runtime
    return None, runtime