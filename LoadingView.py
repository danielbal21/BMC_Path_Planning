import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from z3 import sat, unsat

from ResultView import ResultView
from Services.Solver import run_solver_on_thread, get_result


class LoadingWindow(QWidget):
    def __init__(self, n, M2, timeout_sec, max_k, parent):
        super(LoadingWindow, self).__init__()
        self.header_label = None
        self.progress_bar = None
        self.n = n
        self.M2 = M2
        self.timeout_sec = timeout_sec
        self.max_k = max_k
        self.k = (2 * n) - 1
        self.sec_counter = 0
        self.is_running = True
        self.current_thread = run_solver_on_thread(self.n, self.M2, self.timeout_sec, self.k)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        self.header_label = QLabel("Solver", self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.header_label)

        # Label to show updates
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        self.label.setText(f" elapsed (seconds): {self.sec_counter}, iteration {self.k}/{self.max_k}")
        centered_layout = QHBoxLayout()
        centered_layout.addStretch(1)
        centered_layout.addWidget(self.label)
        centered_layout.addStretch(1)

        # Progress bar for the loading animation
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setRange(0, 0)  # Set to indeterminate mode
        layout.addWidget(self.progress_bar)
        layout.addLayout(centered_layout)
        self.setLayout(layout)

        # Timer to update the label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)  # Update every 1000 milliseconds

    def update_label(self):

        if self.is_running and self.current_thread.is_alive():
            self.sec_counter += 1
            if self.timeout_sec <= self.sec_counter:
                print("Timeout in GUI")
                self.reset()

        if not self.current_thread.is_alive() and self.is_running:
            res = get_result()
            if res[0] == sat:
                self.reset()
                print("Solved in GUI")
                RView = ResultView(self.parent, self.n, res[1],self.M2)
                self.parent.window.setCentralWidget(RView)
            elif res[0] == unsat:
                if self.k < self.max_k:
                    self.k += 1
                    self.current_thread = run_solver_on_thread(self.n, self.M2, self.timeout_sec, self.k)
                else:
                    print("Not Solved in GUI")
                    self.reset()

        # Reset the progress bar for the loading animation
        if self.is_running:
            self.label.setText(f" elapsed (seconds): {self.sec_counter}, iteration {self.k}/{self.max_k}")
            self.progress_bar.setRange(0, 0)

    def reset(self):
        self.timer.stop()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.is_running = False
        self.sec_counter = 0
