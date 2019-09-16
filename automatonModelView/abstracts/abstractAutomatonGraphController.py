from abc import abstractmethod

from PySide2.QtCore import Signal, Slot

from automaton.abstracts.abstractGeneral import AbstractGeneralClass, AbstractGeneral_Meta
from automaton.automataErrors import DuplicateSymbolError, StartStateRemovalError, ActionOnNonexistentStateError, \
    ActionOnNonexistentSymbolError


class AbstractAutomatonGraphController(AbstractGeneralClass):
    __metaclass__ = AbstractGeneral_Meta
    signalCurrentStateChanged = Signal(str)
    signalStartingStateChanged = Signal(str)
    signalStates = Signal(list)
    signalStateAdded = Signal(object)
    signalStateRemoved = Signal(object)
    signalStateUpdated = Signal(dict)
    signalAlphabet = Signal(list)
    signalSymbolAdded = Signal(str)
    signalSymbolRemoved = Signal(str)
    signalCurrentStateId = Signal(str)
    signalTransitionAdded = Signal(dict)
    signalTransitionRemoved = Signal(dict)
    signalAutomatonIsValid = Signal()
    signalError = Signal(str)

    def __init__(self, automaton):
        super(AbstractAutomatonGraphController, self).__init__()
        self.automaton = automaton
        self._stateIdToNodeDict = {}
        # self.populateGraph()

    def populateGraph(self):
        states = self.automaton.getStates()
        if len(states) > 0:
            for state in states:
                self.signalStateAdded.emit(state)
            self.addTransitionsToGraph(states)

    @abstractmethod
    def addTransitionsToGraph(self, states):
        pass

    @Slot()
    def sendStateIds(self):
        states = self.automaton.getStates()
        ids = []
        for state in states:
            ids.append(state.id)
        self.signalStates.emit(ids)

    @Slot()
    def sendAlphabet(self):
        alphabet = self.automaton.getAlphabet()
        self.signalAlphabet.emit(alphabet)

    @Slot(object)
    @abstractmethod
    def stateEdit(self, *args):
        pass

    @Slot(object)
    @abstractmethod
    def initStateEditor(self):
        pass

    @Slot(dict)
    @abstractmethod
    def transitionEdit(self, transitionInfo):
        pass

    @Slot(object, object)
    @abstractmethod
    def initTransitionEditor(self, transitionInfo):
        pass

    @Slot(object, object)
    @abstractmethod
    def removeTransition(self, *args):
        pass

    @Slot(dict)
    @abstractmethod
    def transitionAdd(self, transitionInfo):
        pass

    @Slot(object)
    @abstractmethod
    def stepForward(self, input):
        pass

    @Slot()
    def addState(self):
        stateId = self.automaton.addState(False, False, False)
        state = self.automaton.getStateById(stateId, 'user adding state')
        self._stateIdToNodeDict[stateId] = state
        self.signalStateAdded.emit(state)

    @Slot(str)
    def removeState(self, stateId):
        try:
            self.automaton.removeState(stateId)
            self.signalStateRemoved.emit(stateId)
            self.sendStateIds()
        except ActionOnNonexistentStateError:
            self.signalError.emit('State does not exist!')
        except StartStateRemovalError:
            self.signalError.emit('Cannot remove the starting state!')

    @Slot(object)
    def addSymbol(self, symbol):
        try:
            self.automaton.addSymbol(symbol)
            self.signalSymbolAdded.emit(symbol)
        except DuplicateSymbolError:
            self.signalError.emit('Symbol already exists!')

    @Slot(object)
    def removeSymbol(self, symbol):
        try:
            self.automaton.removeSymbol(symbol)
            self.signalSymbolRemoved.emit(symbol)
        except ActionOnNonexistentSymbolError:
            self.signalError.emit('Symbol does not exist!')

    @Slot(object)
    def sendCurrentStateId(self):
        currentStateId = self.automaton.getCurrentStateId
        self.signalCurrentStateId.emit(currentStateId)

    @Slot()
    def checkAutomatonValidity(self):
        isValid = self.automaton.isAutomatonFullyDefined()
        if isValid == True:
            self.signalAutomatonIsValid.emit()
        else:
            self.signalError.emit('Automaton is not fully defined!')
