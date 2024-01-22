import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QScrollBar, QScrollArea, QCheckBox, QPushButton
)
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF


class DesignerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.parent.window.setGeometry(100, 100, 640, 480)
        self.grid_size = 10  # Default grid size
        self.zoom_factor = 1.0  # Initial zoom factor 
        self.center_x = 0
        self.center_y = 0
        self.panning = False
        self.last_pos = None
        self.selected_cell = None
        self.initial_cell = None
        self.initUI()
        self.updateControlsEnabled()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Screen Header
        header_label = QLabel("System Designer", self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header_label)

        # Grid Size Input
        grid_size_label = QLabel("Grid Size (N x N):", self)
        self.grid_size_input = QLineEdit(str(self.grid_size), self)
        self.grid_size_input.setValidator(QtGui.QIntValidator(2, 100, self))
        self.grid_size_input.textChanged.connect(self.updateGridSize)
        grid_size_row = QWidget(self)
        size_hbox = QHBoxLayout(grid_size_row)
        size_hbox.addWidget(grid_size_label)
        size_hbox.addWidget(self.grid_size_input)
        layout.addWidget(grid_size_row)

        # Scroll Area for the Grid
        scroll_area = QScrollArea(self)
        self.grid_widget = GridWidget(self)
        scroll_area.setWidget(self.grid_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Create a horizontal widget for checkboxes
        checkbox_widget = QWidget(self)
        checkbox_layout = QHBoxLayout(checkbox_widget)

        # Checkboxes for movement directions
        self.step_up_checkbox = QCheckBox("Step Up", self)
        self.step_down_checkbox = QCheckBox("Step Down", self)
        self.step_left_checkbox = QCheckBox("Step Left", self)
        self.step_right_checkbox = QCheckBox("Step Right", self)

        checkbox_layout.addWidget(self.step_up_checkbox)
        checkbox_layout.addWidget(self.step_down_checkbox)
        checkbox_layout.addWidget(self.step_left_checkbox)
        checkbox_layout.addWidget(self.step_right_checkbox)

        # Set Initial button
        self.set_initial_button = QPushButton("Set Initial", self)
        self.set_initial_button.setEnabled(False)  # Initially disabled
        self.set_initial_button.clicked.connect(self.setInitial)
        checkbox_layout.addWidget(self.set_initial_button)

        checkbox_layout.addStretch(1)  # Add stretch to push checkboxes to the left

        # Wrap the horizontal widget in a centered layout
        centered_layout = QHBoxLayout()
        centered_layout.addStretch(1)
        centered_layout.addWidget(checkbox_widget)
        centered_layout.addStretch(1)

        layout.addLayout(centered_layout)  # Add the centered layout to the vertical layout

    def updateControlsEnabled(self):
        # Enable the "Set Initial" button only if a cell is selected
        selected = self.selected_cell is not None
        self.set_initial_button.setEnabled(selected)
        self.step_up_checkbox.setEnabled(selected)
        self.step_down_checkbox.setEnabled(selected)
        self.step_left_checkbox.setEnabled(selected)
        self.step_right_checkbox.setEnabled(selected)

    def setInitial(self):
        # Handle the logic for setting the initial state based on checkboxes here
        # You can access the checkbox states using self.step_up_checkbox.isChecked(), etc.
        self.initial_cell = self.selected_cell
        self.updateGridColor()

    def updateGridSize(self):
        try:
            new_size = int(self.grid_size_input.text())
            if new_size >= 2:
                self.grid_size = new_size
                self.grid_widget.updateGridSize(new_size, self.zoom_factor)
        except ValueError:
            pass

    def updateGridColor(self):
        try:
            self.grid_widget.updateGridSize(self.grid_size, self.zoom_factor,first=False,colorOnly=True)
        except ValueError:
            pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), Qt.white)

    def resizeEvent(self, event):
        self.grid_widget.updateGridSize(self.grid_size,first=True)


class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.grid_size = 10  # Default grid size
        self.zoom_factor = 1.0  # Initial zoom factor

        self.initUI()

    def initUI(self):
        self.setMinimumSize(300, 300)
        self.setMouseTracking(True)  # Enable mouse tracking to capture mouse wheel events

    def updateGridSize(self, new_size, first=False, colorOnly=False):
        if not colorOnly:
            self.grid_size = new_size
            self.adjustSize()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        cell_width = (self.width() * self.zoom_factor) / self.grid_size
        cell_height = (self.height() * self.zoom_factor) / self.grid_size

        # Calculate the center offset
        center_offset_x = (self.parent.center_x)
        center_offset_y = (self.parent.center_y)
        #center_offset_x = (self.parent.center_x) + ((self.width() - (self.width() * self.zoom_factor)) / 2)
        #center_offset_y = (self.parent.center_y) + ((self.height() - (self.height() * self.zoom_factor)) / 2)

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell_x = x * cell_width + center_offset_x
                cell_y = y * cell_height + center_offset_y
                cell_rect = QRectF(cell_x, cell_y, cell_width - 1, cell_height - 1)
                cell_rect.adjust(1, 1, -1, -1)  # Add some padding

                if (x, y) == self.parent.initial_cell:
                    painter.fillRect(cell_rect, QBrush(QColor(0, 215, 100)))
                elif (x, y) == self.parent.selected_cell:
                    painter.fillRect(cell_rect, QBrush(QColor(0, 120, 215)))
                else:
                    painter.drawRect(cell_rect)

    def mousePressEvent(self, event):
        # Get the mouse click coordinates
        if event.button() == Qt.LeftButton:
            click_x = (event.x() - self.parent.center_x)
            click_y = (event.y() - self.parent.center_y)
            print(self.zoom_factor)
            print(self.width() - (self.width() * self.zoom_factor))
            # Calculate the zoomed cell width and height
            cell_width = (self.width() * self.zoom_factor) / (self.grid_size)
            cell_height = (self.height() * self.zoom_factor) / (self.grid_size)

            # Calculate the cell coordinates based on the click coordinates
            cell_x = int(click_x / cell_width)
            cell_y = int(click_y / cell_height)

            # Toggle the selection status of the clicked cell
            if (cell_x, cell_y) == self.parent.selected_cell:
                self.parent.selected_cell = None
            else:
                self.parent.selected_cell = (cell_x, cell_y)
            self.update()
            self.parent.updateControlsEnabled()

        elif event.button() == Qt.RightButton:
            self.parent.panning = True
            self.parent.last_pos = event.pos()

        elif event.button() == Qt.MidButton:
            self.parent.center_x = (self.width() - (self.width() * self.zoom_factor)) / 2
            self.parent.center_y = (self.height() - (self.height() * self.zoom_factor)) / 2
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.parent.panning = False
            self.parent.last_pos = None

    def mouseMoveEvent(self, event):
        if self.parent.panning:
            delta = event.pos() - self.parent.last_pos
            self.parent.center_x += delta.x()
            self.parent.center_y += delta.y()
            self.parent.last_pos = event.pos()
            self.update()

    def wheelEvent(self, event):
        # Get the position of the mouse cursor
        mouse_x = event.x()
        mouse_y = event.y()

        # Calculate the zoom factor
        num_degrees = event.angleDelta().y() / 8
        num_steps = num_degrees / 15.0
        if num_steps > 0:
            self.zoom_factor += 0.1
        else:
            self.zoom_factor -= 0.1

        # Adjust the zoom factor within reasonable limits
        self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))

        # Update the grid with the new zoom factor and center it on the mouse cursor
        self.updateGridSize(self.grid_size)
        #self.parent.center_x = mouse_x
        #self.parent.center_y = mouse_y
