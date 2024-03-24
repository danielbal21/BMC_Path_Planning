import sys

from PyQt5.QtGui import QColor
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
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(186, 228, 229))
        self.setPalette(p)
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
