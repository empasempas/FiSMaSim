import abc

from aspect.logging import logFunction
from automaton.abstracts.abstractGeneral import AbstractGeneralClass, AbstractGeneral_Meta
from automaton.abstracts.abstractState import AbstractState
from automaton.automataErrors import StartStateRemovalError, ActionOnNonexistentStateError, \
    ActionOnNonexistentSymbolError, DuplicateSymbolError


class AbstractAutomaton(AbstractGeneralClass):
    __metaclass__ = AbstractGeneral_Meta

    def __init__(self, alphabet, startStateIndex, acceptedStateIndexes, totalStateCount):
        if acceptedStateIndexes is None:
            acceptedStateIndexes = []
        super(AbstractAutomaton, self).__init__()
        self._currentState = None
        self._startingState = None
        self._states = {}
        for i in range(0, totalStateCount):
            isAcceptable = i in acceptedStateIndexes
            isCurrent = i == startStateIndex
            isStartingState = i == startStateIndex
            self.addState(isAcceptable, isCurrent, isStartingState)
        self._alphabet = alphabet
        self._transitionDict = {}

    @abc.abstractmethod
    def setState(self, args):
        pass

    @staticmethod
    @abc.abstractmethod
    def createTransitionKey(**kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def createTransitionValue(**kwargs):
        pass

    @abc.abstractmethod
    def addTransition(self, **kwargs):
        pass

    @abc.abstractmethod
    def removeTransitionsForState(self, state):
        pass

    @abc.abstractmethod
    def removeTransitionsForSymbol(self, symbol):
        pass

    @abc.abstractmethod
    def getTransitionsFromState(self, stateId):
        pass

    @abc.abstractmethod
    def getTransitionsToState(self, stateId):
        pass

    @abc.abstractmethod
    def stepForth(self, **kwargs):
        pass

    @abc.abstractmethod
    def isAutomatonFullyDefined(self):
        pass

    @abc.abstractmethod
    @logFunction
    def addState(self, isAcceptable, isCurrent, isStartingState):
        state = AbstractState(isAcceptable, isCurrent, isStartingState)
        self._states[state.id] = state
        if isCurrent == True:
            self._currentState = state
        return state.id

    def getStates(self):
        return list(self._states.values())

    def getAlphabet(self):
        return self._alphabet

    def getCurrentStateId(self):
        return self._currentState.id

    def _checkStateExists(self, stateId, actionDescription):
        if stateId not in self._states:
            raise ActionOnNonexistentStateError(actionDescription)

    def getStateById(self, stateId, actionDescription):
        self._checkStateExists(stateId, actionDescription)
        return self._states.get(stateId)

    def removeTransition(self, key):
        if key in self._transitionDict:
            del self._transitionDict[key]

    def addSymbol(self, symbol):
        if symbol in self._alphabet:
            raise DuplicateSymbolError
        self._alphabet.append(symbol)

    def removeSymbol(self, symbol):
        if symbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('deletion')
        self.removeTransitionsForSymbol(symbol)
        self._alphabet.remove(symbol)

    def removeState(self, stateId):
        state = self.getStateById(stateId, 'deletion')
        if state is self._startingState:
            raise StartStateRemovalError
        self.removeTransitionsForState(stateId)
        del self._states[stateId]
