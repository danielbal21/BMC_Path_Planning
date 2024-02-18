import sys

from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, \
    QLineEdit, QCheckBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QCoreApplication

from Services.KripkeGenerator import auto_generate_system
from SystemView import SystemView


class GeneratorView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Header Label
        header_label = QLabel("System Generator", self)
        header_label.setAlignment(Qt.Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header_label)

        # System Name Input
        system_name_label = QLabel("System Name:", self)
        self.system_name_input = QLineEdit(self)
        self.addFormRow(layout, system_name_label, self.system_name_input)

        # Number of Counteragents Input
        num_counteragents_label = QLabel("Number of Counteragents (>= 0):", self)
        self.num_counteragents_input = QLineEdit(self)
        self.addFormRow(layout, num_counteragents_label, self.num_counteragents_input)

        # Counteragent Max Stray Radius Input
        max_steps_label = QLabel("Counteragent Stray Radius (>= 0):", self)
        self.max_steps_input = QLineEdit(self)
        self.addFormRow(layout, max_steps_label, self.max_steps_input)

        # Grid Size Input
        grid_size_label = QLabel("Grid Size (>= 2):", self)
        self.grid_size_input = QLineEdit(self)
        self.addFormRow(layout, grid_size_label, self.grid_size_input)

        # Grid Size Input
        stay_chance_label = QLabel("Stay Chance (0.0 ~ 1.0):", self)
        self.stay_chance = QLineEdit(self)
        self.addFormRow(layout, stay_chance_label, self.stay_chance)

        # Generate Button
        generate_button = QPushButton("Generate", self)
        generate_button.setStyleSheet("""
            background-color: #2ecc71;
            border: none;
            color: white;
            padding: 10px;
            font-size: 16px;
        """)
        generate_button.clicked.connect(self.generateSystem)
        layout.addWidget(generate_button)

    def addFormRow(self, layout, label, widget):
        row_widget = QWidget(self)
        row_layout = QHBoxLayout(row_widget)
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        layout.addWidget(row_widget)

    def generateSystem(self):
        system_name = self.system_name_input.text()
        num_counteragents = self.num_counteragents_input.text()
        stray_radius = self.max_steps_input.text()
        grid_size = self.grid_size_input.text()
        stay_chance = self.stay_chance.text()

        if not system_name or not num_counteragents or not stray_radius or not grid_size or not stay_chance:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields.")
            return

        try:
            num_counteragents = int(num_counteragents)
            stray_radius = int(stray_radius)
            grid_size = int(grid_size)
            stay_chance = float(stay_chance)
            if num_counteragents < 0 or stray_radius < 0 or grid_size < 2 or (0.0 > stay_chance) or (stay_chance > 1.0):
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values.")
            return

        M2 = auto_generate_system(grid_size, num_counteragents, stay_chance, stray_radius)
        QMessageBox.information(self, "System Generated", "System has been generated successfully.")

        systemViewer = SystemView(M2[1])
        self.parent.window.setCentralWidget(systemViewer)
