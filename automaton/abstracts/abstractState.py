import uuid

from automaton.abstracts.abstractGeneral import AbstractGeneralClass, AbstractGeneral_Meta


class AbstractState(AbstractGeneralClass):
    __metaclass__ = AbstractGeneral_Meta

    def __init__(self, isAcceptable=False, isCurrent=False, isStartingState=False):
        super(AbstractState, self).__init__()
        self.isAcceptable = isAcceptable
        self.isCurrent = isCurrent
        self.isStartingState = isStartingState
        self.id = uuid.uuid4()

    def toggleCurrent(self):
        self.isCurrent = not self.isCurrent
