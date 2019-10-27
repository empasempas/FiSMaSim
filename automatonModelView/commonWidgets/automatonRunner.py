from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout, QCheckBox, QLayout


class AutomatonRunner(QWidget):
    signalValidationRequest = Signal()
    signalStepRequest = Signal()
    signalReadReversal = Signal(object)
    signalStateReversal = Signal(object)
    signalRequestNextInput = Signal()
    signalRequestCurrentState = Signal()

    def __init__(self, parent):
        super(AutomatonRunner, self).__init__(parent)
        self.history = []
        self.currentState = None
        self.nextInput = None

        self.isRunning = QCheckBox('Run automaton', self)
        self.isRunning.clicked.connect(self.switchMode)

        self.stepForth = QPushButton('Step forward', self)
        self.stepForth.setDisabled(True)

        self.stepBack = QPushButton('Step back', self)
        self.stepBack.setDisabled(True)

        layout = QHBoxLayout()
        layout.addWidget(self.isRunning)
        layout.addWidget(self.stepForth)
        layout.addWidget(self.stepBack)
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.setLayout(layout)

    @Slot()
    def switchMode(self):
        if self.isRunning.isChecked() == True:
            self.signalValidationRequest.emit()
            self.signalRequestNextInput.emit()
            self.signalRequestCurrentState.emit()
            self.stepForth.setDisabled(False)
            self.stepBack.setDisabled(False)
        else:
            self.toggleMode()

    @Slot(object)
    def getNextInput(self, input):
        self.nextInput = input

    @Slot(object)
    def getCurrentState(self, state):
        self.currentState = state

    @Slot()
    def startRunning(self):
        self.stepForth.setDisabled(False)
        self.stepBack.setDisabled(False)
        self.history.append({'state': self.currentState, 'input': self.nextInput})

    @Slot()
    def stepForward(self):
        self.signalStepRequest.emit()
        self.signalRequestNextInput.emit()
        self.signalRequestCurrentState.emit()

    @Slot()
    def stepBack(self):
        if len(self.history) > 0:
            previousSituation = self.history.pop()
            self.signalReadReversal.emit(previousSituation['input'])
            self.signalStateReversal.emit(previousSituation['state'])

    def toggleMode(self):
        if self.isRunning.isChecked() == True:
            self.stepForth.setDisabled(False)
            self.stepBack.setDisabled(False)
        else:
            self.stepForth.setDisabled(True)
            self.stepBack.setDisabled(True)
