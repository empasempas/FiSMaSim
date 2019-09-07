import abc

from automaton.abstracts.abstractGeneral import AbstractGeneralClass, AbstractGeneral_Meta


class AbstractTransition(AbstractGeneralClass):
    __metaclass__ = AbstractGeneral_Meta

    def __init__(self, onInput, fromState, toState):
        super(AbstractTransition, self).__init__()
        self.onInput = onInput
        self.fromState = fromState
        self.toState = toState

    @abc.abstractmethod
    def toNotation(self):
        pass
