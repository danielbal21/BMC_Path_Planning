import sys

from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, \
    QLineEdit, QCheckBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QCoreApplication


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

        # Counteragent Max Steps Input
        max_steps_label = QLabel("Counteragent Max Steps (>= 0):", self)
        self.max_steps_input = QLineEdit(self)
        self.addFormRow(layout, max_steps_label, self.max_steps_input)

        # Grid Size Input
        grid_size_label = QLabel("Grid Size (>= 2):", self)
        self.grid_size_input = QLineEdit(self)
        self.addFormRow(layout, grid_size_label, self.grid_size_input)

        # Allow Circles Checkbox
        self.allow_circles_checkbox = QCheckBox("Allow Circles", self)
        layout.addWidget(self.allow_circles_checkbox)

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
        max_steps = self.max_steps_input.text()
        grid_size = self.grid_size_input.text()

        if not system_name or not num_counteragents or not max_steps or not grid_size:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields.")
            return

        try:
            num_counteragents = int(num_counteragents)
            max_steps = int(max_steps)
            grid_size = int(grid_size)

            if num_counteragents < 0 or max_steps < 0 or grid_size < 2:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values.")
            return

        # Perform system generation here, using the input values
        # You can add your system generation logic here
        # ...

        # Show a message box indicating successful generation (you can replace this with your actual logic)
        QMessageBox.information(self, "System Generated", "System has been generated successfully.")
