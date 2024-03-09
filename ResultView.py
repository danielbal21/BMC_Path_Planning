import sys

from PyQt5 import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, \
    QScrollArea
from PyQt5.QtGui import QColor
from z3 import sat, unsat

from Utils.Visual import GridDrawerWidget


class ResultView(QWidget):
    def __init__(self, parent, N, result, M2, total_time=0, time_per_iter=0):
        super().__init__()
        self.time_label = None
        self.bad_robot = None
        self.parent = parent
        self.grid_widget = None
        self.N = N
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_movement)
        self.t = 0
        self.status = result[0]
        self.result = result[1]
        self.total_time = total_time
        self.time_per_iter = time_per_iter
        self.M2 = M2
        self.parent.window.setGeometry(100, 100, 650, 550)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header_layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Label
        header_label = QLabel("Result Summary", self)
        header_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)  # Centered at the top
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 0px;")
        header_layout.addWidget(header_label)
        layout.addLayout(header_layout)

        if self.status == sat:
            stat_layout = QHBoxLayout(self)
            sub_layout = QScrollArea(self)
            # Time Label
            self.time_label = QLabel("T=0", self)
            self.time_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 0px;")
            self.time_label.setContentsMargins(0, 0, 5, 0)
            # Time took
            time_took_label = QLabel(f"Total Time: {self.total_time} secs | ", self)
            time_took_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 0px;")

            # Time per iteration
            time_per_iter = QLabel(f"Time per iteration: {self.time_per_iter:.2f} secs", self)
            time_per_iter.setStyleSheet("font-size: 18px; font-weight: bold; margin: 0px;")

            stat_layout.addWidget(self.time_label)
            stat_layout.addWidget(time_took_label)
            stat_layout.addWidget(time_per_iter)
            stat_layout.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)

            layout.addLayout(stat_layout)

            # Grid
            self.grid_widget = GridDrawerWidget(self.N, 640, 480)
            sub_layout.setWidget(self.grid_widget)
            sub_layout.setWidgetResizable(True)
            layout.addWidget(sub_layout)
            self.update_movement()
            self.timer.start(1000)

        elif self.status == unsat:
            # Error Label
            msg_label = QLabel("There is no solution for this problem", self)
            msg_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)  # Centered at the top
            msg_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 0px;")
            layout.addWidget(msg_label)

        elif self.status == 'timeout':
            msg_label = QLabel("Could not find a solution within the specified time", self)
            msg_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)  # Centered at the top
            msg_label.setStyleSheet("font-size: 28px; font-weight: bold; margin: 0px;")
            layout.addWidget(msg_label)

        self.setLayout(layout)

    def update_movement(self):
        self.time_label.setText(f'T={self.t + 1}/{len(self.result)} |')
        if self.t == 0:
            self.bad_robot = self.M2.get_initial_state().node_id
        else:
            self.bad_robot = list(self.M2.relations[self.bad_robot])[0]
            pass
        self.grid_widget.mark_rectangle_bad(self.extract_present(self.M2.nodes[self.bad_robot].properties, self.N))
        row = self.result[self.t][0]
        column = self.result[self.t][1]
        self.grid_widget.mark_rectangle_good(row, column)
        self.grid_widget.update()
        self.t = (self.t + 1) % len(self.result)

    def extract_present(self, grid, n):
        points = []
        for row in range(n):
            for col in range(n):
                if grid[row][col] is True:
                    points.append((row, col))
        return points
