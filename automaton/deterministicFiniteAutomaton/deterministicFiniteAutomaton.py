from automaton.abstracts.abstractAutomaton import AbstractAutomaton
from automaton.automataErrors import ActionOnNonexistentStateError, ActionOnNonexistentSymbolError
from automaton.deterministicFiniteAutomaton.dfaState import DFAState
from automaton.deterministicFiniteAutomaton.dfaTransition import DFATransition


class DeterministicFiniteAutomaton(AbstractAutomaton):
    limiter = "_!_"

    def __init__(self, alphabet, startStateIndex=0, acceptedStateIndexes=None, totalStateCount=1):
        if acceptedStateIndexes is None:
            acceptedStateIndexes = []
        super(DeterministicFiniteAutomaton, self).__init__(alphabet, startStateIndex, acceptedStateIndexes,
                                                           totalStateCount)

    def addState(self, isAcceptable=False, isCurrent=False, isStartingState=False):
        state = DFAState(isAcceptable, isCurrent, isStartingState)
        self._states[state.id] = state
        if (isCurrent):
            self.setState(state.id)
        if (isStartingState):
            self.setStartingState(state.id)
        return state.id

    def setState(self, stateId):
        state = self.getStateById(stateId, 'setting automaton current state')
        if self._currentState is not None:
            self._currentState.toggleCurrent()
        self._currentState = state
        state.toggleCurrent()

    def setStartingState(self, stateId):
        state = self.getStateById(stateId, 'setting automaton starting state')
        if self._startingState is not None:
            self._startingState.toggleStarting()
        self._startingState = state
        state.toggleStarting()

    @staticmethod
    def createTransitionKey(inputSymbol, currentStateId):
        return "{}{}{}".format(inputSymbol, DeterministicFiniteAutomaton.limiter, currentStateId)

    @staticmethod
    def createTransitionValue(currentState, inputSymbol, nextState):
        return DFATransition(fromState=currentState, onInput=inputSymbol, toState=nextState)

    def addTransition(self, currentStateId, inputSymbol, nextStateId):
        if inputSymbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('transition addition')
        elif nextStateId not in self._states or currentStateId not in self._states:
            raise ActionOnNonexistentStateError('transition addition')
        else:
            key = DeterministicFiniteAutomaton.createTransitionKey(inputSymbol, currentStateId)
            value = DeterministicFiniteAutomaton.createTransitionValue(self._states.get(currentStateId), inputSymbol,
                                                                       self._states.get(nextStateId))
            self._transitionDict[key] = value

    def removeTransitionsForState(self, stateId):
        if stateId not in self._states:
            raise ActionOnNonexistentStateError('transition removal')

        transitionToFromStateKeys = []
        state = self._states.get(stateId)
        for key, transition in self._transitionDict.items():
            if transition.toState is state or transition.fromState is state:
                transitionToFromStateKeys.append(key)
        for key in transitionToFromStateKeys:
            self.removeTransition(key)

    def removeTransitionsForSymbol(self, symbol):
        if symbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('transition removal')

        transitionOnSymbolKeys = []
        for key, transition in self._transitionDict.items():
            if transition.onInput == symbol:
                transitionOnSymbolKeys.append(key)
        for key in transitionOnSymbolKeys:
            self.removeTransition(key)

    def getTransitionsFromState(self, stateId):
        state = self.getStateById(stateId, 'outbound transition retrieve')
        return [x for x in self._transitionDict.values() if x.fromState is state]

    def getTransitionsToState(self, stateId):
        state = self.getStateById(stateId, 'inbound transition retrieve')
        return [x for x in self._transitionDict.values() if x.toState is state]

    def stepForth(self, inputSymbol):
        if inputSymbol not in self._alphabet:
            raise ActionOnNonexistentSymbolError('automaton step')
        else:
            key = DeterministicFiniteAutomaton.createTransitionKey(inputSymbol, self._currentState.id)
            transition = self._transitionDict[key]
            self.setState(transition.toState.id)

    def isAutomatonFullyDefined(self):
        allTransitionsDefined = len(self._transitionDict) == len(self._states) * len(self._alphabet)
        hasAtLeastTwoStates = len(self._states) > 1
        hasAtLeastTwoSymbols = len(self._alphabet) > 1
        atLeastOneStateIsAccepted = len([x for x in self._states.values() if x.isAcceptable]) > 0

        return allTransitionsDefined and hasAtLeastTwoStates and hasAtLeastTwoSymbols and atLeastOneStateIsAccepted
