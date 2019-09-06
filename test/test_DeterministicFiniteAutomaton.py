import unittest

from automaton.deterministicFiniteAutomaton import DeterministicFiniteAutomaton
from automaton.automataErrors import DuplicateStateError, DuplicateSymbolError, StartStateRemovalError, \
    ActionOnNonexistentStateError, ActionOnNonexistentSymbolError

class Test_Set_State(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        return testObj

    def test_state_is_set(self):
        testObj = self.getInstance()
        testState = '1'
        testObj.setState(testState)
        self.assertEqual(testObj._currentState, testState)

    def test_nonexistent_state_cannot_be_set(self):
        testObj = self.getInstance()
        testState = '3'
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.setState(testState)

class Test_Transition_Key_Creation(unittest.TestCase):
    def test_transition_key_creation(self):
        self.assertEqual(DeterministicFiniteAutomaton.createTransitionKey('a', 'b'), "a_!_b")

class Test_Transition_Value_Creation(unittest.TestCase):
    def test_transition_value_creation(self):
        self.assertEqual(DeterministicFiniteAutomaton.createTransitionValue('a'), 'a')

class Test_Add_Transition(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        return testObj

    def test_transition_addition_successful(self):
        testObj = self.getInstance()
        testObj.addTransition('a', '0', '1')
        self.assertDictEqual(testObj._transitionDict, {'a_!_0': '1'})

    def test_adding_transition_impossible_for_symbol_not_in_alphabet(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.addTransition('c', '0', '1')

    def test_adding_transition_not_possible_for_nonexistent_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.addTransition('a', '0', '5')

class TestRemoveTransitionsForState(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a', 'b']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        testObj.addTransition('a', '1', '2')
        testObj.addTransition('a', '2', '1')
        testObj.addTransition('a', '0', '2')
        return testObj

    def test_removal_is_successful(self):
        testObj = self.getInstance()
        testObj.removeTransitionsForState('1')
        self.assertDictEqual(testObj._transitionDict, {'a_!_0': '2'})

    def test_removal_impossible_for_state_not_in_set(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.removeTransitionsForState('5')

class TestRemoveTransitionsForSymbol(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a', 'b']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        testObj.addTransition('a', '1', '2')
        testObj.addTransition('a', '2', '1')
        testObj.addTransition('b', '0', '2')
        return testObj

    def test_removal_is_successful(self):
        testObj = self.getInstance()
        testObj.removeTransitionsForSymbol('a')
        self.assertDictEqual(testObj._transitionDict, {'b_!_0': '2'})

    def test_removal_impossible_for_symbol_not_in_alphabet(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.removeTransitionsForSymbol('c')

class Test_Step_Forth(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a', 'b']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        testObj.addTransition('a', '1', '2')
        testObj.addTransition('a', '2', '1')
        testObj.addTransition('b', '0', '2')
        return testObj

    def test_step_successful(self):
        testObj = self.getInstance()
        testObj.stepForth('b')
        self.assertEqual(testObj._currentState, '2')

    def test_step_not_done_for_symbol_not_in_alphabet(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.stepForth('c')

class Test_Is_State_Acceptable(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a', 'b']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        return testObj

    def test_state_recognized_as_acceptable(self):
        testObj = self.getInstance()
        self.assertTrue(testObj.isStateAcceptable('1'))

    def test_current_state_acceptable(self):
        testObj = self.getInstance()
        self.assertTrue(testObj.isStateAcceptable())

    def test_state_recognized_as_rejected(self):
        testObj = self.getInstance()
        self.assertFalse(testObj.isStateAcceptable('2'))

    def test_current_state_recognized_as_rejected(self):
        testObj = self.getInstance()
        testObj.setState('2')
        self.assertFalse(testObj.isStateAcceptable())

class Test_Get_Transitions_From_State(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a', 'b']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        testObj.addTransition('a', '1', '2')
        testObj.addTransition('a', '2', '1')
        testObj.addTransition('b', '1', '0')
        return testObj

    def test_get_all_transitions(self):
        testObj = self.getInstance()
        self.assertDictEqual(testObj.getTransitionsFromState('1'), {'a_!_1': '2', 'b_!_1': '0'})

    def test_get_transitions_from_nonexistent_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.getTransitionsFromState('5')

class Test_Get_Transitions_To_State(unittest.TestCase):
    def getInstance(self):
        alphabet = ['a', 'b']
        testStartState = '0'
        testAcceptedStates = [testStartState, '1']
        stateSet = [testStartState, '1', '2']
        testObj = DeterministicFiniteAutomaton(alphabet, testStartState, testAcceptedStates, stateSet)
        testObj.addTransition('a', '1', '2')
        testObj.addTransition('a', '2', '1')
        testObj.addTransition('b', '1', '2')
        return testObj

    def test_get_all_transitions(self):
        testObj = self.getInstance()
        self.assertDictEqual(testObj.getTransitionsToState('2'), {'a_!_1': '2', 'b_!_1': '2'})

    def test_get_transitions_from_nonexistent_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.getTransitionsToState('5')

if __name__ == '__main__':
    unittest.main()
