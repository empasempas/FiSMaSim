import math
import weakref
from abc import abstractmethod

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsTextItem

from automatonModelView.abstracts.abstractGeneral import AbstractGeneralGraphicsItem_Meta, \
    AbstractGeneralGraphicsItemClass


class AbstractEdge(AbstractGeneralGraphicsItemClass):
    __metaclass__ = AbstractGeneralGraphicsItem_Meta
    Pi = math.pi
    TwoPi = 2.0 * Pi

    def __init__(self, fromNode, toNode, input):
        super(AbstractEdge, self).__init__()
        self.arrowSize = 10.0
        self.fromPoint = QPointF()
        self.toPoint = QtCore.QPointF()
        self._fromNode = weakref.ref(fromNode)
        self._toNode = weakref.ref(toNode)
        self._fromNode().addEdge(self)
        self._toNode().addEdge(self)
        self._input = input

        self.labelBox = QGraphicsTextItem(self)
        self.labelBox.setDefaultTextColor(QColor(0, 0, 0))

        self.adjust()

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def calculateBoundingRect(self, extra):
        pass

    @abstractmethod
    def paint(self, painter, option, widget):
        pass

    def input(self):
        return self._input

    def setInput(self, input):
        self._input = input

    def fromNode(self):
        return self._fromNode()

    def setFromNode(self, node):
        self._fromNode = weakref.ref(node)
        self.adjust()

    def toNode(self):
        return self._toNode()

    def setToNode(self, node):
        self._toNode = weakref.ref(node)
        self.adjust()

    def boundingRect(self):
        if not self._fromNode() or not self._toNode():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0
        return self.calculateBoundingRect(extra)

    def adjust(self):
        if not self._fromNode() or not self._toNode():
            return

        line = QtCore.QLineF(self.mapFromItem(self._fromNode(), 0, 0), self.mapFromItem(self._toNode(), 0, 0))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 20) / length, (line.dy() * 20) / length)

        self.prepareGeometryChange()
        self.fromPoint = line.p1() + edgeOffset
        self.toPoint = line.p2() - edgeOffset
        self.update()

    def drawArrowHead(self, painter, angle, point):
        x1 = math.sin(angle - AbstractEdge.Pi / 3) * self.arrowSize
        y1 = math.cos(angle - AbstractEdge.Pi / 3) * self.arrowSize
        p1 = QtCore.QPointF(x1, y1)

        p2 = QtCore.QPointF(math.sin(angle - AbstractEdge.Pi + AbstractEdge.Pi / 3) * self.arrowSize,
                            math.cos(angle - AbstractEdge.Pi + AbstractEdge.Pi / 3) * self.arrowSize)

        toArrowP1 = self.toPoint + p1
        toArrowP2 = self.toPoint + p2

        painter.setBrush(QColor(255, 255, 255))
        painter.drawPolygon(QtGui.QPolygonF([point, toArrowP1, toArrowP2]))

    def setLabel(self, *args):
        pass
