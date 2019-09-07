import unittest
import uuid
from unittest.mock import Mock

from automaton.abstracts.abstractAutomaton import AbstractAutomaton
from automaton.automataErrors import DuplicateSymbolError, StartStateRemovalError, ActionOnNonexistentStateError, \
    ActionOnNonexistentSymbolError


class Test_Abstract_Automaton_Remove_Transition(unittest.TestCase):
    def getInstance(self):
        testObj = AbstractAutomaton(['a'], 0, [0], 1)
        testObj._transitionDict[0] = 0
        testObj._transitionDict[1] = 1
        return testObj

    def test_remove_transition(self):
        testObj = self.getInstance()
        self.assertTrue(0 in testObj._transitionDict)
        testObj.removeTransition(0)
        self.assertFalse(0 in testObj._transitionDict)

    def remove_nonexistent_transition_fails_silently(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj._transitionDict), 2)
        testObj.removeTransition(3)
        self.assertEqual(len(testObj._transitionDict), 2)


class Test_Abstract_Automaton_Add_Symbol(unittest.TestCase):
    def getInstanceWithAlphabet(self, alphabet):
        testObj = AbstractAutomaton(alphabet, 0, [0], 1)
        return testObj

    def test_add_symbol(self):
        testObj = self.getInstanceWithAlphabet([])
        testSymbol = 'a'
        testObj.addSymbol(testSymbol)
        self.assertListEqual(testObj._alphabet, [testSymbol])

    def test_previously_added_symbol_does_not_duplicate(self):
        testSymbol = 'a'
        testAlphabet = [testSymbol]
        testObj = self.getInstanceWithAlphabet(testAlphabet)

        with self.assertRaises(DuplicateSymbolError):
            testObj.addSymbol(testSymbol)
        self.assertListEqual(testObj._alphabet, testAlphabet)


class Test_Abstract_Automaton_Remove_Symbol(unittest.TestCase):
    testAlphabet = ['a']

    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, 0, [0], 1)
        testObj.removeTransitionForSymbol = Mock()
        return testObj

    def test_remove_symbol(self):
        testObj = self.getInstance()
        testObj.removeSymbol('a')
        self.assertListEqual(testObj._alphabet, [])

    def test_remove_symbol_that_is_not_in_alphabet(self):
        testObj = self.getInstance()

        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.removeSymbol('b')
        self.assertListEqual(testObj._alphabet, self.testAlphabet)


class Test_Abstract_Automaton_Remove_State(unittest.TestCase):
    testAlphabet = ['a']
    stateId0 = None
    stateId1 = None
    startStateId = None

    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, 0, [0], 2)
        testObj.removeTransitionsForState = Mock()
        self.stateId0 = list(testObj._states.keys())[0]
        self.stateId1 = list(testObj._states.keys())[1]
        self.startStateId = self.stateId0
        testObj._startingState = testObj._states.get(self.stateId0)
        return testObj

    def test_remove_state(self):
        testObj = self.getInstance()
        self.assertListEqual(list(testObj._states.keys()), [self.stateId0, self.stateId1])
        testObj.removeState(self.stateId1)
        self.assertListEqual(list(testObj._states.keys()), [self.stateId0])

    def test_remove_start_state_raises_exception(self):
        testObj = self.getInstance()

        with self.assertRaises(StartStateRemovalError):
            testObj.removeState(self.startStateId)

    def test_remove_nonexistent_state(self):
        testObj = self.getInstance()
        testId = uuid.uuid4()

        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.removeState(testId)


if __name__ == '__main__':
    unittest.main()
