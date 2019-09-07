from automaton.abstracts.abstractState import AbstractState


class DFAState(AbstractState):
    def __init__(self, isAcceptable=False, isCurrent=False, isStartingState=False):
        super(DFAState, self).__init__(isAcceptable, isCurrent, isStartingState)

    def toggleAcceptable(self):
        self.isAcceptable = not self.isAcceptable

    def toggleStarting(self):
        self.isStartingState = not self.isStartingState