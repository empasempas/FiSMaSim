from automaton.abstracts.abstractTransition import AbstractTransition


class DFATransition(AbstractTransition):
    def __init__(self, onInput, fromState, toState):
        super(DFATransition, self).__init__(onInput, fromState, toState)

    def toNotation(self):
        return 'q{}, {} --> {}'.format(self.fromState.id, self.onInput, self.toState.id)
