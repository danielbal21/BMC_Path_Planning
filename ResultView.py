import sys

from PyQt5 import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout
from PyQt5.QtGui import QColor

from Utils.Visual import GridDrawerWidget


class ResultView(QWidget):
    def __init__(self,parent, N, result):
        super().__init__()
        self.parent = parent
        self.grid_widget = None
        self.N = N
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_movement)
        self.t = 0
        self.result = result
        self.timer.start(1000)
        #self.parent.window.setGeometry(100,100,900,900)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        header_layout = QHBoxLayout(self)
        sub_layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Label
        header_label = QLabel("Result Summary", self)
        header_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)  # Centered at the top
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 0px;")
        header_layout.addWidget(header_label)

        # Grid
        self.grid_widget = GridDrawerWidget(self.N, 640, 480)
        sub_layout.addWidget(self.grid_widget)
        layout.addLayout(header_layout)
        layout.addLayout(sub_layout)

        self.setLayout(layout)

    def update_movement(self):
        row = self.result[self.t][0]
        column = self.result[self.t][1]
        self.grid_widget.mark_rectangle(row,column)
        self.grid_widget.update()
        self.t = (self.t + 1) % len(self.result)