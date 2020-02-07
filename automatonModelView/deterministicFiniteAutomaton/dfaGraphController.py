from PySide2.QtCore import Signal, Slot

from aspect.logging import logFunction
from automaton.automataErrors import ActionOnNonexistentSymbolError, ActionOnNonexistentStateError
from automaton.deterministicFiniteAutomaton.deterministicFiniteAutomaton import DeterministicFiniteAutomaton
from automatonModelView.abstracts.abstractAutomatonGraphController import AbstractAutomatonGraphController
from automatonModelView.deterministicFiniteAutomaton.editors.dfaStateEditor import DFAStateEditor
from automatonModelView.deterministicFiniteAutomaton.editors.dfaTransitionEditor import DFATransitionEditor


class DFAGraphController(AbstractAutomatonGraphController):

    def __init__(self, dfa):
        super(DFAGraphController, self).__init__(dfa)

    def addTransitionsToGraph(self, states):
        transitions = []
        for state in states:
            stateTransitions = self.automaton.getTransitionsFromState(state.id)
            if len(stateTransitions) > 0:
                transitions.extend(stateTransitions)

        if len(transitions) > 0:
            for transition in transitions:
                transitionInfo = {'fromStateId': transition.toStateId(), 'toStateId': transition.fromStateId(),
                                  'input': transition.onInput}
                self.signalTransitionAdded.emit(transitionInfo)

    def transitionAdd(self, transitionInfo):
        try:
            self.automaton.addTransition(transitionInfo['fromStateId'], transitionInfo['input'],
                                         transitionInfo['toStateId'])
            self.signalTransitionAdded.emit(transitionInfo)
        except ActionOnNonexistentSymbolError:
            self.signalError.emit('Input symbol does not exist!')
        except ActionOnNonexistentStateError:
            self.signalError.emit('Cannot add transition to/from a state that does not exist!')

    @Slot(dict)
    def initTransitionEditor(self, transitionInfo):
        stateIds = [state.id for state in self.automaton.getStates()]
        symbols = self.automaton.getAlphabet()
        editor = DFATransitionEditor(stateIds, symbols, transitionInfo)
        editor.signalEditedTransitionInfo.connect(self.transitionEdit)
        editor.signalTransitionDeletion.connect(self.removeTransition)
        editor.exec()

    @Slot(dict, dict)
    def transitionEdit(self, transitionInfo, initialInfo=None):
        if transitionInfo != initialInfo:
            if initialInfo['input'] is not None:
                self.removeTransition(initialInfo['fromState'], initialInfo['input'])
            self.transitionAdd(transitionInfo)

    @Slot(object, object)
    def removeTransition(self, fromStateId, input):
        key = DeterministicFiniteAutomaton.createTransitionKey(input, fromStateId)
        self.automaton.removeTransition(key)
        self.signalTransitionRemoved.emit({'fromStateId': fromStateId, 'onInput': input})

    @Slot(object)
    def setStartingState(self, stateId):
        try:
            self.automaton.setStartingState(stateId)
            self.signalStartingStateChanged(stateId)
        except:
            self.emitError('Unable to set starting state!')

    @Slot(object)
    def setCurrentState(self, stateId):
        try:
            self.automaton.setState(stateId)
            self.signalCurrentStateChanged.emit(stateId)
        except:
            self.signalError.emit('Unable to set current state!')

    @logFunction
    @Slot(object)
    def initStateEditor(self, stateId):
        state = self.automaton.getStateById(stateId, 'user editing state')
        editor = DFAStateEditor(state)
        editor.signalEditedStateInfo.connect(self.stateEdit)
        editor.exec()

    @Slot(dict, dict)
    def stateEdit(self, stateInfo, initialInfo=None):
        if stateInfo != initialInfo and initialInfo is not None:
            if initialInfo['isAcceptable'] != stateInfo['isAcceptable']:
                state = self.automaton.getStateById(stateInfo['stateId'], 'getting state for update')
                state.toggleAcceptable()
                self.signalStateUpdated.emit(stateInfo)

    @Slot(object)
    def stepForward(self, input):
        self.automaton.stepForth(input)
        currentStateId = self.automaton.getCurrentStateId()
        self.signalCurrentStateChanged.emit(currentStateId)
