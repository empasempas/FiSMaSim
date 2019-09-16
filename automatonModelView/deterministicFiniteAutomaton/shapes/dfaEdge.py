import math

from PySide2 import QtCore
from PySide2.QtCore import QPointF, QLineF, QRectF, QSizeF
from PySide2.QtGui import QPen, QColor, QPainterPath
from PySide2.QtWidgets import QGraphicsItem

from automatonModelView.abstracts.shapes.abstractEdge import AbstractEdge


class DFAEdge(AbstractEdge):
    Type = QGraphicsItem.UserType + 3

    def __init__(self, fromNode, toNode, input):
        super(DFAEdge, self).__init__(fromNode, toNode, input)

    def type(self):
        return DFAEdge.Type

    def calculateBoundingRect(self, extra):
        return QtCore.QRectF(self.fromPoint,
                             QtCore.QSizeF(self.toPoint.x() - self.fromPoint.x(),
                                           self.toPoint.y() - self.fromPoint.y())).normalized().adjusted(-extra, -extra,
                                                                                                         extra, extra)

    def calculatePerpendicularPoint(self, startingPoint, distance, line):
        labelHelperLine = QLineF()
        labelHelperLine.setP1(startingPoint)
        labelHelperLine.setAngle(line.angle() + 90)
        labelHelperLine.setLength(distance)
        return labelHelperLine.p2()

    def setLabel(self, fromNodeIndex, toNodeIndex):
        text = '<div style="text-align:center">q<sub>{}</sub>, {} --> q<sub>{}</sub></div>'.format(fromNodeIndex,
                                                                                                   self.input(),
                                                                                                   toNodeIndex)
        self.labelBox.setHtml(text)
        self.labelBox.adjustSize()
        self.labelBox.update()

    def paint(self, painter, option, widget):
        pen = QPen()
        pen.setColor(QColor(154, 35, 27))
        pen.setWidth(1)
        painter.setPen(pen)

        if not self._fromNode() or not self._toNode():
            return

        line = QLineF(self.fromPoint, self.toPoint)
        if line.length() == 0.0:
            return

        # self.drawArc(painter, line)
        topLeftPoint = self.calculatePerpendicularPoint(self.fromPoint, 50, line)
        arcRect = QRectF(topLeftPoint, QSizeF(line.length(), 100))
        if self._fromNode is self._toNode:
            spanAngle = -360
        else:
            spanAngle = -180
        # painter.drawArc(arcRect, 0, spanAngle)

        colliding = self.collidingItems()
        if len(colliding) > 0:
            line.setP1(line.p1() + QPointF(10, 10))
            line.setP2(line.p2() + QPointF(10, 10))
            line.translate(10, 10)
        painter.drawLine(line)

        midpoint = QPointF(line.center().x(), line.center().y())
        labelCenterPoint = self.calculatePerpendicularPoint(midpoint, 75, line)
        self.labelBox.setPos(labelCenterPoint)

        angle = math.acos(line.dx() / line.length())
        self.drawArrowHead(painter, angle, line.p2())

    def drawArc(self, painter, line):
        topLeftPoint = self.calculatePerpendicularPoint(self.fromPoint, 50, line)
        arcRect = QRectF(topLeftPoint, QSizeF(line.length(), 100))
        if self._fromNode is self._toNode:
            spanAngle = -360
        else:
            spanAngle = -180

        path = QPainterPath()
        path.arcMoveTo(arcRect, spanAngle)
        path.arcTo(arcRect, -180, spanAngle)
        painter.drawPath(path)