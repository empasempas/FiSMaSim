import abc

from PySide2.QtCore import QAbstractListModel


class AbstractGeneralListModel_Meta(type(QAbstractListModel), type(abc.ABCMeta)):
    pass


class AbstractGeneralListModelClass(QAbstractListModel):
    pass
