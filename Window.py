import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

from ChoiceView import ChoiceView


class Startup(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prev_view = None
        self.central_widget = None
        self.setWindowTitle("Z3 Path Solver")
        self.setFixedWidth(500)  # Set a fixed width for the main window
        self.initUI()

    def initUI(self):
        choiceView = ChoiceView(self)
        self.setCentralWidget(choiceView)

# Startup
def main():
    app = QApplication(sys.argv)
    window = Startup()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()