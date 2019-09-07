import abc

from PySide2.QtCore import QObject


class AbstractGeneral_Meta(type(QObject), type(abc.ABCMeta)):
    pass


class AbstractGeneralClass(QObject):
    pass
