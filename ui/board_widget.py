from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

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
        self.prev_grid = None

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
                                       
                        QLineEdit[state="pop"] {
                            background-color: #4ade80;  /* sáng hơn */
                            border: 3px solid #bbf7d0;
                        }
                                       
                        /* ===== EXPAND (node đang mở rộng) ===== */
                        QLineEdit[state="expand"] {
                            background-color: #60a5fa;
                            color: black;
                        }

                        /* ===== CANDIDATE (trong open set) ===== */
                        QLineEdit[state="candidate"] {
                            background-color: #a78bfa;
                            color: black;
                        }

                        /* ===== GOAL ===== */
                        QLineEdit[state="goal"] {
                            background-color: #0f172a;
                            color: #38bdf8;
                            border: 2px solid #3b82f6;
                            border-radius: 8px;
                            font-weight: bold;
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

            cell.setProperty("state", "pop")
            cell.style().unpolish(cell)
            cell.style().polish(cell)

            QTimer.singleShot(120, lambda: self._finish_assign(cell))


        elif action == "reject":
            cell.setProperty("state", "reject")

        elif action == "backtrack":
            cell.setText("")
            cell.setProperty("state", None)

        # refresh style
        cell.style().unpolish(cell)
        cell.style().polish(cell)

    def apply_step_astar(self, step):
        action = step["action"]
        grid = step.get("grid")
        info = step.get("info", {})

        focus_cells = []   # chỉ những cell cần highlight

        # ===== UPDATE GRID (KHÔNG STYLE) =====
        if grid:
            for r in range(len(grid)):
                for c in range(len(grid)):
                    val = grid[r][c]
                    cell = self.cells[(r, c)]

                    # chỉ update nếu khác để tránh repaint
                    if self.prev_grid is None or val != self.prev_grid[r][c]:
                        cell.setText(str(val) if val != 0 else "")

                        # lưu lại cell thay đổi
                        focus_cells.append(cell)

        # ===== RESET STATE CŨ (NHẸ NHÀNG) =====
        if hasattr(self, "last_highlight"):
            for cell in self.last_highlight:
                cell.setProperty("state", None)
                cell.style().unpolish(cell)
                cell.style().polish(cell)

        new_highlight = []

        # ===== APPLY VISUAL (CHỈ 1 ÍT CELL) =====
        if action == "expand":
            # highlight 1 cell đầu tiên (node đang expand)
            if focus_cells:
                c = focus_cells[0]
                c.setProperty("state", "expand")
                new_highlight.append(c)

        elif action == "push":
            # highlight tối đa 2-3 cell thôi (frontier)
            for c in focus_cells[:3]:
                c.setProperty("state", "candidate")
                new_highlight.append(c)

        elif action == "pop":
            if focus_cells:
                c = focus_cells[0]
                c.setProperty("state", "current")
                new_highlight.append(c)

                QTimer.singleShot(80, lambda c=c: self._do_pop(c))

        elif action == "goal":
            for c in self.cells.values():
                c.setProperty("state", "goal")
                c.style().unpolish(c)
                c.style().polish(c)
            self.last_highlight = []
            return

        # ===== APPLY STYLE (CHỈ CELL CẦN) =====
        for cell in new_highlight:
            cell.style().unpolish(cell)
            cell.style().polish(cell)

        self.last_highlight = new_highlight

        # ===== SAVE GRID =====
        self.prev_grid = [row[:] for row in grid] if grid else None

        # ===== LOG =====
        if hasattr(self, "log_box") and info:
            g = info.get("g")
            h = info.get("h")
            f = info.get("f")

            msg = f"[{action.upper()}]"
            if g is not None:
                msg += f" g={g}"
            if h is not None:
                msg += f" h={h}"
            if f is not None:
                msg += f" f={f}"

            self.log_box.append(msg)
        
    def reset_previous_cell(self, new_cell):
        if not self.current_cell:
            return

        if self.current_cell == new_cell:
            return

        self.current_cell.setProperty("state", None)
        self.current_cell.style().unpolish(self.current_cell)
        self.current_cell.style().polish(self.current_cell)


    def highlight_cell(self, cell):
        """Highlight cell đang xét"""
        cell.setProperty("state", "highlight")
        cell.style().unpolish(cell)
        cell.style().polish(cell)

        self.current_cell = cell


    def apply_action(self, cell, action, value):
        """Apply logic chính cho từng action"""

        if action == "assign":
            cell.setText(str(value))

            cell.setProperty("state", "pop")
            cell.style().unpolish(cell)
            cell.style().polish(cell)

            QTimer.singleShot(120, lambda: self._finish_assign(cell))


        elif action == "backtrack":
            cell.setText("")
            cell.setProperty("state", None)

        elif action == "reject":
            cell.setProperty("state", "reject")

        elif action == "fail":
            cell.setProperty("state", "reject")

        elif action == "goal":
            for cell in self.cells.values():
                cell.setProperty("state", "goal")

                cell.style().unpolish(cell)
                cell.style().polish(cell)

            return

        # refresh
        cell.style().unpolish(cell)
        cell.style().polish(cell)


    def handle_global_action(self, action):
        """Xử lý step không có cell"""
        if action == "goal":
            for cell in self.cells.values():
                cell.setProperty("state", "goal")
                cell.style().unpolish(cell)
                cell.style().polish(cell)

        elif action == "fail":
            print("GLOBAL FAIL")


    def apply_step_fc(self, step):
        """Main entry – dễ debug"""

        print("STEP:", step)  

        action = step.get("action")
        cell_pos = step.get("cell")
        value = step.get("value")
        
        if action == "goal":
            # tô màu
            for cell in self.cells.values():
                cell.setProperty("state", "goal")
                cell.style().unpolish(cell)
                cell.style().polish(cell)

            if hasattr(self, "final_grid") and self.final_grid:
                for (r, c), val in self.final_grid.items():
                    cell = self.cells[(r, c)]
                    cell.setText(str(val))

            return

        # ===== GLOBAL STEP =====
        if cell_pos is None:
            self.handle_global_action(action)
            return

        # ===== GET CELL =====
        try:
            r, c = cell_pos
            cell = self.cells[(r, c)]
        except Exception as e:
            print("CELL ERROR:", step, e)
            return

        # ===== RESET OLD =====
        self.reset_previous_cell(cell)

        # ===== HIGHLIGHT =====
        self.highlight_cell(cell)

        # ===== APPLY ACTION =====
        self.apply_action(cell, action, value)
    
    def _finish_assign(self, cell):
        cell.setProperty("state", "assign")

        cell.style().unpolish(cell)
        cell.style().polish(cell)

    def _do_pop(self, cell):
        cell.setProperty("state", "pop")
        cell.style().unpolish(cell)
        cell.style().polish(cell)

        QTimer.singleShot(120, lambda c=cell: self._finish_assign(c))
    
    def highlight_goal(self):
        for cell in self.cells.values():
            cell.setProperty("state", "goal")
            cell.style().unpolish(cell)
            cell.style().polish(cell)