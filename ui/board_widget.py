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
        self.current_cell = None

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
                                                /* highlight riêng */
                        QLineEdit[highlight="true"] {
                            border: 3px solid #facc15;
                        }

                        /* trạng thái */
                        QLineEdit[state="assign"] {
                            background-color: #22c55e;
                            color: black;
                        }

                        QLineEdit[state="reject"] {
                            background-color: #ef4444;
                            color: white;
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
                        QLineEdit:hover {
                            border: 2px solid #38bdf8;
                                                }
                                                /* highlight riêng */
                        QLineEdit[highlight="true"] {
                            border: 3px solid #facc15;
                        }

                        /* trạng thái */
                        QLineEdit[state="assign"] {
                            background-color: #22c55e;
                            color: black;
                        }

                        QLineEdit[state="reject"] {
                            background-color: #ef4444;
                            color: white;
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
                        QLineEdit:hover {
                            border: 2px solid #38bdf8;
                                                }
                                                /* highlight riêng */
                        QLineEdit[highlight="true"] {
                            border: 3px solid #facc15;
                        }

                        /* trạng thái */
                        QLineEdit[state="assign"] {
                            background-color: #22c55e;
                            color: black;
                        }

                        QLineEdit[state="reject"] {
                            background-color: #ef4444;
                            color: white;
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

    def apply_step(self, step):
        action = step["action"]
        r, c = step["cell"]
        val = step["value"]

        cell = self.cells[(r, c)]

        # ===== RESET ô cũ =====
        if self.current_cell and self.current_cell != cell:
            self.current_cell.setProperty("state", None)
            self.current_cell.style().unpolish(self.current_cell)
            self.current_cell.style().polish(self.current_cell)

        # ===== HIGHLIGHT ô đang xét =====
        cell.setProperty("state", "highlight")
        cell.style().unpolish(cell)
        cell.style().polish(cell)

        self.current_cell = cell

        # ===== APPLY ACTION =====
        if action == "assign":
            cell.setText(str(val))
            cell.setProperty("state", "assign")

        elif action == "reject":
            cell.setProperty("state", "reject")

        elif action == "backtrack":
            cell.setText("")
            cell.setProperty("state", None)

        # refresh style
        cell.style().unpolish(cell)
        cell.style().polish(cell)