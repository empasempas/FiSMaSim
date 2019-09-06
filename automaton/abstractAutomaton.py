import abc
from typing import List, Dict

from PySide2.QtCore import QObject

from automaton.automataErrors import StartStateRemovalError, ActionOnNonexistentStateError, \
    ActionOnNonexistentSymbolError, DuplicateStateError, DuplicateSymbolError


class AbstractAutomaton_Meta(type(QObject), type(abc.ABCMeta)):
    pass


class AbstractAutomatonClass(QObject):
    pass


class AbstractAutomaton(AbstractAutomatonClass):
    _alphabet: List[str]
    _startState: str
    _acceptedStates: List[str]
    _states: List[str]
    _transitionDict: Dict[str, str]
    __metaclass__ = AbstractAutomaton_Meta

    def __init__(self, alphabet, startState, acceptedStates, allStates=None):
        super(AbstractAutomaton, self).__init__()
        if allStates is None:
            allStates = []
        self._alphabet = alphabet
        self._startState = startState
        self._acceptedStates = acceptedStates

        self._states = allStates
        if startState not in self._acceptedStates:
            self._states.append(self._startState)
        self._states.extend(self._acceptedStates)

        self._transitionDict = {}
        self.setState(startState)

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
    def stepForth(self, **kwargs):
        pass

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

    def addState(self, state, isAcceptable=False):
        if state in self._states:
            raise DuplicateStateError(state)
        self._states.append(state)
        if isAcceptable:
            self._acceptedStates.append(state)

    def removeState(self, state):
        if state == self._startState:
            raise StartStateRemovalError
        if state not in self._states:
            raise ActionOnNonexistentStateError('deletion')
        self._states.remove(state)
        self.removeTransitionsForState(state)
        if state in self._acceptedStates:
            self._acceptedStates.remove(state)

    def toggleStateAcceptability(self, state):
        if state not in self._states:
            raise ActionOnNonexistentStateError('toggling acceptability')
        if state in self._acceptedStates:
            self._acceptedStates.remove(state)
        else:
            self._acceptedStates.append(state)

    def isAutomatonFullyDefined(self):
        allTransitionsDefined = len(self._transitionDict) == len(self._states) * len(self._alphabet)
        hasAtLeastTwoStates = len(self._states) > 1
        hasAtLeastTwoSymbols = len(self._alphabet) > 1
        atLeastOneStateIsAccepted = len(self._acceptedStates) > 0

        return allTransitionsDefined and hasAtLeastTwoStates and hasAtLeastTwoSymbols and atLeastOneStateIsAccepted

    @abc.abstractmethod
    def isStateAcceptable(self, state):
        pass

    @abc.abstractmethod
    def getTransitionsFromState(self, state):
        pass

    @abc.abstractmethod
    def getTransitionsToState(self, state):
        pass
