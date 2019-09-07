class Error(Exception):
    pass


class DuplicateSymbolError(Error):
    def __init__(self):
        self.message = "Symbol already exists in alphabet"


class StartStateRemovalError(Error):
    def __init__(self):
        self.message = "Illegal action - start state cannot be removed"


class ActionOnNonexistentStateError(Error):
    def __init__(self, action):
        self.message = "Illegal action - {} attempted on a state that does not exist".format(action)


class ActionOnNonexistentSymbolError(Error):
    def __init__(self, action):
        self.message = "Illegal action - {} attempted on a symbol that is not in the alphabet".format(action)
