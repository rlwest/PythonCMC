"""
these funcitons perform basic actions in the produciton system
"""


import random


class Utility: # this class provides utility functions for matching and choosing chunks
    
    @staticmethod
    def check_match(key, value, target_dict, wildcard='*'):
        """
        Check if a single key-value pair matches in the target dictionary.
        This will be used below in 'check_positive_matches' and 'check_negative_matches'
        Args:
            key (str): The key to look for in the target dictionary.
            value (str): The value to match against the value in the target dictionary.
            target_dict (dict): The dictionary to search in.
            wildcard (str, optional): A special character used to indicate any value is acceptable. Defaults to '*'.
        Returns:
            bool: True if the key exists in the dictionary and the corresponding value matches, False otherwise.
        """
        return key in target_dict and (value == wildcard or target_dict[key] == value)

    @staticmethod
    def check_positive_matches(buffer_dict, matching_dict, wildcard='*'):
        """
        Check if all key-value pairs in the matching dictionary are found in the buffer dictionary.
        Args:
            buffer_dict (dict): The buffer dictionary where matches are looked for.
            matching_dict (dict): The dictionary containing key-value pairs to match.
            wildcard (str, optional): A character that represents any value. Defaults to '*'.
        Returns:
            bool: True if all key-value pairs match, False otherwise.
        """
        return all(Utility.check_match(key, value, buffer_dict, wildcard) for key, value in matching_dict.items())

    @staticmethod
    def check_negative_matches(buffer_dict, negation_dict):
        """
        Check if none of the key-value pairs in the negation dictionary are found in the buffer dictionary.
        Args:
            buffer_dict (dict): The buffer dictionary where matches are checked.
            negation_dict (dict): The dictionary containing key-value pairs that should not match.
        Returns:
            bool: True if none of the key-value pairs are found in the buffer dictionary, False otherwise.
        """
        return not any(Utility.check_match(key, value, buffer_dict) for key, value in negation_dict.items())

    @staticmethod
    def buffer_match_eval(buffer_dict, matching_dict, negation_dict, wildcard='*'):
        """
        Evaluate if a buffer matches given positive and negative conditions.
        Args:
            buffer_dict (dict): The buffer dictionary to evaluate.
            matching_dict (dict): The dictionary of conditions that should match.
            negation_dict (dict): The dictionary of conditions that should not match.
            wildcard (str, optional): A character that represents any value. Defaults to '*'.
        Returns:
            bool: True if the buffer matches all positive conditions and none of the negative conditions, False otherwise.
        """
        return Utility.check_positive_matches(buffer_dict, matching_dict, wildcard) and Utility.check_negative_matches(buffer_dict, negation_dict)



    @staticmethod
    def find_max(match_list):
        """
        Selects the item with the highest utility from a list of items.
        Args:
            match_list (list): A list of items where each item is a dictionary containing at least a 'utility' key.
        Returns:
            dict: The item with the highest utility. If there are multiple items with the same highest utility,
            one of them is returned randomly. Returns None if the input list is empty.
        """
        if not match_list:
            return None  # Return None if the input list is empty

        # Filter out items without the 'utility' key
        items_with_utility = [item for item in match_list if 'utility' in item]

        if not items_with_utility:
            return random.choice(match_list)  # Return a random choice from the original input list

        highest_utility = max(items_with_utility, key=lambda item: item['utility'])['utility']
        highest_utility_productions = [item for item in items_with_utility if item['utility'] == highest_utility]

        return random.choice(highest_utility_productions)



    @staticmethod
    # Enhanced buffer match evaluation function with diagnostics.
    def buffer_match_eval_diagnostic(buffer_dict, matching_dict, negation_dict, wildcard='*'):
        # Display diagnostic information
        #print(f"\nEvaluating buffer: {buffer_dict}")
        #print(f"Against matching criteria: {matching_dict} and negation criteria: {negation_dict}")

        # Initialize a dictionary to capture wildcard values
        wildcard_values = {}
        # Iterate over matching conditions
        for key, match_value in matching_dict.items():
            # Handle wildcard values
            if match_value == wildcard:
                #print(f"Wildcard for key: {key}, any value is acceptable.")
                wildcard_values[key] = buffer_dict.get(key, None)  # Capture the actual value from the buffer
                continue
            # Check for a match
            #print(f"Checking match for key: {key} with value: {match_value}")
            if key not in buffer_dict or buffer_dict[key] != match_value:
                #print("Match failed!")
                return False, {}
            #print("Match succeeded!")

        # Iterate over negation conditions
        for key, neg_value in negation_dict.items():
            # Check for negation
            #print(f"Checking negation for key: {key} with value: {neg_value}")
            if key in buffer_dict and buffer_dict[key] == neg_value:
                #print("Negation failed!")
                return False, {}
            #print("Negation succeeded!")

        #print("Buffer item passed all criteria.")
        # Return both the result and the captured wildcard values
        return True, wildcard_values

    @staticmethod
    # Function to match chunks in a buffer with given cues, considering diagnostics.
    def match_chunks_with_diagnostics(buffer, cue):
        matched_chunks_data = []  # Store matched chunks
        # Iterate over each buffer item
        for buffer_key, buffer_value in buffer.items():
            # print(f"\nProcessing buffer item: {buffer_key}")
            # Evaluate buffer item against matching and negation criteria
            match, wildcard_values = Utility.buffer_match_eval_diagnostic(buffer_value, cue['matches'], cue['negations'])
            if match:
                matched_chunk_data = buffer_value.copy()  # Copy matching chunk data
                matched_chunk_data.update(wildcard_values)  # Include wildcard values
                matched_chunks_data.append(matched_chunk_data)  # Add to the list of matched chunks
                #print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")

        # Select the best chunk based on utility
        best_chunk_data = Utility.find_max(matched_chunks_data)
        return best_chunk_data

    
