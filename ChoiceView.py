from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog

from DesignerView import DesignerView
from GeneratorView import GeneratorView
from Services.FileManager import system_from_file
from SystemView import SystemView


class ChoiceView(QWidget):
    """
    The ChoiceView class represents the main interface for selecting different system operations.

    Attributes:
        window (QWidget): The parent window.
    """
    def __init__(self, window):
        """
        Initialize the ChoiceView.

        Args:
            window (QWidget): The parent window.
        """
        super().__init__(window)

        self.window = window
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface layout.
        """
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
        """
        Create a styled button with the given text, color, and action.

        Args:
            text (str): The text displayed on the button.
            color (str): The background color of the button in hexadecimal format.
            action (function): The action to be executed when the button is clicked.

        Returns:
            QPushButton: The styled button.
        """
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
        """
        Open a file dialog to import a system from a file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.ExistingFile
        options |= QFileDialog.HideNameFilterDetails

        file_path, _ = QFileDialog.getOpenFileName(self, "Select a .sys File", "", "System Files (*.sys)",
                                                   options=options)

        if file_path:
            # If a file is selected, load the system and display it
            print(f"Selected file: {file_path}")
            M2 = system_from_file(file_path)
            sysView = SystemView(M2, self)
            self.window.setCentralWidget(sysView)

    def generateSystem(self):
        """
        Switch to the system generator view.
        """
        generateView = GeneratorView(self)
        self.window.setCentralWidget(generateView)

    def designSystem(self):
        """
        Switch to the system designer view.
        """
        designerView = DesignerView(self)
        self.window.setCentralWidget(designerView)

    def closeApp(self):
        """
        Close the application.
        """
        self.close()
        QCoreApplication.exit(0)
