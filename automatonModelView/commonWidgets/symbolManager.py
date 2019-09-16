from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QHBoxLayout, QLineEdit, QLayout


class SymbolManager(QWidget):
    signalSymbolsRequest = Signal()
    signalSymbolAddRequest = Signal(object)
    signalSymbolRemovalRequest = Signal(object)

    def __init__(self, parent):
        super(SymbolManager, self).__init__(parent)
        self.addButton = QPushButton('Add symbol: ', self)
        self.addButton.clicked.connect(self.addSymbol)
        self.symbolInput = QLineEdit(self)
        self.symbolInput.setMaxLength(1)

        self.removeButton = QPushButton('Remove symbol: ', self)
        self.removeButton.clicked.connect(self.removeSymbol)
        self.symbolSelect = QComboBox(self)
        self.signalSymbolsRequest.emit()

        layout = QHBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.symbolInput)
        layout.addWidget(self.removeButton)
        layout.addWidget(self.symbolSelect)
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        layout.expandingDirections()
        self.setLayout(layout)

    @Slot(list)
    def populateSymbolSelect(self, symbols):
        self.symbolSelect.clear()
        for symbol in symbols:
            self.symbolSelect.addItem(symbol, symbol)
        self.symbolSelect.setCurrentIndex(0)

    def refreshSymbolSelect(self):
        self.signalSymbolsRequest.emit()

    @Slot()
    def addSymbol(self):
        symbol = self.symbolInput.text()
        self.symbolInput.clear()
        self.signalSymbolAddRequest.emit(symbol)

    @Slot()
    def removeSymbol(self):
        symbol = self.symbolSelect.currentData()
        self.signalSymbolRemovalRequest.emit(symbol)

    @Slot()
    def disableEdit(self):
        self.symbolSelect.setDisabled(True)
        self.symbolInput.setDisabled(True)
        self.addButton.setDisabled(True)
        self.removeButton.setDisabled(True)

    @Slot()
    def enableEdit(self):
        self.symbolSelect.setDisabled(False)
        self.symbolInput.setDisabled(False)
        self.addButton.setDisabled(False)
        self.removeButton.setDisabled(False)
