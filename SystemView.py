import networkx as nx
import scipy as sp
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage


class SystemView(QGraphicsView):
    def __init__(self, kripke):
        super().__init__()

        self.kripke = kripke
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.kripke_present()

    def kripke_present(self):

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
        # Zoom in/out using the mouse wheel
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

    def generate_2d_array_string(self, matrix):
        result = ""
        for row_index, row in enumerate(matrix):
            for col_index, value in enumerate(row):
                if value:
                    result += f"({row_index},{col_index})\n"
        return result

    def on_click(self, event):
        tol = 0.05
        if event.inaxes == self.ax:
            for node in self.pos:
                x, y = self.pos[node]
                if abs(x - event.xdata) < tol and abs(y - event.ydata) < tol:
                    self.show_message(node)
                    break

    def show_message(self, node_id):
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
