from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QHBoxLayout, QLayout


class SequenceInputWidget(QWidget):
    signalSymbolsRequest = Signal()
    signalInputRead = Signal(object)
    signalNextSymbol = Signal(object)

    def __init__(self, parent):
        super(SequenceInputWidget, self).__init__(parent)
        self.display = QLabel(self)
        self.sequence = []

        self.symbolSelect = QComboBox(self)
        self.signalSymbolsRequest.emit()

        self.addButton = QPushButton('Append symbol: ', self)
        self.addButton.clicked.connect(self.appendSymbol)
        self.removeButton = QPushButton('Remove last symbol...', self)
        self.removeButton.clicked.connect(self.popSymbol)

        layout = QHBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.symbolSelect)
        layout.addWidget(self.removeButton)
        layout.addWidget(self.display)
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.setLayout(layout)

    @Slot(list)
    def populateSelectList(self, symbols):
        self.symbolSelect.clear()
        for symbol in symbols:
            self.symbolSelect.addItem(symbol, symbol)
        self.symbolSelect.setCurrentIndex(0)

    def setDisplayText(self):
        limiter = ', '
        if len(self.sequence) > 0:
            self.display.setText(limiter.join(self.sequence))

    @Slot()
    def appendSymbol(self):
        symbol = self.symbolSelect.currentData()
        self.sequence.append(symbol)
        self.setDisplayText()

    @Slot()
    def popSymbol(self):
        if len(self.sequence) > 0:
            self.sequence.pop()
            self.setDisplayText()

    @Slot()
    def readInput(self):
        if len(self.sequence) > 0:
            input = self.sequence.pop(0)
            self.setDisplayText()
            self.signalInputRead.emit(input)

    @Slot()
    def sendNextSymbol(self):
        self.signalNextSymbol.emit(self.sequence[0])

    @Slot(object)
    def revertSymbol(self, symbol):
        self.sequence.insert(0, symbol)

    @Slot()
    def disableEdit(self):
        self.symbolSelect.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)

    @Slot()
    def enableEdit(self):
        self.symbolSelect.setDisabled(False)
        self.addButton.setDisabled(False)
        self.removeButton.setDisabled(False)
