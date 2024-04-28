import matplotlib.pyplot as plt
import networkx as nx
from PyQt5 import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, \
    QPushButton, QHBoxLayout, QFileDialog, QWidget, QLineEdit, QMessageBox

from LoadingView import LoadingWindow
from Services.FileManager import system_to_file


class SystemView(QWidget):
    """
    Widget for configuring and visualizing a system.
    """
    def __init__(self, kripke, parent):
        """
        Initialize the SystemView widget.

        Args:
            kripke: The Kripke structure representing the system.
            parent: The parent widget.
        """
        super().__init__()

        self.max_path_txt = None
        self.timeout_txt = None
        self.text_artist = None
        self.pos = None
        self.ax = None
        self.fig = None
        self.parent = parent
        self.kripke = kripke
        self.parent.window.setGeometry(100,100,400,150)
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface elements.
        """
        layout = QVBoxLayout(self)
        iteration_timeout_line = QHBoxLayout(self)
        iteration_max_path_length = QHBoxLayout(self)

        # Header Label
        header_label = QLabel("Solver Configuration", self)
        header_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header_label)

        # Form
        timeout_label = QLabel("Timeout (sec): ")
        timeout_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 0px;")
        self.timeout_txt = QLineEdit(self)

        max_path_label = QLabel("Max path length: ")
        max_path_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 0px;")
        self.max_path_txt = QLineEdit(self)

        iteration_timeout_line.addWidget(timeout_label)
        iteration_timeout_line.addWidget(self.timeout_txt)

        iteration_max_path_length.addWidget(max_path_label)
        iteration_max_path_length.addWidget(self.max_path_txt)

        sub_layout = QHBoxLayout(self)
        # View Button
        view_system_btn = QPushButton("View M2", self)
        view_system_btn.setStyleSheet("""
            background-color: #2ecc71;
            border: none;
            color: white;
            padding: 10px;
            font-size: 16px;
        """)
        view_system_btn.clicked.connect(self.kripke_present)
        sub_layout.addWidget(view_system_btn)

        # Save Button
        save_system_btn = QPushButton("Save System", self)
        save_system_btn.setStyleSheet("""
            background-color: #2ecc71;
            border: none;
            color: white;
            padding: 10px;
            font-size: 16px;
        """)
        save_system_btn.clicked.connect(self.save_file_dialog)
        sub_layout.addWidget(save_system_btn)

        # Solve Button
        solve_system_btn = QPushButton("Solve", self)
        solve_system_btn.setStyleSheet("""
            background-color: #2ecc71;
            border: none;
            color: white;
            padding: 10px;
            font-size: 16px;
        """)
        solve_system_btn.clicked.connect(self.solve)
        sub_layout.addWidget(solve_system_btn)
        sub_layout.setAlignment(Qt.Qt.AlignBottom)

        layout.addLayout(iteration_timeout_line)
        layout.addLayout(iteration_max_path_length)
        layout.addLayout(sub_layout)

    def solve(self):
        """
        Handle the Solve button click event.
        """
        timeout = self.timeout_txt.text()
        max_k = self.max_path_txt.text()
        if not timeout or not max_k:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields.")
            return
        try:
            timeout_sec = int(timeout)
            max_k_iterations = int(max_k)
            if timeout_sec < 1 or max_k_iterations < 1 or max_k_iterations < ((2 * self.kripke.n) - 1):
                raise ValueError()
        except:
            QMessageBox.warning(self, "Invalid Input", "timeout and max iterations max be a positive integer\nmax "
                                                       "iterations must be at least " + str(self.kripke.n * 2 - 1))
            return

        LView = LoadingWindow(self.kripke.n, self.kripke, timeout_sec, max_k_iterations, self.parent)
        self.parent.window.setCentralWidget(LView)

    def save_file_dialog(self):
        """
        Display the file dialog for saving the system.
        """
        # Display the file dialog for saving
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Sys files (*.sys)")
        file_dialog.setDefaultSuffix("sys")

        if file_dialog.exec_() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            system_to_file(file_path, self.kripke)

    def kripke_present(self):
        """
        Display the Kripke structure visualization.
        """
        plt.close()
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle('Kripke Viewer')
        self.ax.set_title('Click a Node to view the safety matrix')
        G = nx.DiGraph()
        for node in self.kripke.nodes:
            G.add_node(node.node_id, properties_str=self.generate_2d_array_string(node.properties))
            for t in self.kripke.relations:
                for e in self.kripke.relations[t]:
                    G.add_edge(t, e)

        # Draw the graph using Matplotlib
        self.pos = nx.kamada_kawai_layout(G, scale=2)
        nx.draw(G, self.pos, with_labels=True, node_size=600, node_color='lightblue', font_color='black', font_size=8)

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.setWindowTitle('Kripke Viewer')
        plt.show()

    def wheelEvent(self, event):
        """
        Handle zooming using the mouse wheel.
        """
        # Zoom in/out using the mouse wheel
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

    def generate_2d_array_string(self, matrix):
        """
        Generate a string representation of a 2D matrix.

        Args:
            matrix: The input matrix.

        Returns:
            str: A string representation of the matrix.
        """
        result = ""
        for row_index, row in enumerate(matrix):
            for col_index, value in enumerate(row):
                if value:
                    result += f"({row_index},{col_index})\n"
        return result

    def on_click(self, event):
        """
        Handle the click event on the visualization.

        Args:
            event: The event object.
        """
        tol = 0.1
        if event.inaxes == self.ax:
            for node in self.pos:
                x, y = self.pos[node]
                if abs(x - event.xdata) < tol and abs(y - event.ydata) < tol:
                    self.show_message(node)
                    break

    def show_message(self, node_id):
        """
        Display additional information on node click.

        Args:
            node_id: The ID of the clicked node.
        """
        matrix_string = f"Safety Matrix for {node_id}:\n"
        matrix_string += self.generate_2d_array_string(self.kripke.nodes[node_id].properties)

        # Remove the previous text artist if it exists
        if hasattr(self, 'text_artist') and self.text_artist:
            self.text_artist.remove()

        # Display the additional information in the upper right corner
        self.text_artist = self.ax.text(self.pos[node_id][0], self.pos[node_id][1], matrix_string,
                                        fontsize=10,
                                        verticalalignment='top', horizontalalignment='right',
                                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Refresh the display
        self.fig.canvas.draw_idle()
