from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QHBoxLayout, QLayout


class StateManager(QWidget):
    signalStateIdsRequest = Signal()
    signalStateAdded = Signal()
    signalStateRemoveRequest = Signal(object)

    def __init__(self, parent):
        super(StateManager, self).__init__(parent)
        self.addButton = QPushButton('Add state...', self)
        self.addButton.clicked.connect(self.addState)

        self.removeButton = QPushButton('Remove state: ', self)
        self.removeButton.clicked.connect(self.removeState)
        self.stateSelect = QComboBox(self)

        layout = QHBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.removeButton)
        layout.addWidget(self.stateSelect)
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.setLayout(layout)

    @Slot(list)
    def populateStateSelect(self, stateIds):
        self.stateSelect.clear()
        for stateId in stateIds:
            self.stateSelect.addItem('q{}'.format(stateIds.index(stateId)), stateId)
        self.stateSelect.setCurrentIndex(0)

    @Slot()
    def addState(self):
        self.signalStateAdded.emit()

    @Slot()
    def removeState(self):
        stateId = self.stateSelect.currentData()
        self.signalStateRemoveRequest.emit(stateId)

    @Slot()
    def disableEdit(self):
        self.stateSelect.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)

    @Slot()
    def enableEdit(self):
        self.stateSelect.setDisabled(False)
        self.addButton.setDisabled(False)
        self.removeButton.setDisabled(False)
