# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow

from automatonModelView.deterministicFiniteAutomaton.dfaProjectWidget import DFAProjectWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    project = DFAProjectWidget(None, None)
    window.layout().addWidget(project)
    window.setWindowState(Qt.WindowFullScreen)
    window.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
    window.show()
    sys.exit(app.exec_())
