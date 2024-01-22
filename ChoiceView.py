import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import QCoreApplication

from GeneratorView import GeneratorView
from DesignerView import DesignerView

class ChoiceView(QWidget):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        button1 = self.createStyledButton("Import from file", "#3498db", self.importFromFile)
        button2 = self.createStyledButton("Generate System", "#e74c3c", self.generateSystem)
        button3 = self.createStyledButton("Design System", "#2ecc71", self.designSystem)
        button4 = self.createStyledButton("Exit", "#34495e", self.closeApp)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)


    def createStyledButton(self, text, color, action):
        button = QPushButton(text, self)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 10px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: darker({color}, 20%);
            }}
        """)
        button.clicked.connect(action)
        return button

    def importFromFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.ExistingFile
        options |= QFileDialog.HideNameFilterDetails

        file_path, _ = QFileDialog.getOpenFileName(self, "Select a .sys File", "", "System Files (*.sys)",
                                                   options=options)

        if file_path:
            print(f"Selected file: {file_path}")

    def generateSystem(self):
        generateView = GeneratorView(self)
        self.window.setCentralWidget(generateView)


    def designSystem(self):
        designerView = DesignerView(self)
        self.window.setCentralWidget(designerView)

    def closeApp(self):
        self.close()