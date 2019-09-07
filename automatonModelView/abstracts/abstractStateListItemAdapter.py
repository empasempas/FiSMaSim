import uuid

from automaton.abstracts.abstractGeneral import AbstractGeneral_Meta, AbstractGeneralClass


class AbstractStateListItemAdapter(AbstractGeneralClass):
    __metaclass__ = AbstractGeneral_Meta

    def __init__(self, state):
        super(AbstractStateListItemAdapter, self).__init__()
        self.id = uuid.uuid4()
        self.stateId = state.id
        self.isAcceptable = state.isAcceptable
        self.isCurrent = state.isCurrent
        self.isStartingState = state.isStartingState
        self.transitionsTo = {}

    def toggleAcceptable(self):
        self.isAcceptable = not self.isAcceptable

    def toggleCurrent(self):
        self.isCurrent = not self.isCurrent

    def toggleStartingState(self):
        self.isStartingState = not self.isStartingState

    def mapTransitionsToAdapters(self, transitions=None, otherAdapters=None):
        if otherAdapters is None:
            otherAdapters = []
        if transitions is None:
            transitions = []

        for transition in transitions:
            if transition.fromState.id == self.stateId:
                for adapter in otherAdapters:
                    if adapter.stateId == transition.toState.id:
                        self.transitionsTo[transition.onInput] = adapter
