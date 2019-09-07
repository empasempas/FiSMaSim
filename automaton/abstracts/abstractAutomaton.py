import abc

from automaton.abstracts.abstractGeneral import AbstractGeneralClass, AbstractGeneral_Meta
from automaton.abstracts.abstractState import AbstractState
from automaton.automataErrors import StartStateRemovalError, ActionOnNonexistentStateError, \
    ActionOnNonexistentSymbolError, DuplicateSymbolError


class AbstractAutomaton(AbstractGeneralClass):
    __metaclass__ = AbstractGeneral_Meta

    def __init__(self, alphabet, startStateIndex, acceptedStateIndexes, totalStateCount):
        if acceptedStateIndexes is None:
            acceptedStateIndexes = []
        self._currentState = None
        self._startingState = None

        super(AbstractAutomaton, self).__init__()
        self._states = {}
        for i in range(totalStateCount):
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
    def addState(self, isAcceptable, isCurrent, isStartingState):
        state = AbstractState(isAcceptable, isCurrent, isStartingState)
        self._states[state.id] = state
        return state.id

    def getStates(self):
        return list(self._states.values())

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
        self._alphabet.remove(symbol)
        self.removeTransitionsForSymbol(symbol)

    def removeState(self, stateId):
        state = self.getStateById(stateId, 'deletion')
        if state is self._startingState:
            raise StartStateRemovalError
        del self._states[stateId]
        self.removeTransitionsForState(stateId)
