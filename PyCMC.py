
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
            one of them is returned randomly. Returns None if the list is empty or no items have a utility value.
        """
        highest_utility = float('-inf')
        highest_utility_productions = []
        for item in match_list:
            utility = item.get('utility', float('-inf'))  # Retrieve the utility of the production.
            if utility > highest_utility:
                highest_utility = utility
                highest_utility_productions = [item]
            elif utility == highest_utility:
                highest_utility_productions.append(item)
        # Randomly choose one production if there are multiple productions with the highest utility.
        return random.choice(highest_utility_productions) if highest_utility_productions else None

    @staticmethod
    # Enhanced buffer match evaluation function with diagnostics.
    def buffer_match_eval_diagnostic(buffer_dict, matching_dict, negation_dict, wildcard='*'):
        # Display diagnostic information
        print(f"\nEvaluating buffer: {buffer_dict}")
        print(f"Against matching criteria: {matching_dict} and negation criteria: {negation_dict}")

        # Initialize a dictionary to capture wildcard values
        wildcard_values = {}
        # Iterate over matching conditions
        for key, match_value in matching_dict.items():
            # Handle wildcard values
            if match_value == wildcard:
                print(f"Wildcard for key: {key}, any value is acceptable.")
                wildcard_values[key] = buffer_dict.get(key, None)  # Capture the actual value from the buffer
                continue
            # Check for a match
            print(f"Checking match for key: {key} with value: {match_value}")
            if key not in buffer_dict or buffer_dict[key] != match_value:
                print("Match failed!")
                return False, {}
            print("Match succeeded!")

        # Iterate over negation conditions
        for key, neg_value in negation_dict.items():
            # Check for negation
            print(f"Checking negation for key: {key} with value: {neg_value}")
            if key in buffer_dict and buffer_dict[key] == neg_value:
                print("Negation failed!")
                return False, {}
            print("Negation succeeded!")

        print("Buffer item passed all criteria.")
        # Return both the result and the captured wildcard values
        return True, wildcard_values

    @staticmethod
    # Function to match chunks in a buffer with given cues, considering diagnostics.
    def match_chunks_with_diagnostics(buffer, cue):
        matched_chunks_data = []  # Store matched chunks
        # Iterate over each buffer item
        for buffer_key, buffer_value in buffer.items():
            print(f"\nProcessing buffer item: {buffer_key}")
            # Evaluate buffer item against matching and negation criteria
            match, wildcard_values = Utility.buffer_match_eval_diagnostic(buffer_value, cue['matches'], cue['negations'])
            if match:
                matched_chunk_data = buffer_value.copy()  # Copy matching chunk data
                matched_chunk_data.update(wildcard_values)  # Include wildcard values
                matched_chunks_data.append(matched_chunk_data)  # Add to the list of matched chunks
                print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")

        # Select the best chunk based on utility
        best_chunk_data = Utility.find_max(matched_chunks_data)
        return best_chunk_data

    @staticmethod
    def delete_chunk_from_dict(dictionary, chunk_key):
        """
        Deletes a chunk from a given dictionary based on the provided chunk key.

        Args:
            dictionary (dict): The dictionary from which the chunk will be deleted.
            chunk_key (str): The key of the chunk to be deleted.

        Returns:
            bool: True if the chunk was successfully deleted, False if the chunk was not found.
        """
        if chunk_key in dictionary:
            del dictionary[chunk_key]
            print(f"Chunk '{chunk_key}' deleted from the dictionary.")
            return True
        else:
            print(f"Chunk '{chunk_key}' not found in the dictionary.")
            return False


class ProductionCycle: # This class runs the production cycle
    def __init__(self):
        self.pending_actions = []

    def match_productions(self, working_memory, AllProductionSystems):
        """Finds and groups matched productions."""
        grouped_matched_productions = {key: [] for key in AllProductionSystems}

        for prod_system_key, prod_system_value in AllProductionSystems.items():
            if prod_system_value[1] > 0:
                prod_system_value[1] -= 1

            prod_system = prod_system_value[0]
            delay = prod_system_value[1]

            if delay > 0:
                continue

            for production in prod_system:
                is_match_for_all_buffers = True
                for buffer_key in production['matches'].keys():
                    matches = production['matches'].get(buffer_key, {})
                    negations = production['negations'].get(buffer_key, {})
                    if not Utility.buffer_match_eval(working_memory.get(buffer_key, {}), matches, negations):
                        is_match_for_all_buffers = False
                        break

                if is_match_for_all_buffers:
                    grouped_matched_productions[prod_system_key].append(production)
                    print('PRODUCTION MATCHED')
                    print(f"Matched Production in {prod_system_key}: {production.get('report')}")

        return grouped_matched_productions


    def process_pending_actions(self, working_memory, AllProductionSystems, DelayResetValues):
        """
        Processes pending actions that are scheduled to be executed.
        Deals with the execution and management of actions that were previously scheduled and are now due

        This method iterates through the list of pending actions in reverse order,
        executing those that have completed their delay period and updating the delay
        for others.

        Args:
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            DelayResetValues (dict): Dictionary containing the original delays for each production system.
        """
        for i in range(len(self.pending_actions) - 1, -1, -1):
            prod_system_key, production, delay = self.pending_actions[i]
            
            # Check if the delay period is completed
            if delay <= 1:
                # Execute the action associated with the production
                production['action'](working_memory)
                report_info = production.get('report')
                print(f'[ACTION TAKEN] Executing action for production {production.get("report")}.')
                print(f'[REPORT] {report_info}')
                
                # Reset the delay for the production system to its original value
                AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]
                print(f'[INFO] Delay for production system {prod_system_key} reset to original value.')

                # Remove the action from pending actions
                del self.pending_actions[i]
            else:
                # If the delay is not yet completed, decrement it
                self.pending_actions[i] = (prod_system_key, production, delay - 1)
                print(f'[INFO] Delay for action in production {production.get("report")} decremented. Remaining delay: {delay - 1}')

    
        

    def filter_and_execute_productions(self, grouped_productions, working_memory, AllProductionSystems, DelayResetValues):
        """
        Selects the production with the highest utility matched production for each production system.
        Executes the selected production's action if there is no delay
        Manages action delays by scheduling them for future execution
        Resetting the production system delay for production systems that fired

        Args:
            grouped_productions (dict): A dictionary of matched productions grouped by production system.
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            DelayResetValues (dict): Dictionary containing the original delays for each production system.
        """
        for prod_system_key, productions in grouped_productions.items():
            highest_utility_production = Utility.find_max(productions)
            # Find the production with the highest utility in the current production system
            
            if highest_utility_production:
                # Reporting the selected production
                print(f"[INFO] Production System '{prod_system_key}' selected production: '{highest_utility_production.get('report')}'")

                # Execute the action associated with the selected production
                delay = highest_utility_production['action'](working_memory)

                if delay > 0:
                    # If the action has a delay, add it to the pending actions
                    self.pending_actions.append((prod_system_key, highest_utility_production, delay))
                    print(f"[INFO] Action from production '{highest_utility_production.get('report')}' has been scheduled with a delay of {delay} cycles.")
                else:
                    # If no delay, print the action report and reset the production system delay
                    report_info = highest_utility_production.get('report')
                    print('[ACTION TAKEN] ' + report_info)
                    AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]
                    print(f"[INFO] Production System '{prod_system_key}' delay reset to its original value.")



    def execute_actions(self, working_memory, matched_productions, AllProductionSystems, DelayResetValues):
        """
        Executes actions based on matched productions.
        """

        # Process any actions that are pending from previous cycles
        print("[INFO] Processing pending actions.")
        self.process_pending_actions(working_memory, AllProductionSystems, DelayResetValues)

        # The matched_productions dictionary is already grouped by production system keys
        print("[INFO] Filtering and executing matched productions.")
        self.filter_and_execute_productions(matched_productions, working_memory, AllProductionSystems, DelayResetValues)




##### test set ###################################################

### Production System 1 - PS1

PS1_list = []


def action_test_ProductionSystem1(working_memory):
    working_memory['buffer2']['test'] = 'two'
    working_memory['buffer1']['animal'] = working_memory['buffer2']['number']
##### match chunk  
    cue = {
    'matches': {'animal': 'cat', 'colour': '*', 'name': '*'},
    'negations': {}
}
    BufferName = DM
    best_chunk_data = Utility.match_chunks_with_diagnostics(BufferName, cue)



def action_test_ProductionSystem1(working_memory):
    # Existing logic
    working_memory['buffer2']['test'] = 'two'
    working_memory['buffer1']['animal'] = working_memory['buffer2']['number']
    
    # Diagnostic match to find the best chunk
    cue = {
        'matches': {'animal': 'cat', 'colour': '*', 'name': '*'},
        'negations': {}
    }
    BufferName = DM
    best_chunk_data = Utility.match_chunks_with_diagnostics(BufferName, cue)
    
    # Check if a valid chunk was found and then update buffer2
    if best_chunk_data:
        working_memory['buffer2'] = best_chunk_data
        print(f"Updated buffer2 with best chunk data: {best_chunk_data}")
    
    return 0

PS1_list.append({
    'matches': {'buffer1': {'animal': 'cat', 'colour': 'brown'}, 'buffer2': {'test': 'one'}},
    'negations': {},
    'utility': 10,
    'action': action_test_ProductionSystem1,
    'report': "PS1-Production1"
})





def action_test_ProductionSystem2(working_memory):
    working_memory['buffer2']['test'] = 'three'
    working_memory['buffer2']['number'] = working_memory['buffer2']['number'] + 2
    return 2
PS1_list.append({
    'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'two'}},
    'negations': {},
    'utility': 20,
    'action': action_test_ProductionSystem2,
    'report': 'PS1-Production2'
})


def action_test_production3(working_memory):
    working_memory['buffer2']['test'] = 'four'
    A = 2 + 2
    working_memory['buffer2']['number'] = A
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'three'}},
    'negations': {'buffer1': {'animal': 'dog'}, 'buffer2': {}},
    'utility': 30,
    'action': action_test_production3,
    'report': 'PS1-Production3'
})


def action_test_production4(working_memory):
    working_memory['buffer2']['test'] = 'five'
    return 3
PS1_list.append({
    'matches': {'buffer1': {'animal': '*'}, 'buffer2': {'test': 'four'}},
    'negations': {'buffer1': {'animal': 'dog'}},
    'utility': 40,
    'action': action_test_production4,
    'report': 'PS1-Production4'
})


def action_test_production5(working_memory):
    working_memory['buffer2']['test'] = 'siProductionSystem1_Countdown'
    working_memory['buffer3']['fruit'] = 'apple'
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'five'}},
    'negations': {},
    'utility': 10,
    'action': action_test_production5,
    'report': 'PS1-Production5'
})


def action_test_production6(working_memory):
    working_memory['buffer2']['test'] = 'seven'
    working_memory['buffer1']['animal'] = 'dog'
    working_memory['buffer1']['colour'] = 'golden'
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'siProductionSystem1_Countdown'}, 'buffer3': {'fruit': 'apple'}},
    'negations': {},
    'utility': 10,
    'action': action_test_production6,
    'report': 'PS1-Production6'
})


def action_test_production6b(working_memory):
    working_memory['buffer2']['test'] = 'seven'
    working_memory['buffer1']['animal'] = 'rat'
    working_memory['buffer1']['colour'] = 'blue'
    return 0
PS1_list.append({
    'matches': {'buffer2': {'test': 'siProductionSystem1_Countdown'}, 'buffer3': {'fruit': 'apple'}},
    'negations': {},
    'utility': 10,
    'action': action_test_production6b,
    'report': 'PS1-Production6b'
})


### Production System 2 - PS2

PS2_list = []


def action_test_ProductionSystem2a(working_memory):
    working_memory['buffer4']['fish'] = 'salmon'
    return 0
PS2_list.append({
    'matches': {'buffer2': {'fish': 'tuna'}},
    'negations': {},
    'utility': 10,
    'action': action_test_ProductionSystem2a,
    'report': "ProductionSystem2a"
})


def action_test_ProductionSystem2b(working_memory):
    working_memory['buffer4']['fish'] = 'shark'
    return 3
PS2_list.append({
    'matches': {'buffer2': {'animal': 'cat'}},
    'negations': {},
    'utility': 10,
    'action': action_test_ProductionSystem2b,
    'report': "ProductionSystem2b - matched to animal cat in buffer 2"
})



# working memory - dictionary of all buffers

working_memory = {
    'buffer1': {'animal': 'cat', 'colour': 'brown'}, 
    'buffer2': {'test': 'one', 'number': 5}, 
    'buffer3': {'fruit': 'pear'}, 
    'buffer4': {'fish': 'tuna'}
}

DM = {
    'chunk1': {'animal': 'cat', 'colour': 'brown', 'utility': 25},
    'chunk2': {'animal': 'cat', 'colour': 'white', 'name': 'whitney', 'utility': 30},
    'chunk3': {'animal': 'fish', 'colour': 'blue', 'utility': 15}
    }

# production system delays in ticks
ProductionSystem1_Countdown=1
ProductionSystem2_Countdown=2

# stores the number of cycles for a production system to fire
# so it can be reset after firing
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown}

ProductionSystem1_Countdown = ProductionSystem1_Countdown
ProductionSystem2_Countdown = ProductionSystem2_Countdown

# dictionary of all production systems and delays
AllProductionSystems = {'ProductionSystem1': [PS1_list, ProductionSystem1_Countdown],
                        'ProductionSystem2': [PS2_list, ProductionSystem2_Countdown]}



##### run the cycle #################################################################

# timing for tick system
cycles = 20
millisecpercycle = 10

# run ProductionCycle in tick cycles
ps = ProductionCycle()
for cycle_number in range(cycles):
    print()
    print('Milliseconds', (cycle_number+1) * millisecpercycle, '---------------------------------------')
    matched_productions = ps.match_productions(working_memory, AllProductionSystems)  # Call as a method of the instance
    ps.execute_actions(working_memory, matched_productions, AllProductionSystems, DelayResetValues)
