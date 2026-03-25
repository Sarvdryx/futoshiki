from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


class BoardWidget(QWidget):
    def __init__(self, size=4):
        super().__init__()
        self.size = size

        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        self.cells = {}
        self.h_labels = {}
        self.v_labels = {}

        self.build_grid()

    def build_grid(self):
        N = self.size

        for i in range(2 * N - 1):
            if i % 2 == 1:
                self.layout.setRowMinimumHeight(i, 20)
                self.layout.setColumnMinimumWidth(i, 20)
            for j in range(2 * N - 1):

                if i % 2 == 0 and j % 2 == 0:
                    cell = QLineEdit()
                    cell.setFixedSize(45, 45)
                    cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setReadOnly(True)
                    self.layout.addWidget(cell, i, j)
                    self.cells[(i // 2, j // 2)] = cell

                elif i % 2 == 0:
                    lbl = QLabel("")
                    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.layout.addWidget(lbl, i, j)
                    self.h_labels[(i // 2, j // 2)] = lbl

                elif j % 2 == 0:
                    lbl = QLabel("")
                    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.layout.addWidget(lbl, i, j)
                    self.v_labels[(i // 2, j // 2)] = lbl

    def load_from_model(self, data):
        for r in range(data.n):
            for c in range(data.n):
                val = data.grid[r][c]
                cell = self.cells[(r, c)]

                cell.setText(str(val) if val != 0 else "")
                cell.setReadOnly(val != 0)
                cell.setStyleSheet("background: #ddd;" if val else "")
                cell.setReadOnly(True)

        for r, row in enumerate(data.h_constraints):
            for c, val in enumerate(row):
                self.h_labels[(r, c)].setText(
                    "<" if val == 1 else ">" if val == -1 else ""
                )

        for r, row in enumerate(data.v_constraints):
            for c, val in enumerate(row):
                self.v_labels[(r, c)].setText(
                    "∧" if val == 1 else "∨" if val == -1 else ""
                )