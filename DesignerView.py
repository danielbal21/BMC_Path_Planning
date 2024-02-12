import sys
from Models.System import System
from Models.Robot import Robot
from Models.Robot import Movement

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QScrollBar, QScrollArea, QCheckBox, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF

from Services.KripkeGenerator import KripkeGenerator


class DesignerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.size = None
        self.grid_widget = None
        self.step_up_checkbox = None
        self.grid_size_input = None
        self.designed_system = System()
        self.current_robot = Robot()
        self.design_grid = {}
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
        self.step_up_checkbox.stateChanged.connect(self.movement_changed)
        self.step_down_checkbox = QCheckBox("Step Down", self)
        self.step_down_checkbox.stateChanged.connect(self.movement_changed)
        self.step_left_checkbox = QCheckBox("Step Left", self)
        self.step_left_checkbox.stateChanged.connect(self.movement_changed)
        self.step_right_checkbox = QCheckBox("Step Right", self)
        self.step_right_checkbox.stateChanged.connect(self.movement_changed)
        self.step_stay_checkbox = QCheckBox("Stay", self)
        self.step_stay_checkbox.stateChanged.connect(self.movement_changed)

        checkbox_layout.addWidget(self.step_up_checkbox)
        checkbox_layout.addWidget(self.step_down_checkbox)
        checkbox_layout.addWidget(self.step_left_checkbox)
        checkbox_layout.addWidget(self.step_right_checkbox)
        checkbox_layout.addWidget(self.step_stay_checkbox)

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

        # Create a horizontal widget for robots
        robot_control_widget = QWidget(self)
        robots_layout = QHBoxLayout(robot_control_widget)

        # Set SetRobot button
        self.set_robot_button = QPushButton("Add Robot", self)
        self.set_robot_button.setEnabled(True)  # Initially disabled
        self.set_robot_button.clicked.connect(self.set_robot)
        robots_layout.addWidget(self.set_robot_button)

        # Set SetRobot button
        self.finish_button = QPushButton("Finish", self)
        self.finish_button.setEnabled(True)  # Initially disabled
        self.finish_button.clicked.connect(self.finish_design)
        robots_layout.addWidget(self.finish_button)

        # Wrap the horizontal widget in a centered layout (2)
        centered_layout_2 = QHBoxLayout()
        centered_layout_2.addStretch(1)
        centered_layout_2.addWidget(robot_control_widget)
        centered_layout_2.addStretch(1)

        layout.addLayout(centered_layout_2)  # Add the centered_2 layout to the vertical layout
        self.grid_widget.onCellClicked = self.selected_cell_changed

    def updateControlsEnabled(self):
        # Enable the "Set Initial" button only if a cell is selected
        selected = self.selected_cell is not None
        self.set_initial_button.setEnabled(selected)
        self.step_up_checkbox.setEnabled(selected)
        self.step_down_checkbox.setEnabled(selected)
        self.step_left_checkbox.setEnabled(selected)
        self.step_right_checkbox.setEnabled(selected)
        self.step_stay_checkbox.setEnabled(selected)

    def setInitial(self):
        # Handle the logic for setting the initial state based on checkboxes here
        # You can access the checkbox states using self.step_up_checkbox.isChecked(), etc.
        self.initial_cell = self.selected_cell
        if self.initial_cell is not None:
            self.current_robot.initial_pos = (self.initial_cell[1],self.initial_cell[0])
        else:
            self.current_robot.initial_pos = None
        self.updateGridColor()

    def updateGridSize(self):
        try:
            new_size = int(self.grid_size_input.text())
            if new_size >= 2:
                if new_size == self.grid_size:
                    return

                res = QMessageBox.question(self, 'Warning', 'Changing size will reset the designer, are you sure?',
                                           QMessageBox.Yes | QMessageBox.No)
                if res == QMessageBox.Yes:
                    self.grid_size = new_size
                    self.current_robot.clear()
                    self.designed_system.clear()
                    self.selected_cell = None
                    self.selected_cell_changed()
                    self.initial_cell = None
                    self.grid_widget.updateGridSize(new_size, self.zoom_factor)
                else:
                    self.grid_size_input.setText(self.grid_size.__str__())
            else:
                raise ValueError
        except ValueError:
            self.grid_size_input.setText(self.grid_size.__str__())
            QMessageBox.warning(self, 'Invalid Value', 'The value you entered is invalid', QMessageBox.Ok)

    def updateGridColor(self):
        try:
            self.grid_widget.updateGridSize(self.grid_size, self.zoom_factor, colorOnly=True)
        except ValueError:
            pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), Qt.white)

    def resizeEvent(self, event):
        self.grid_widget.updateGridSize(self.grid_size, first=True)

    def movement_changed(self):
        self.current_robot.add_movement(self.selected_cell[1],
                                        self.selected_cell[0],
                                        self.step_right_checkbox.isChecked(),
                                        self.step_left_checkbox.isChecked(),
                                        self.step_up_checkbox.isChecked(),
                                        self.step_down_checkbox.isChecked(),
                                        self.step_stay_checkbox.isChecked(),
                                        self.initial_cell == self.selected_cell)
        print(f"slot added to {self.selected_cell[1]},{self.selected_cell[0]} with:"
              f" \nR:{self.step_right_checkbox.isChecked()}"
              f"\nL:{self.step_left_checkbox.isChecked()}"
              f"\nU:{self.step_up_checkbox.isChecked()}"
              f"\nD:{self.step_down_checkbox.isChecked()}"
              f"\nS:{self.step_stay_checkbox.isChecked()}"
              f"\nI:{self.initial_cell == self.selected_cell}")

    def finish_design(self):
        kg = KripkeGenerator()
        generate_from_system(self.designed_system, self.grid_size)

    def set_robot(self):
        if not self.current_robot.is_valid():
            QMessageBox.critical(self,'Invalid Robot','This robot has invalid movements', QMessageBox.Ok)
        else:
            self.designed_system.add_robot(self.current_robot)

            print(f'Robot added:'
                  f'\n #Movements: {len(self.current_robot.movement_map)}'
                  f'\n Initial Pos: {self.current_robot.initial_pos}')

            self.current_robot = Robot()
            self.selected_cell = None
            self.initial_cell = self.selected_cell
            self.updateGridColor()


    def selected_cell_changed(self):
        if self.selected_cell is None:
            return
        movement = self.current_robot.movement_get(self.selected_cell[1], self.selected_cell[0])
        if movement is None:
            self.step_right_checkbox.setChecked(False)
            self.step_left_checkbox.setChecked(False)
            self.step_up_checkbox.setChecked(False)
            self.step_down_checkbox.setChecked(False)
            self.step_stay_checkbox.setChecked(False)
        else:
            self.step_right_checkbox.setChecked(movement.right)
            self.step_left_checkbox.setChecked(movement.left)
            self.step_up_checkbox.setChecked(movement.up)
            self.step_down_checkbox.setChecked(movement.down)
            self.step_stay_checkbox.setChecked(movement.stay)


class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.onCellClicked = None
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
                elif self.parent.current_robot.movement_get(y, x) is not None:
                    painter.fillRect(cell_rect, QBrush(QColor(60, 90, 160)))
                else:
                    painter.drawRect(cell_rect)

    def mousePressEvent(self, event):
        # Get the mouse click coordinates
        if event.button() == Qt.LeftButton:
            click_x = (event.x() - self.parent.center_x)
            click_y = (event.y() - self.parent.center_y)
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

            if self.onCellClicked is not None:
                self.onCellClicked()

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
        # self.parent.center_x = mouse_x
        # self.parent.center_y = mouse_y
