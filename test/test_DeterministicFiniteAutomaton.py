import unittest

from automaton.automataErrors import ActionOnNonexistentStateError, ActionOnNonexistentSymbolError
from automaton.deterministicFiniteAutomaton.deterministicFiniteAutomaton import DeterministicFiniteAutomaton


class Test_Add_State(unittest.TestCase):
    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 1)
        return testObj

    def test_state_added_successfully(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj._states), 1)
        testObj.addState()
        self.assertEqual(len(testObj._states), 2)


class Test_Set_State(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        return testObj

    def test_current_state_changes(self):
        testObj = self.getInstance()
        currentState = testObj._currentState
        testObj.setState(self.state1Id)
        self.assertTrue(testObj._currentState is not currentState)

    def test_nonexistent_state_cannot_be_set(self):
        testObj = self.getInstance()
        testState = '3'
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.setState(testState)


class Test_Set_Starting_State(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        return testObj

    def test_starting_state_changes(self):
        testObj = self.getInstance()
        startingState = testObj._startingState
        testObj.setStartingState(self.state1Id)
        self.assertTrue(testObj._startingState is not startingState)

    def test_nonexistent_state_cannot_be_set(self):
        testObj = self.getInstance()
        testState = '3'
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.setStartingState(testState)


class Test_Transition_Key_Creation(unittest.TestCase):
    def test_transition_key_creation(self):
        self.assertEqual(DeterministicFiniteAutomaton.createTransitionKey('a', 'b'), "a_!_b")


class Test_Transition_Value_Creation(unittest.TestCase):
    def test_transition_value_creation(self):
        value = DeterministicFiniteAutomaton.createTransitionValue('a', 'b', 'c')
        self.assertEqual(value.fromState, 'a')
        self.assertEqual(value.onInput, 'b')
        self.assertEqual(value.toState, 'c')


# class Test_Abstract_Automaton_Toggle_State_Acceptability(unittest.TestCase):
#     testAlphabet = ['a']
#     testStartState = '0'
#     testAcceptedStates = [testStartState]
#     testState = 'b'
#
#     def getInstance(self):
#         testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, list(self.testAcceptedStates))
#         return testObj
#
#     def test_toggle_acceptability_to_rejected(self):
#         testObj = self.getInstance()
#         testObj.toggleStateAcceptability(self.testStartState)
#         self.assertListEqual(testObj._acceptedStates, [])
#
#     def test_toggle_acceptability_from_rejected_to_acceptable(self):
#         testObj = self.getInstance()
#         testObj.addState(self.testState)
#
#         testObj.toggleStateAcceptability(self.testState)
#         self.assertListEqual(testObj._acceptedStates, [self.testStartState, self.testState])
#
#     def test_toggle_acceptability_on_nonexistent_state(self):
#         testObj = self.getInstance()
#
#         with self.assertRaises(ActionOnNonexistentStateError):
#             testObj.toggleStateAcceptability(self.testState)

# class Test_Abstract_Automaton_Add_State(unittest.TestCase):
# testStartState = '0'
# testAlphabet = ['a']
# testAcceptedStates = [testStartState]
# testState = 'b'
#
# def getInstance(self):
#     testObj = AbstractAutomaton(self.testAlphabet, self.testStartState, list(self.testAcceptedStates))
#     return testObj
#
# def test_add_state(self):
#     testObj = self.getInstance()
#
#     testObj.addState(self.testState)
#     self.assertListEqual(testObj._states, [self.testStartState, self.testState])
#     self.assertListEqual(testObj._acceptedStates, self.testAcceptedStates)
#
# def test_add_acceptable_state(self):
#     testObj = self.getInstance()
#
#     testObj.addState(self.testState, True)
#     self.assertListEqual(testObj._states, [self.testStartState, self.testState])
#     self.assertListEqual(testObj._acceptedStates, testObj._states)
#
# def test_adding_duplicate_state_should_be_impossible(self):
#     testObj = self.getInstance()
#
#     testObj.addState(self.testState)
#     with self.assertRaises(DuplicateStateError):
#         testObj.addState(self.testState)
#     self.assertListEqual(testObj._states, [self.testStartState, self.testState])


class Test_Add_Transition(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        return testObj

    def test_transition_addition_successful(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj._transitionDict), 0)
        testObj.addTransition(self.state0Id, 'a', self.state1Id)
        self.assertEqual(len(testObj._transitionDict), 1)

    def test_adding_transition_impossible_for_symbol_not_in_alphabet(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.addTransition(self.state0Id, 'x', self.state1Id)

    def test_adding_transition_not_possible_for_nonexistent_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.addTransition('i', 'a', self.state1Id)

    def test_adding_transition_not_possible_for_nonexistent_target_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.addTransition(self.state1Id, 'a', 'i')


class Test_Remove_Transitions_For_State(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        testObj.addTransition(self.state0Id, 'a', self.state1Id)
        return testObj

    def test_removal_is_successful(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj._transitionDict), 1)
        testObj.removeTransitionsForState(self.state0Id)
        self.assertEqual(len(testObj._transitionDict), 0)

    def test_removal_impossible_for_state_not_in_set(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.removeTransitionsForState('5')


class Test_Remove_Transitions_For_Symbol(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        testObj.addTransition(self.state0Id, 'a', self.state1Id)
        return testObj

    def test_removal_is_successful(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj._transitionDict), 1)
        testObj.removeTransitionsForSymbol('a')
        self.assertEqual(len(testObj._transitionDict), 0)

    def test_removal_impossible_for_symbol_not_in_alphabet(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.removeTransitionsForSymbol('c')


class Test_Step_Forth(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        testObj.addTransition(self.state0Id, 'a', self.state1Id)
        return testObj

    def test_step_successful(self):
        testObj = self.getInstance()
        testObj.stepForth('a')
        self.assertTrue(testObj._currentState is testObj._states.get(self.state1Id))

    def test_step_not_done_for_symbol_not_in_alphabet(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentSymbolError):
            testObj.stepForth('c')

class Test_Get_Transitions_From_State(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        testObj.addTransition(self.state0Id, 'a', self.state1Id)
        return testObj

    def test_get_all_transitions(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj.getTransitionsFromState(self.state0Id)), 1)

    def test_empty_list_is_returned_when_no_transitions_exist(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj.getTransitionsFromState(self.state1Id)), 0)

    def test_get_transitions_from_nonexistent_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.getTransitionsFromState('5')


class Test_Get_Transitions_To_State(unittest.TestCase):
    state0Id = None
    state1Id = None

    def getInstance(self):
        testObj = DeterministicFiniteAutomaton(['a'], 0, [0], 2)
        self.state0Id = list(testObj._states.keys())[0]
        self.state1Id = list(testObj._states.keys())[1]
        testObj.addTransition(self.state0Id, 'a', self.state1Id)
        return testObj

    def test_get_all_transitions(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj.getTransitionsToState(self.state1Id)), 1)

    def test_empty_list_is_returned_when_no_transitions_exist(self):
        testObj = self.getInstance()
        self.assertEqual(len(testObj.getTransitionsToState(self.state0Id)), 0)

    def test_get_transitions_from_nonexistent_state(self):
        testObj = self.getInstance()
        with self.assertRaises(ActionOnNonexistentStateError):
            testObj.getTransitionsToState('5')


if __name__ == '__main__':
    unittest.main()
