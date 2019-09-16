from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsItem

from automatonModelView.abstracts.shapes.abstractNode import AbstractNode


class DFANode(AbstractNode):
    Type = QGraphicsItem.UserType + 1

    @property
    def borderQColor(self):
        return QColor(0, 0, 0)

    @property
    def fillQColor(self):
        return QColor(255, 255, 255)

    @property
    def currentStateFillQColor(self):
        return QColor(150, 123, 182)

    @property
    def radius(self):
        return 30

    def __init__(self, graphWidget, stateInfo):
        super(DFANode, self).__init__(graphWidget, stateInfo)

    def setLabel(self, value):
        text = '<div style="text-align:center">q<sub>{}</sub></div>'.format(value)
        self.labelBox.setHtml(text)
        self.labelBox.adjustSize()
        self.labelBox.update()
