import unittest
from unittest.mock import Mock

from automaton.abstractAutomaton import AbstractAutomaton
from automaton.automataErrors import DuplicateStateError, DuplicateSymbolError, StartStateRemovalError, \
    ActionOnNonexistentStateError, ActionOnNonexistentSymbolError


class Test_Abstract_Automaton_Add_Symbol(unittest.TestCase):
    def getInstanceWithAlphabet(self, alphabet):
        testStartState = '0'
        testAcceptedStates = [testStartState]
        testObj = AbstractAutomaton(alphabet, testStartState, testAcceptedStates)
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


class Test_Abstract_Automaton_Add_State(unittest.TestCase):
    testStartState = '0'
    testAlphabet = ['a']
    testAcceptedStates = [testStartState]
    testState = 'b'

    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, list(self.testAcceptedStates))
        return testObj

    def test_add_state(self):
        testObj = self.getInstance()

        testObj.addState(self.testState)
        self.assertListEqual(testObj._states, [self.testStartState, self.testState])
        self.assertListEqual(testObj._acceptedStates, self.testAcceptedStates)

    def test_add_acceptable_state(self):
        testObj = self.getInstance()

        testObj.addState(self.testState, True)
        self.assertListEqual(testObj._states, [self.testStartState, self.testState])
        self.assertListEqual(testObj._acceptedStates, testObj._states)

    def test_adding_duplicate_state_should_be_impossible(self):
        testObj = self.getInstance()

        testObj.addState(self.testState)
        with self.assertRaises(DuplicateStateError):
            testObj.addState(self.testState)
        self.assertListEqual(testObj._states, [self.testStartState, self.testState])


class Test_Abstract_Automaton_Remove_Symbol(unittest.TestCase):
    testAlphabet = ['a']
    testStartState = '0'
    testAcceptedStates = [testStartState]
    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, self.testAcceptedStates)
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
    testStartState = '0'
    testAcceptedStates = [testStartState]
    testState = 'b'

    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, self.testAcceptedStates)
        testObj.removeTransitionsForState = Mock()
        return testObj

    def test_remove_state(self):
        testObj = self.getInstance()
        testObj.addState(self.testState)
        self.assertListEqual(testObj._states, [self.testStartState, self.testState])

        testObj.removeState(self.testState)
        self.assertListEqual(testObj._states, [self.testStartState])

    def test_remove_start_state_raises_exception(self):
        testObj = self.getInstance()

        with self.assertRaises(StartStateRemovalError):
            testObj.removeState(self.testStartState)

    def test_remove_nonexistent_state(self):
        testObj = self.getInstance()

        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.removeState(self.testState)


class Test_Abstract_Automaton_Toggle_State_Acceptability(unittest.TestCase):
    testAlphabet = ['a']
    testStartState = '0'
    testAcceptedStates = [testStartState]
    testState = 'b'

    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, list(self.testAcceptedStates))
        return testObj

    def test_toggle_acceptability_to_rejected(self):
        testObj = self.getInstance()
        testObj.toggleStateAcceptability(self.testStartState)
        self.assertListEqual(testObj._acceptedStates, [])

    def test_toggle_acceptability_from_rejected_to_acceptable(self):
        testObj = self.getInstance()
        testObj.addState(self.testState)

        testObj.toggleStateAcceptability(self.testState)
        self.assertListEqual(testObj._acceptedStates, [self.testStartState, self.testState])

    def test_toggle_acceptability_on_nonexistent_state(self):
        testObj = self.getInstance()

        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.toggleStateAcceptability(self.testState)

class Test_Is_AutomatonFully_Defined(unittest.TestCase):
    testAlphabet = ['a', 'b']
    testStartState = '0'
    testAcceptedStates = ['1']
    testStates = [testStartState, '1']

    def getInstance(self):
        testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, list(self.testAcceptedStates))
        testObj._transitionDict = {'a_!_0': '1', 'b_!_0': '1', 'a_!_1': '1', 'b_!_1': '0'}
        return testObj

    def test_automaton_is_defined(self):
        testObj = self.getInstance()
        self.assertTrue(testObj.isAutomatonFullyDefined())

    def test_automaton_is_not_defined(self):
        testObj = self.getInstance()
        testObj.removeTransition('a_!_0')
        self.assertFalse(testObj.isAutomatonFullyDefined())


if __name__ == '__main__':
    unittest.main()
