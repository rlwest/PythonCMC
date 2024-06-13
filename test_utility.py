
import unittest
import random
from utility import Utility  # Import the Utility class from the utility module

class TestUtility(unittest.TestCase):
    # TestUtility class inherits from unittest.TestCase, which provides a framework for writing and running tests

    def test_check_match(self):
        # Test the check_match static method of the Utility class
        self.assertTrue(Utility.check_match('key', 'value', {'key': 'value'}))
        # Assert True if the key-value pair matches exactly

        self.assertFalse(Utility.check_match('key', 'wrong', {'key': 'value'}))
        # Assert False if the value does not match the dictionary value for the given key

        self.assertTrue(Utility.check_match('key', '*', {'key': 'value'}))
        # Assert True if wildcard '*' is used, indicating any value for the given key is acceptable

    def test_check_positive_matches(self):
        # Test the check_positive_matches static method
        self.assertTrue(Utility.check_positive_matches({'a': 1, 'b': 2}, {'a': 1}))
        # Assert True if all key-value pairs in matching_dict are found in buffer_dict

        self.assertFalse(Utility.check_positive_matches({'a': 1, 'b': 2}, {'c': 3}))
        # Assert False if a key-value pair in matching_dict is not found in buffer_dict

        self.assertTrue(Utility.check_positive_matches({'a': 1, 'b': 2}, {'a': '*'}))
        # Assert True if a wildcard '*' is used, indicating any value for the key 'a' is acceptable

    def test_check_negative_matches(self):
        # Test the check_negative_matches static method
        self.assertTrue(Utility.check_negative_matches({'a': 1, 'b': 2}, {'c': 3}))
        # Assert True if none of the key-value pairs in negation_dict are found in buffer_dict

        self.assertFalse(Utility.check_negative_matches({'a': 1, 'b': 2}, {'a': 1}))
        # Assert False if a key-value pair in negation_dict is found in buffer_dict

    def test_buffer_match_eval(self):
        # Test the buffer_match_eval static method
        self.assertTrue(Utility.buffer_match_eval({'a': 1, 'b': 2}, {'a': 1}, {'c': 3}))
        # Assert True if the buffer matches all positive conditions and none of the negative conditions

        self.assertFalse(Utility.buffer_match_eval({'a': 1, 'b': 2}, {'a': 1}, {'b': 2}))
        # Assert False if the buffer matches a negative condition

    def test_find_max(self):
        # note, find_max requires all items have a utility value
        
        random.seed(0)  # Ensure predictability in tests involving randomness
        
        self.assertEqual(Utility.find_max([{'utility': 1}, {'utility': 2}]), {'utility': 2})
        # Assert that the item with the highest utility is returned

        self.assertIn(Utility.find_max([{'utility': 2}, {'utility': 2}]), [{'utility': 2}, {'utility': 2}])
        # Assert that one of the items with the highest utility is returned when there are multiple

        self.assertIsNone(Utility.find_max([]))
        # Assert None is returned if the input list is empty

        self.assertEqual(Utility.find_max([{'utility': 42}]), {'utility': 42})
        # If there's only one item with 'utility', it should be returned

        self.assertEqual(Utility.find_max([{'utility': -1}, {'utility': -5}, {'utility': -3}]), {'utility': -1})
        # The item with the highest (least negative) utility should be returned


    def test_buffer_match_eval_diagnostic(self):
        # Test the buffer_match_eval_diagnostic method, assuming it returns a tuple (bool, dict)
        match, wildcard_values = Utility.buffer_match_eval_diagnostic({'a': 1, 'b': 2}, {'a': 1}, {'c': 3})
        self.assertTrue(match)
        # Assert True if the buffer matches the criteria

        self.assertEqual(wildcard_values, {})
        # Assert the returned wildcard values dictionary is empty as expected in this test case

    def test_match_chunks_with_diagnostics(self):
        # Define a buffer with several items, each represented as a dictionary.
        # These items have different attributes and utility values.
        # print('this test will print some things as part of its normal actions, they are not diagnostic')
        buffer = {
            'chunk1': {'type': 'task', 'status': 'complete', 'utility': 5},
            'chunk2': {'type': 'task', 'status': 'incomplete', 'utility': 8},
            'chunk3': {'type': 'event', 'status': 'upcoming', 'utility': 3}
        }

        # Define cues for matching and negation. Here, we look for tasks that are not complete.
        cue = {
            'matches': {'type': 'task'},
            'negations': {'status': 'complete'}
        }

        # Call the match_chunks_with_diagnostics function with the buffer and cues.
        # The expected result is 'chunk2' since it's the only 'task' that is not 'complete',
        # and it has the highest utility among the matching items.
        best_chunk = Utility.match_chunks_with_diagnostics(buffer, cue)

        # Assert that the returned best_chunk is indeed 'chunk2' and its details match our expectation.
        expected_chunk = {'type': 'task', 'status': 'incomplete', 'utility': 8}
        self.assertEqual(best_chunk, expected_chunk)




if __name__ == '__main__':
    unittest.main()
    # Run the tests when the script is executed
