from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from ui.board_widget import BoardWidget
from model.board import FutoshikiData
from cnf.build_kb import generate_kb
from utils.random_puzzle import generate_puzzle
from utils.thread_runner import run_in_thread
from horn_clauses.build_horn_kb import build_kb
from inference.forward_chaining import forward_chaining
from solver.smart_fc_solver import solve_board
from solver.backtracking_solver import BacktrackingSolver
from solver.brutefrorce_solver import BruteForceSolver
from solver.astar_solver import AStarSolver
from heuristics.h1_inequality import Heuristic1
from heuristics.h2_ac3 import Heuristic2
from utils.goal import is_valid
import os
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Futoshiki")
        self.resize(1400, 900)
        self.stop_flag = False

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14pt;
            }

            QLineEdit {
                background: #f5f5f5;
                border-radius: 4pt;
                color: black;
            }

            QComboBox {
                padding: 2pt;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout()
        central.setLayout(self.main_layout)

        # ===== TITLE =====
        title = QLabel("Futoshiki")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.main_layout.addWidget(title)

        # ===== TOP CONTROLS =====
        top_layout = QHBoxLayout()

        # choosing file
        self.file_box = QComboBox()
        self.refresh_file_list()
        self.file_box.currentTextChanged.connect(self.load_board_from_file)

        self.size_box = QComboBox()
        self.size_box.addItems(["4", "5", "6", "7", "8", "9"])

        self.diff_box = QComboBox()
        self.diff_box.addItems(["easy", "medium", "hard"])

        self.click_box = QComboBox()
        self.click_box.addItems(["Forward Chaining", "A* (Heuristic 1)", "A* (Heuristic 2)", "Backtracking", "Brute Force"])

        self.random_button = QPushButton("Generate puzzle")
        self.random_button.clicked.connect(self.load_board_from_random_puzzle)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(
            lambda: self.solve_puzzle()
        )

        self.stop_button = QPushButton("Stop")
        self.stop_button.setVisible(False)
        self.stop_button.clicked.connect(self.stop_solving)

        top_layout.addWidget(QLabel("Input File:"))
        top_layout.addWidget(self.file_box)
        top_layout.addWidget(QLabel("Board size:"))
        top_layout.addWidget(self.size_box)
        top_layout.addWidget(QLabel("Difficulty:"))
        top_layout.addWidget(self.diff_box)
        top_layout.addWidget(QLabel("Agents:"))
        top_layout.addWidget(self.click_box)
        top_layout.addWidget(self.random_button)
        top_layout.addWidget(self.solve_button)
        top_layout.addWidget(self.stop_button)
        top_layout.addStretch()

        

        self.main_layout.addLayout(top_layout)
        

        self.controls = [
            self.file_box,
            self.size_box,
            self.diff_box,
            self.click_box,
            self.random_button,
            self.solve_button
        ]

        # ===== MAIN CONTENT AREA (BOARD + LOG) =====
        content_layout = QHBoxLayout()
        content_layout.setSpacing(50) # Khoảng cách giữa Board và Log

        # --- LEFT PANEL (BOARD) ---
        # Sử dụng stretch=3 để Board chiếm 75% chiều ngang
        self.left_container = QWidget()
        self.board_container = QVBoxLayout(self.left_container)
        self.board_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.left_container, stretch=3)

        if self.file_box.count() > 0:
            self.load_board_from_file(self.file_box.currentText())

        # --- RIGHT PANEL (LOG + BUTTONS) ---
        # Sử dụng stretch=1 để Log chiếm 25% chiều ngang
        right_panel_container = QWidget()
        right_panel_layout = QVBoxLayout(right_panel_container)
        right_panel_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Log Box
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("Log output...")
        self.log_box.setFixedSize(500, 300) # Cố định kích thước log theo thiết kế
        right_panel_layout.addWidget(self.log_box)

        # Control Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(0, 20, 0, 0)

        self.undo_button = QPushButton()
        self.pause_button = QPushButton()
        self.ff_button = QPushButton()

        style = self.style()
        self.undo_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward))
        self.pause_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self.ff_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward))
        
        btn_layout.addStretch()
        for btn in [self.undo_button, self.pause_button, self.ff_button]:
            btn.setFixedSize(60, 60) # Tăng kích thước nút cho cân đối
            btn.setIconSize(btn.size() * 0.6)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border-radius: 10px;
                }
            """)
            btn_layout.addWidget(btn)
        btn_layout.addStretch()

        right_panel_layout.addLayout(btn_layout)
        
        # Bọc Right Panel vào một layout để nó luôn nằm giữa theo chiều dọc
        right_wrapper = QVBoxLayout()
        right_wrapper.addStretch()
        right_wrapper.addWidget(right_panel_container)
        right_wrapper.addStretch()

        content_layout.addLayout(right_wrapper, stretch=1)

        self.main_layout.addLayout(content_layout)
        # ===== FOOTER =====
        self.footer = QLabel("Ready")
        self.main_layout.addWidget(self.footer)
    
    def refresh_file_list(self):
        input_dir = "input"

        files = sorted([f for f in os.listdir(input_dir) if f.endswith('.txt')])
        self.file_box.clear()
        self.file_box.addItems(files)
    
    @staticmethod
    def parse_input_file(file_path) -> FutoshikiData:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [
                l.split('#')[0].strip()
                for l in f.readlines()
                if l.split('#')[0].strip()
            ]

        # ===== VALIDATE =====
        if len(lines) == 0:
            raise ValueError("File rỗng")

        N = int(lines[0])

        expected_lines = 1 + N + N + (N - 1)
        if len(lines) < expected_lines:
            raise ValueError("File không đủ dữ liệu")

        data = FutoshikiData(N)

        # ===== GRID =====
        for i in range(N):
            row = [int(x) for x in lines[i + 1].split(',')]
            if len(row) != N:
                raise ValueError(f"Grid dòng {i} sai kích thước")
            data.grid[i] = row

        # ===== HORIZONTAL =====
        data.h_constraints = []
        for i in range(N):
            row = [int(x) for x in lines[N + 1 + i].split(',')]
            if len(row) != N - 1:
                raise ValueError(f"H constraint dòng {i} sai")
            data.h_constraints.append(row)

        # ===== VERTICAL =====
        data.v_constraints = []
        for i in range(N - 1):
            row = [int(x) for x in lines[2 * N + 1 + i].split(',')]
            if len(row) != N:
                raise ValueError(f"V constraint dòng {i} sai")
            data.v_constraints.append(row)

        return data
    
    def clear_board(self):
        while self.board_container.count():
            child = self.board_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def render_board(self, data: FutoshikiData):
        self.board = BoardWidget(data.n)
        self.board.load_from_model(data)

        self.board_container.addWidget(
            self.board,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
    
    def load_board_from_file(self, filename):
        if not filename:
            return

        file_path = os.path.join("input", filename)

        try:
            # 1. Parse
            self.data = self.parse_input_file(file_path)

            # 2. Reset UI
            self.clear_board()

            # 3. Render
            self.render_board(self.data)

        except Exception as e:
            print(f"Lỗi load file '{filename}': {e}")
    

    def load_board_from_random_puzzle(self):
        size = int(self.size_box.currentText())
        difficulty = self.diff_box.currentText()

        self.footer.setText("Starting...")

        def on_done(data):
            self.data = data
            self.clear_board()
            self.render_board(self.data)
            self.footer.setText("Done!")

        self.thread, self.worker = run_in_thread(
            self, 
            generate_puzzle,
            size,
            difficulty,
            on_done=on_done
        )

    # ground cnf KB
    def debug_print_kb(self):
        """In toàn bộ Knowledge Base ra Console để kiểm tra."""
        if not hasattr(self, 'data') or self.data is None:
            print("[KB Debug] Không có dữ liệu bàn cờ để tạo KB.")
            return

        print(f"\n{'='*20} GENERATING KB (N={self.data.n}) {'='*20}")
        
        try:
            kb = generate_kb(self.data)
            
            # 2. Lấy danh sách các câu con (conjuncts) từ And()
            # Trong logic.py của bạn, And lưu các câu con trong self.conjuncts
            clauses = kb.conjuncts
            
            print(f"Tổng số mệnh đề (clauses): {len(clauses)}")
            print(f"Tổng số biến (symbols): {len(kb.symbols())}")
            print("-" * 50)

            # 3. In chi tiết từng mệnh đề
            for i, clause in enumerate(clauses):
                # .formula() giúp hiển thị ký hiệu logic ~, |, & thay vì tên object
                print(f"Clause {i:03d}: {clause.formula()}")
            
            print(f"{'='*25} END KB DEBUG {'='*25}\n")

        except Exception as e:
            print(f"[KB Debug] Lỗi khi tạo KB: {e}")
    
    # ground horn KB
    def debug_print_horn_kb(self, filename="output/horn_kb.txt", limit_rules=1000):
        kb = build_kb(self.data)

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            f.write("========== DEBUG HORN KB ==========\n\n")

            # =====================
            # FACTS
            # =====================
            f.write("FACTS:\n")
            for fact in sorted(kb.facts, key=lambda x: str(x)):
                f.write(f"  {fact}\n")

            f.write(f"\nTotal facts: {len(kb.facts)}\n")

            # =====================
            # RULES
            # =====================
            f.write("\nRULES:\n")

            for i, rule in enumerate(kb.rules):
                if i >= limit_rules:
                    f.write(f"... ({len(kb.rules) - limit_rules} more rules)\n")
                    break

                premises = " ^ ".join(str(p) for p in rule.premises)
                f.write(f"  {premises} => {rule.conclusion}\n")

            f.write(f"\nTotal rules: {len(kb.rules)}\n")
            f.write("\n==================================\n")

        print(f"KB đã được ghi vào file: {filename}")
    
    # forward chaining debug
    def write_kb_to_file(self, filename="output/horn_kb.txt"):
        # =====================
        # Measure build KB
        # =====================
        start_build = time.perf_counter()

        kb = build_kb(self.data)

        end_build = time.perf_counter()
        build_time = end_build - start_build

        # =====================
        # Measure forward chaining
        # =====================
        start_fc = time.perf_counter()

        kb = forward_chaining(kb)

        end_fc = time.perf_counter()
        fc_time = end_fc - start_fc

        with open(filename, "w", encoding="utf-8") as f:

            # =====================
            # FACTS
            # =====================
            f.write("===== FACTS =====\n")
            for fact in sorted(kb.facts, key=str):
                f.write(f"{fact}\n")

            f.write(f"\nTotal facts: {len(kb.facts)}\n")

            # =====================
            # RULES
            # =====================
            f.write("\n===== RULES =====\n")
            for rule in kb.rules:
                f.write(f"{rule}\n")

            f.write(f"\nTotal rules: {len(kb.rules)}\n")

        print(f"KB written to {filename}")
        print(f"Build KB: {build_time:.6f}s")
        print(f"Forward chaining: {fc_time:.6f}s")
        print(f"Total: {(build_time + fc_time):.6f}s")

    def solve_logic(self, data, method, progress_callback=None):
        if self.stop_flag:
            return None, 0
        if method == "Forward Chaining":
            result, runtime = solve_board(data, stop_check=lambda: self.stop_flag)

        elif method == "A* (Heuristic 1)":
            solver = AStarSolver(Heuristic1(), is_valid)
            result, runtime = solver.solve(data, stop_check=lambda: self.stop_flag)

        elif method == "A* (Heuristic 2)":
            solver = AStarSolver(Heuristic2(), is_valid)
            result, runtime = solver.solve(data, stop_check=lambda: self.stop_flag)

        elif method == "Brute Force":
            solver = BruteForceSolver(data)
            result, runtime = solver.solve(stop_check=lambda: self.stop_flag)

        elif method == "Backtracking":
            solver = BacktrackingSolver(data)
            result, runtime = solver.solve(stop_check=lambda: self.stop_flag)

        else:
            raise Exception("Thuật toán không hợp lệ")

        return result, runtime
    
    def solve_puzzle(self):
        method = self.click_box.currentText()

        self.stop_flag = False
        self.set_controls_enabled(False)
        self.stop_button.setVisible(True)
        self.footer.setText("Solving...")

        def on_done(result_tuple):
            result, runtime = result_tuple

            if result is None:
                self.footer.setText("No solution")
            else:
                self.footer.setText(f"Solve in {runtime:.6f}s")

                self.data = result
                self.clear_board()
                self.render_board(self.data)

            self.set_controls_enabled(True)
            self.stop_button.setVisible(False)
            QTimer.singleShot(3000, lambda: self.footer.setText("Ready"))

        self.thread, self.worker = run_in_thread(
            self,
            self.solve_logic,
            self.data,
            method,
            on_done=on_done
        )

    def set_controls_enabled(self, enabled: bool):
        for w in self.controls:
            w.setEnabled(enabled)

    def stop_solving(self):
        self.stop_flag = True
        self.stop_button.setVisible(False)
        self.footer.setText("Ready")