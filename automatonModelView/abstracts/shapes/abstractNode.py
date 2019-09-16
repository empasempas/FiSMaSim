import weakref
from abc import abstractmethod

from PySide2 import QtGui
from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QPen, QBrush, QColor
from PySide2.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem

from automatonModelView.abstracts.abstractGeneral import AbstractGeneralGraphicsItem_Meta, \
    AbstractGeneralGraphicsItemClass


class AbstractNode(AbstractGeneralGraphicsItemClass):
    __metaclass__ = AbstractGeneralGraphicsItem_Meta

    def __init__(self, graphWidget, state):
        super(AbstractNode, self).__init__()

        self.graph = weakref.ref(graphWidget)
        self.isAcceptable = state.isAcceptable
        self.isCurrent = state.isCurrent

        self.newPos = QPointF()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setZValue(-1)
        self.setAcceptHoverEvents(True)

        self._edges = []
        self.currentFill = self.fillQColor
        self.border = QGraphicsEllipseItem(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
        self.finalNodeBorder = QGraphicsEllipseItem(-self.radius + 4, -self.radius + 4, self.radius * 2 - 10,
                                                    self.radius * 2 - 10)
        self.finalNodeBorder.mapToParent(self.border.pos())
        if self.isAcceptable == False:
            pen = self.finalNodeBorder.pen()
            pen.setColor(QColor(25, 255, 5))
            self.finalNodeBorder.update()

        if self.isCurrent == True:
            self.resolveFillColor()

        self.labelBox = QGraphicsTextItem(self)
        self.labelBox.setPos(0, 0)
        self.labelBox.setDefaultTextColor(QColor(0, 0, 0))

    @property
    @abstractmethod
    def borderQColor(self):
        pass

    @property
    @abstractmethod
    def fillQColor(self):
        pass

    @property
    @abstractmethod
    def currentStateFillQColor(self):
        pass

    @property
    @abstractmethod
    def radius(self):
        pass

    @abstractmethod
    def setLabel(self, value):
        pass

    def toggleCurrentState(self):
        self.isCurrent = not self.isCurrent
        self.resolveFillColor()

    def resolveFillColor(self):
        brush = QBrush()
        if self.isCurrent == True:
            brush.setColor(self.currentStateFillQColor)
            brush.setStyle(Qt.SolidPattern)
            self.currentFill = self.currentStateFillQColor
        else:
            brush.setColor(self.fillQColor)
            brush.setStyle(Qt.SolidPattern)
            self.currentFill = self.fillQColor
        self.border.setBrush(brush)
        self.update()

    def toggleFinalNodeBorder(self):
        self.isAcceptable = not self.isAcceptable
        self.resolveFinalNodeBorder()

    def resolveFinalNodeBorder(self):
        pen = QPen()
        if self.isAcceptable == True:
            pen.setColor(self.borderQColor)
            pen.setWidth(2)
        else:
            pen.setColor(self.currentFill)
            pen.setWidth(1)
        self.finalNodeBorder.setPen(pen)
        self.update()

    def addEdge(self, edge):
        self._edges.append(weakref.ref(edge))
        edge.adjust()

    def getEdges(self):
        return self._edges

    def getEdgesForInput(self, input):
        edges = []
        for edge in self._edges:
            if edge.onInput == input:
                edges.append(edge)
        return edges

    def getEdgesFromSelf(self, input):
        edges = []
        for edge in self._edges:
            if edge.onInput == input and edge.fromNode is self:
                edges.append(edge)
        return edges

    def getEdgeToNode(self, toNode):
        toReturn = None
        for edge in self._edges:
            if edge.toNode() is toNode:
                toReturn = edge
        return toReturn

    def boundingRect(self):
        adjust = 2.0
        return QRectF(-self.radius - adjust, -self.radius - adjust, (self.radius + adjust) * 2,
                      (self.radius + adjust) * 2)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
        return path

    def paint(self, painter, option, widget):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(self.borderQColor)
        brush = QBrush()
        self.border.setPen(pen)
        self.border.setBrush(brush)
        self.resolveFillColor()
        self.resolveFinalNodeBorder()
        self.border.paint(painter, option, widget)
        self.finalNodeBorder.paint(painter, option, widget)
        self.labelBox.setTextWidth(20)
        self.labelBox.setDefaultTextColor(QColor(0, 0, 0))

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for edge in self._edges:
                edge().adjust()

        return QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.update()
