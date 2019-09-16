from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QHBoxLayout, QLayout


class AutomatonStateManager(QWidget):
    signalStateIdsRequest = Signal()
    signalSetStartingStateRequest = Signal(str)
    signalSetCurrentStateRequest = Signal(str)

    def __init__(self, parent):
        super(AutomatonStateManager, self).__init__(parent)

        self.startingStateButton = QPushButton('Set starting state: ', self)
        self.startingStateButton.clicked.connect(self.setStartingState)
        self.startingSelect = QComboBox(self)

        self.currentStateButton = QPushButton('Set current state: ', self)
        self.currentStateButton.clicked.connect(self.setCurrentState)
        self.currentSelect = QComboBox(self)
        self.signalStateIdsRequest.emit()

        layout = QHBoxLayout()
        layout.addWidget(self.startingStateButton)
        layout.addWidget(self.startingSelect)
        layout.addWidget(self.currentStateButton)
        layout.addWidget(self.currentSelect)
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.setLayout(layout)

    @Slot(list)
    def populateStateSelect(self, stateIds):
        self.startingSelect.clear()
        self.currentSelect.clear()
        for stateId in stateIds:
            self.startingSelect.addItem('q{}'.format(stateIds.index(stateId)), stateId)
            self.currentSelect.addItem('q{}'.format(stateIds.index(stateId)), stateId)
        self.startingSelect.setCurrentIndex(0)
        self.currentSelect.setCurrentIndex(0)

    @Slot()
    def setStartingState(self):
        stateId = self.startingSelect.currentData()
        self.signalSetStartingStateRequest.emit(stateId)

    @Slot()
    def setCurrentState(self):
        stateId = self.currentSelect.currentData()
        self.signalSetCurrentStateRequest.emit(stateId)

    @Slot()
    def disableEdit(self):
        self.startingSelect.setDisabled(True)
        self.startingStateButton.setDisabled(True)
        self.currentSelect.setDisabled(True)
        self.currentStateButton.setDisabled(True)

    @Slot()
    def enableEdit(self):
        self.startingSelect.setDisabled(False)
        self.startingStateButton.setDisabled(False)
        self.currentSelect.setDisabled(False)
        self.currentStateButton.setDisabled(False)
