from abc import abstractmethod

from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QVBoxLayout, QLayout, QMessageBox, QCheckBox

from automatonModelView.abstracts.abstractGeneral import AbstractGeneralWidget_Meta, AbstractGeneralWidgetClass


class AbstractProjectWidget(AbstractGeneralWidgetClass):
    __metaclass__ = AbstractGeneralWidget_Meta
    __instance = None

    @staticmethod
    def getInstance(parent, automaton, graphControllerClass, graphSceneClass, runnerWidgetClass,
                    automatonManagerWidgetClass, sequenceInputWidgetClass, stateManagerClass, symbolManagerClass):
        if AbstractProjectWidget.__instance == None:
            AbstractProjectWidget(parent, automaton, graphControllerClass, graphSceneClass, runnerWidgetClass,
                                  automatonManagerWidgetClass, sequenceInputWidgetClass, stateManagerClass,
                                  symbolManagerClass)
        return AbstractProjectWidget.__instance

    def __init__(self, parent, automaton, graphControllerClass, graphSceneClass, runnerWidgetClass,
                 automatonManagerWidgetClass, sequenceInputWidgetClass, stateManagerClass, symbolManagerClass):
        if AbstractProjectWidget.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(AbstractProjectWidget, self).__init__(parent)
            AbstractProjectWidget.__instance = self
            self.automaton = automaton
            self.graphControllerClass = graphControllerClass
            self.graphController = self.graphControllerClass(self.automaton)
            self.graphSceneClass = graphSceneClass
            self.runnerWidgetClass = runnerWidgetClass
            self.automatonManagerWidgetClass = automatonManagerWidgetClass
            self.sequenceInputWidgetClass = sequenceInputWidgetClass
            self.stateManagerClass = stateManagerClass
            self.symbolManagerClass = symbolManagerClass

            self.setupGraph()
            self.setupManagementWidgets()
            self.connectSignalsToSlots()
            self.setupLayout()
            self.graphController.populateGraph()

    def setupGraph(self):
        self.graph = self.graphSceneClass(self)


    def setupManagementWidgets(self):
        self.runner = self.runnerWidgetClass(self)
        self.automatonManager = self.automatonManagerWidgetClass(self)
        self.sequenceInput = self.sequenceInputWidgetClass(self)
        self.stateManager = self.stateManagerClass(self)
        self.symbolManager = self.symbolManagerClass(self)

    @abstractmethod
    def connectSignalsToSlots(self):
        pass

    def setupLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.runner)
        layout.addWidget(self.graph.view)
        layout.addWidget(self.sequenceInput)
        layout.addWidget(self.automatonManager)
        layout.addWidget(self.stateManager)
        layout.addWidget(self.symbolManager)
        self.setLayout(layout)
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.graph.view.show()

    @Slot(object)
    def error(self, error):
        self.runner.isRunning.setCheckState(QCheckBox.Unchecked)
        messageBox = QMessageBox()
        messageBox.critical(self, 'Critical Error', error)