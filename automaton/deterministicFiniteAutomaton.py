from automaton.abstractAutomaton import AbstractAutomaton
from automaton.automataErrors import ActionOnNonexistentStateError, ActionOnNonexistentSymbolError


class DeterministicFiniteAutomaton(AbstractAutomaton):
    _currentState: str
    limiter = "_!_"

    def __init__(self, alphabet, startState, acceptedStates, allStates=None):
        if allStates is None:
            allStates = []
        super(DeterministicFiniteAutomaton, self).__init__(alphabet, startState, acceptedStates, allStates)

    def setState(self, state):
        if state not in self._states:
            raise ActionOnNonexistentStateError('setting automaton current state')
        self._currentState = state

    @staticmethod
    def createTransitionKey(inputSymbol, currentState):
        return "{}{}{}".format(inputSymbol, DeterministicFiniteAutomaton.limiter, currentState)

    @staticmethod
    def createTransitionValue(nextState):
        return str(nextState)

    def addTransition(self, inputSymbol, currentState, nextState):
        if inputSymbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('transition addition')
        elif nextState not in self._states or currentState not in self._states:
            raise ActionOnNonexistentStateError('transition addition')
        else:
            key = DeterministicFiniteAutomaton.createTransitionKey(inputSymbol, currentState)
            value = DeterministicFiniteAutomaton.createTransitionValue(nextState)
            self._transitionDict[key] = value

    def removeTransitionsForState(self, state):
        if state not in self._states:
            raise ActionOnNonexistentStateError('transition removal')
        for symbol in self._alphabet:
            key = DeterministicFiniteAutomaton.createTransitionKey(symbol, state)
            self.removeTransition(key)

        transitionToStateKeys = []
        for key, value in self._transitionDict.items():
            if value == state:
                transitionToStateKeys.append(key)
        for key in transitionToStateKeys:
            self.removeTransition(key)

    def removeTransitionsForSymbol(self, symbol):
        if symbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('transition removal')
        for state in self._states:
            key = DeterministicFiniteAutomaton.createTransitionKey(symbol, state)
            self.removeTransition(key)

    def stepForth(self, inputSymbol):
        if inputSymbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('automaton step')
        else:
            key = DeterministicFiniteAutomaton.createTransitionKey(inputSymbol, self._currentState)
            nextState = self._transitionDict[key]
            self.setState(nextState)

    def isStateAcceptable(self, state=None):
        if state == None:
            state = self._currentState
        return state in self._acceptedStates

    def getTransitionsFromState(self, state):
        if state not in self._states:
            raise ActionOnNonexistentStateError('outbound transition retrieve')
        return {key: value for key, value in self._transitionDict.items() if
                '{}{}'.format(DeterministicFiniteAutomaton.limiter, state) in key}

    def getTransitionsToState(self, state):
        if state not in self._states:
            raise ActionOnNonexistentStateError('inbound transition retrieve')
        return {key: value for key, value in self._transitionDict.items() if value == state}
