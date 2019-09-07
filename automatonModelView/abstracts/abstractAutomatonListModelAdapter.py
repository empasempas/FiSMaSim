import abc

from PySide2.QtCore import Qt, QModelIndex

from automatonModelView.abstracts.abstractGeneral import AbstractGeneralListModelClass, AbstractGeneralListModel_Meta
from automatonModelView.abstracts.abstractStateListItemAdapter import AbstractStateListItemAdapter


class AbstractAutomatonListModel(AbstractGeneralListModelClass):
    __metaclass__ = AbstractGeneralListModel_Meta

    def __init__(self, automatonInstance):
        super(AbstractGeneralListModelClass, self).__init__()
        self.automaton = automatonInstance
        self.adapters = self.generateAdapters()

    @abc.abstractmethod
    def generateAdapters(self):
        states = self.automaton.getStates()
        return list(map(lambda state: self.adaptState(state), states))

    def adaptState(self, state):
        return AbstractStateListItemAdapter(state)

    @abc.abstractmethod
    def rowCount(self, parent=QModelIndex()):
        return len(self.automaton.getStates())

    def data(self, index, role=0):
        if 0 <= index.row() < self.rowCount() and index.isValid():
            adapter = self.adapters[index]
            stateId = adapter.stateId
            transitions = self.automaton.getTransitionsFromState(stateId)
            adapter.mapTransitionsToAdapters(transitions, self.adapters)
            return adapter

    def setData(self, index, value, role=1):
        if 0 <= index.row() < self.rowCount() and index.isValid():
            adapter = self.adapters[index]
            stateId = adapter.stateId
            adapter.applyValues(value)
            state = self.automaton.getStateById(stateId, 'fetching for editing')
            state.applyValues(value)
            return True
        else:
            return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

    def appendRow(self, **kwargs):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        newStateId = self.automaton.addState(**kwargs)
        newAdapter = self.adaptState(self.automaton.getStateById(newStateId))
        self.adapters.append(newAdapter)
        self.endInsertRows()
