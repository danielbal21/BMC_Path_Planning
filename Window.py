import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

from ChoiceView import ChoiceView


class Startup(QMainWindow):
    """
    Main window for the application.
    """
    def __init__(self):
        """
        Initialize the Startup window.
        """
        super().__init__()

        self.prev_view = None
        self.central_widget = None
        self.setWindowTitle("Z3 Path Solver")
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface.
        """
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(186, 228, 229))
        self.setPalette(p)
        choiceView = ChoiceView(self)
        self.setCentralWidget(choiceView)


# Startup
def main():
    """
    Main entry point of the application.
    """
    app = QApplication(sys.argv)
    window = Startup()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
