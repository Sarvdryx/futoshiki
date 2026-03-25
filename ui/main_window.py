from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ui.board_widget import BoardWidget
from model.board import FutoshikiData
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Futoshiki")
        self.resize(1200, 900)

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
        self.click_box.addItems(["show selector", "auto fill"])

        top_layout.addWidget(QLabel("Input File:"))
        top_layout.addWidget(self.file_box)
        top_layout.addWidget(QLabel("Board size:"))
        top_layout.addWidget(self.size_box)
        top_layout.addWidget(QLabel("Difficulty:"))
        top_layout.addWidget(self.diff_box)
        top_layout.addWidget(QLabel("On click:"))
        top_layout.addWidget(self.click_box)
        top_layout.addStretch()

        self.main_layout.addLayout(top_layout)

        # ===== BOARD =====
        self.board_container = QVBoxLayout()
        self.main_layout.addLayout(self.board_container)
        if self.file_box.count() > 0:
            self.load_board_from_file(self.file_box.currentText())

        # ===== FOOTER =====
        footer = QLabel("The game automatically detects a correct solution.")
        self.main_layout.addWidget(footer)
    
    def refresh_file_list(self):
        input_dir = "input"

        files = sorted([f for f in os.listdir(input_dir) if f.endswith('.txt')])
        self.file_box.clear()
        self.file_box.addItems(files)
    
    def parse_input_file(self, file_path) -> FutoshikiData:
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
        
