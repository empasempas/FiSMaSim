from automaton.deterministicFiniteAutomaton.deterministicFiniteAutomaton import DeterministicFiniteAutomaton
from automatonModelView.abstracts.abstractProjectWidget import AbstractProjectWidget
from automatonModelView.commonWidgets.automatonRunner import AutomatonRunner
from automatonModelView.commonWidgets.automatonStateManager import AutomatonStateManager
from automatonModelView.commonWidgets.sequenceInputWidget import SequenceInputWidget
from automatonModelView.commonWidgets.stateManager import StateManager
from automatonModelView.commonWidgets.symbolManager import SymbolManager
from automatonModelView.deterministicFiniteAutomaton.dfaGraphController import DFAGraphController
from automatonModelView.deterministicFiniteAutomaton.dfaGraphScene import DFAGraphScene


class DFAProjectWidget(AbstractProjectWidget):
    def __init__(self, parent, automaton=None):
        if automaton is None:
            automaton = DeterministicFiniteAutomaton(None)
        super(DFAProjectWidget, self).__init__(parent, automaton, DFAGraphController, DFAGraphScene, AutomatonRunner,
                                               AutomatonStateManager, SequenceInputWidget, StateManager, SymbolManager)

    def connectStateAddition(self):
        # add state
        self.stateManager.signalStateAdded.connect(self.graphController.addState)
        self.graphController.signalStateAdded.connect(self.graph.addNode)
        self.graphController.signalStateAdded.connect(self.graphController.sendStateIds)

    def connectStateRemoval(self):
        # remove state
        self.stateManager.signalStateIdsRequest.connect(self.graphController.sendStateIds)
        self.graphController.signalStates.connect(self.stateManager.populateStateSelect)
        self.stateManager.signalStateRemoveRequest.connect(self.graphController.removeState)
        self.graphController.signalStateRemoved.connect(self.graph.deleteForStateId)
        self.stateManager.signalStateIdsRequest.emit()

    def connectStateEditing(self):
        # edit state
        self.graph.signalStateEditing.connect(self.graphController.initStateEditor)
        self.graphController.signalStateUpdated.connect(self.graph.updateNodeFromInfo)

    def connectSymbolAddition(self):
        # add symbol
        self.symbolManager.signalSymbolAddRequest.connect(self.graphController.addSymbol)
        self.graphController.signalSymbolAdded.connect(self.symbolManager.signalSymbolsRequest)
        self.symbolManager.signalSymbolsRequest.connect(self.graphController.sendAlphabet)
        self.graphController.signalAlphabet.connect(self.symbolManager.populateSymbolSelect)
        self.symbolManager.signalSymbolsRequest.emit()

    def connectSymbolRemoval(self):
        # remove symbol
        self.symbolManager.signalSymbolRemovalRequest.connect(self.graphController.removeSymbol)
        self.graphController.signalSymbolRemoved.connect(self.graph.deleteTransitionsForInput)
        self.graph.signalSymbolDataRemoved.connect(self.symbolManager.signalSymbolsRequest)

    def connectTransitionAddition(self):
        # add transition
        self.graph.signalTransitionAddition.connect(self.graphController.initTransitionEditor)
        self.graphController.signalTransitionAdded.connect(self.graph.addEdge)

    def connectAutomatonManagement(self):
        # sequence input, automaton runner, automaton state settings
        self.sequenceInput.signalSymbolsRequest.connect(self.graphController.sendAlphabet)
        self.graphController.signalAlphabet.connect(self.sequenceInput.populateSelectList)
        self.runner.signalRequestNextInput.connect(self.sequenceInput.sendNextSymbol)
        self.sequenceInput.signalNextSymbol.connect(self.runner.getNextInput)
        self.runner.signalRequestCurrentState.connect(self.graphController.sendCurrentStateId)
        self.automatonManager.signalSetStartingStateRequest.connect(self.graphController.setStartingState)
        self.graphController.signalStartingStateChanged.connect(self.graph.updateCurrentState)
        self.automatonManager.signalSetCurrentStateRequest.connect(self.graphController.setCurrentState)
        self.graphController.signalCurrentStateChanged.connect(self.graph.updateCurrentState)
        self.graphController.signalStates.connect(self.automatonManager.populateStateSelect)

    def connectRunner(self):
        # running
        self.runner.signalStepRequest.connect(self.graphController.stepForward)
        self.runner.signalReadReversal.connect(self.sequenceInput.revertSymbol)
        self.runner.signalStateReversal.connect(self.graphController.setCurrentState)
