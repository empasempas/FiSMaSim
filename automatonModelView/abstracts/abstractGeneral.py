import abc

from PySide2.QtWidgets import QGraphicsItem, QGraphicsScene, QWidget, QGraphicsItemGroup

class AbstractGeneralQGraphicsItemGroup_Meta(type(QGraphicsItemGroup), type(abc.ABCMeta)):
    pass


class AbstractGeneralQGraphicsItemGroupClass(QGraphicsItemGroup):
    pass


class AbstractGeneralGraphicsItem_Meta(type(QGraphicsItem), type(abc.ABCMeta)):
    pass


class AbstractGeneralGraphicsItemClass(QGraphicsItem):
    pass


class AbstractGeneralGraphScene_Meta(type(QGraphicsScene), type(abc.ABCMeta)):
    pass


class AbstractGeneralGraphSceneClass(QGraphicsScene):
    pass

class AbstractGeneralWidget_Meta(type(QWidget), type(abc.ABCMeta)):
    pass

class AbstractGeneralWidgetClass(QWidget):
    pass