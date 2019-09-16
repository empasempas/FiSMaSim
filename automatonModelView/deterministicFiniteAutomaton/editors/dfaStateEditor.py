from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QDialog, QGridLayout, QCheckBox, QPushButton


class DFAStateEditor(QDialog):
    signalEditedStateInfo = Signal(dict, dict)

    def __init__(self, state=None):
        super(DFAStateEditor, self).__init__()
        self.setModal(True)
        self.initialInfo = {'stateId': state.id, 'isAcceptable': state.isAcceptable}
        self.isAcceptableCheckBox = QCheckBox('State is acceptable ', self)
        self.accepted = QPushButton('OK', self)
        self.rejected = QPushButton('Cancel', self)

        if state is not None:
            self.setCheckBox(self.isAcceptableCheckBox, state.isAcceptable)
        else:
            self.isAcceptableCheckBox.setCheckState(QCheckBox.Unchecked)

        self.accepted.clicked.connect(self.sendCollectedInfo)
        self.rejected.clicked.connect(self.reject)

        self.setMaximumHeight(200)
        self.setMaximumWidth(200)

        layout = QGridLayout()
        # layout.setParent(self)
        layout.addWidget(self.isAcceptableCheckBox, 0, 0)
        layout.addWidget(self.accepted, 1, 0)
        layout.addWidget(self.rejected, 1, 1)
        self.setLayout(layout)

    def setCheckBox(self, checkbox, value):
        if value is True:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)

    @Slot()
    def sendCollectedInfo(self):
        info = {'stateId': self.initialInfo['stateId'], 'isAcceptable': self.isAcceptableCheckBox.isChecked()}
        self.signalEditedStateInfo.emit(info, self.initialInfo)
        self.accept()
