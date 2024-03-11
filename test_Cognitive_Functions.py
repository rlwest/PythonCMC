
import unittest
import random
from utility import Utility  # Import the Utility class from the utility module
from Cognitive_Functions import match_chunks_with_diagnostics

class TestCogFunc(unittest.TestCase):
    # TestUtility class inherits from unittest.TestCase, which provides a framework for writing and running tests

    def test_match_chunks_with_diagnostics(self):
        # Define a buffer with several items, each represented as a dictionary.
        # These items have different attributes and utility values.
        print('this test will print some things as part of its normal actions, they are not diagnostic')
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
