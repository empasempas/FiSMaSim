from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QLabel, QGridLayout, QPushButton


class DFATransitionEditor(QDialog):
    signalEditedTransitionInfo = Signal(dict, dict)
    signalTransitionDeletion = Signal(object, object)

    def __init__(self, stateIds, symbols, initialInfo=None):
        super(DFATransitionEditor, self).__init__()
        self.setModal(True)
        self.initialInfo = initialInfo
        fromStateLabel = QLabel('from state: ')
        self.fromStateComboBox = QComboBox(self)

        toStateLabel = QLabel('to state: ')
        self.toStateComboBox = QComboBox(self)

        self.prepareDropdownLists(stateIds)

        inputLabel = QLabel('on symbol: ')
        self.inputComboBox = QComboBox(self)
        for symbol in symbols:
            self.inputComboBox.addItem(symbol, symbol)

        self.fromStateComboBox.setCurrentIndex(0)
        self.toStateComboBox.setCurrentIndex(0)
        self.inputComboBox.setCurrentIndex(0)

        self.deleteButton = QPushButton('Delete transition', self)
        self.deleteButton.clicked.connect(self.deleteTransition)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.sendCollectedInfo)
        buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(fromStateLabel, 0, 0)
        layout.addWidget(toStateLabel, 1, 0)
        layout.addWidget(inputLabel, 2, 0)
        layout.addWidget(self.fromStateComboBox, 0, 1)
        layout.addWidget(self.toStateComboBox, 1, 1)
        layout.addWidget(self.inputComboBox, 2, 1)
        layout.addWidget(self.deleteButton, 3, 0)
        layout.addWidget(buttonBox, 4, 0)
        self.setLayout(layout)

    def prepareDropdownLists(self, stateIds):
        for stateId in stateIds:
            self.toStateComboBox.addItem('q{}'.format(stateIds.index(stateId)), stateId)
            self.fromStateComboBox.addItem('q{}'.format(stateIds.index(stateId)), stateId)

    def collectInfo(self):
        return {'fromStateId': self.fromStateComboBox.currentData(), 'toStateId': self.toStateComboBox.currentData(),
                'input': self.inputComboBox.currentData()}

    def deleteTransition(self):
        info = self.collectInfo()
        self.signalTransitionDeletion.emit(info['fromStateId'], info['input'])

    @Slot()
    def sendCollectedInfo(self):
        info = self.collectInfo()
        self.signalEditedTransitionInfo.emit(info, self.initialInfo)
        self.accept()
