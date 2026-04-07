from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


class BoardWidget(QWidget):
    def __init__(self, size=4):
        super().__init__()
        self.size = size

        self.setStyleSheet("""
            QWidget {
                background-color: #020617;
                border: 2px solid #1e293b;
                border-radius: 12px;
            }
        """)

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

            for j in range(2 * N - 1):
                self.layout.setRowStretch(i, 0)
                self.layout.setColumnStretch(i, 0)
                # ===== CELL =====
                if i % 2 == 0 and j % 2 == 0:
                    cell = QLineEdit()
                    cell.setFixedSize(40, 40)
                    cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setReadOnly(True)

                    cell.setStyleSheet("""
                        QLineEdit {
                            background-color: #1e293b;
                            color: #f8fafc;
                            border: 2px solid #334155;
                            border-radius: 8px;
                            font-weight: bold;
                        }
                        QLineEdit:hover {
                            border: 2px solid #38bdf8;
                        }
                    """)

                    self.layout.addWidget(cell, i, j)
                    self.cells[(i // 2, j // 2)] = cell

                # ===== HORIZONTAL CONSTRAINT =====
                elif i % 2 == 0:
                    lbl = QLabel("")
                    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    lbl.setFixedSize(20, 40)

                    lbl.setStyleSheet("""
                        QLabel {
                            color: #facc15;
                            font-weight: bold;
                            border-radius: 4px;
                            background-color: transparent
                        }
                    """)

                    self.layout.addWidget(lbl, i, j)
                    self.h_labels[(i // 2, j // 2)] = lbl

                # ===== VERTICAL CONSTRAINT =====
                elif j % 2 == 0:
                    lbl = QLabel("")
                    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    lbl.setFixedSize(40, 20)

                    lbl.setStyleSheet("""
                        QLabel {
                            color: #facc15;
                            font-weight: bold;
                            border-radius: 4px;
                            background-color: transparent
                        }
                    """)

                    self.layout.addWidget(lbl, i, j)
                    self.v_labels[(i // 2, j // 2)] = lbl

    def load_from_model(self, data):
        for r in range(data.n):
            for c in range(data.n):
                val = data.grid[r][c]
                cell = self.cells[(r, c)]

                cell.setText(str(val) if val != 0 else "")

                # ===== FILLED CELL =====
                if val != 0:
                    cell.setStyleSheet("""
                        QLineEdit {
                            background-color: #0f172a;
                            color: #38bdf8;
                            border: 2px solid #3b82f6;
                            border-radius: 8px;
                            font-weight: bold;
                        }
                    """)
                else:
                    # ===== EMPTY CELL =====
                    cell.setStyleSheet("""
                        QLineEdit {
                            background-color: #1e293b;
                            color: #f8fafc;
                            border: 2px solid #334155;
                            border-radius: 8px;
                        }
                    """)

                cell.setReadOnly(True)

        # ===== HORIZONTAL CONSTRAINT =====
        for r, row in enumerate(data.h_constraints):
            for c, val in enumerate(row):
                lbl = self.h_labels[(r, c)]

                if val == 1:
                    lbl.setText("<")
                    lbl.setStyleSheet("""
                        QLabel {
                            color: #22c55e;
                            font-weight: bold;
                            border-radius: 4px;
                            background-color: transparent;
                        }
                    """)
                    lbl.setFixedSize(20, 40)
                elif val == -1:
                    lbl.setText(">")
                    lbl.setStyleSheet("""
                        QLabel {
                            color: #22c55e;
                            font-weight: bold;
                            border-radius: 4px;
                            background-color: transparent;
                        }
                    """)
                    lbl.setFixedSize(20, 40)
                else:
                    lbl.setText("")

        # ===== VERTICAL CONSTRAINT =====
        for r, row in enumerate(data.v_constraints):
            for c, val in enumerate(row):
                lbl = self.v_labels[(r, c)]

                if val == 1:
                    lbl.setText("∧")
                    lbl.setStyleSheet("""
                        QLabel {
                            color: #22c55e;
                            font-weight: bold;
                            border-radius: 4px;
                            background-color: transparent
                        }
                    """)
                    lbl.setFixedSize(40, 20)
                elif val == -1:
                    lbl.setText("∨")
                    lbl.setStyleSheet("""
                        QLabel {
                            color: #22c55e;
                            font-size: 18px;
                            font-weight: bold;
                            border-radius: 4px;
                            background-color: transparent
                        }
                    """)
                    lbl.setFixedSize(40, 20)
                else:
                    lbl.setText("")