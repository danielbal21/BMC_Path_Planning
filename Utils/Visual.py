import math

import PyQt5
from PyQt5.QtCore import QPoint, QPointF, QLineF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QPolygon, QPainterPath, QTransform
from PyQt5.QtWidgets import QWidget
from PyQt5.uic.properties import QtGui


class ArrowWidget(QWidget):
    def draw_arrow(self, painter, start_point, end_point):
        painter.setRenderHint(QPainter.Antialiasing)
        arrow_size = 12
        stroke = 1.3  # arrow_size / 4
        # Draw line
        line_pen = QPen(QColor('black'), stroke, PyQt5.QtCore.Qt.SolidLine)
        painter.setPen(line_pen)
        painter.drawLine(start_point, end_point)

        # Draw arrowhead
        arrowhead_pen = QPen(QColor('black'), stroke, PyQt5.QtCore.Qt.SolidLine)
        painter.setPen(arrowhead_pen)

        angle = self.calculate_angle(start_point, end_point)
        arrowhead_polygon = self.create_arrowhead_polygon(end_point, arrow_size, angle)
        painter.drawPolygon(arrowhead_polygon)

    def calculate_angle(self, start_point, end_point):
        # Calculate the angle of the line
        return math.atan2(end_point.y() - start_point.y(), end_point.x() - start_point.x())

    def create_arrowhead_polygon(self, end_point, size, angle):
        # Create a polygon for arrowhead
        arrowhead_polygon = QPolygonF([
            end_point,
            QPointF(end_point.x() - size * math.cos(angle + math.pi / 6),
                    end_point.y() - size * math.sin(angle + math.pi / 6)),
            QPointF(end_point.x() - size * math.cos(angle - math.pi / 6),
                    end_point.y() - size * math.sin(angle - math.pi / 6))
        ])
        return arrowhead_polygon

    def draw_circle_in_center(self, painter, x, y, radius):
        # Calculate the top-left corner of the bounding rectangle for the ellipse
        top_left_x = x - radius
        top_left_y = y - radius

        # Draw the circle in the center
        painter.setBrush(QColor(255, 0, 0))  # Example color (red)
        painter.drawEllipse(top_left_x, top_left_y, 2 * radius, 2 * radius)
