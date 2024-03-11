
from utility import Utility





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
            print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")

    # Select the best chunk based on utility
    best_chunk_data = Utility.find_max(matched_chunks_data)
    return best_chunk_data



##class MemorySearcher:
##    def __init__(self, memory_system, parent_output_dict, output_key):
##        """
##        Initializes the MemorySearcher with a memory system and output location.
##        """
##        self.memory_system = memory_system
##        self.parent_output_dict = parent_output_dict
##        self.output_key = output_key
##
##    def search_and_populate(self, query):
##        """
##        Searches for entries matching the query, selecting the one with the highest utility.
##        Randomly selects among ties. Updates the parent_output_dict with the chosen entry.
##        """
##        # Adjust matching_entries comprehension to consider '*' as the wildcard.
##        matching_entries = [entry for key, entry in self.memory_system.items() if self.matches_query(query, entry)]
##
##        # Use the Utility.find_max function to select the entry with the highest utility.
##        chosen_entry = Utility.find_max(matching_entries)
##
##        # If a matching entry is found, store it in the specified output location.
##        if chosen_entry:
##            self.parent_output_dict[self.output_key] = chosen_entry
##
##    def matches_query(self, query, entry):
##        """
##        Checks if an entry matches the query criteria, treating '*' as the wildcard for any value.
##        """
##        for query_key, query_value in query.items():
##            # Here, '*' is treated as a wildcard, indicating any value is acceptable for that key.
##            if not Utility.check_match(query_key, query_value, entry, wildcard='*'):
##                return False
##        return True
##
##
##

#### test
##
##
### Mock memory system: a dictionary of dictionaries, each representing a pet.
##memory_system = {
##    'pet1': {'type': 'dog', 'name': 'Rover', 'color': 'brown', 'utility': 20},
##    'pet2': {'type': 'cat', 'name': 'Whiskers', 'color': 'black', 'utility': 15},
##    'pet3': {'type': 'dog', 'name': 'Spot', 'color': 'black', 'utility': 25},
##}
##
### Query: Updated to use '*' as the wildcard character.
### Looking for any 'dog' regardless of 'name', but we want to find its 'color'.
##query = {'type': 'dog', 'name': '*', 'color': '*'}
##
### Parent dictionary for output location, and the key under which results will be stored.
##parent_output_dict = {}
##output_key = 'search_results'
##
### Assuming MemorySearcher class is defined as previously discussed and available here.
##
### Instantiate MemorySearcher with the mock data and output location.
##searcher = MemorySearcher(memory_system, parent_output_dict, output_key)
##
### Perform the search.
##searcher.search_and_populate(query)
##
### The expected result is now the single best match, the dog with the highest utility.
##expected_result = {'type': 'dog', 'name': 'Spot', 'color': 'black', 'utility': 25}
##
### Test assertion: Check if the result matches the expected output.
##assert parent_output_dict[output_key] == expected_result, "The search result does not match the expected output."
##
##print("Test passed successfully.")
##

















## doesn't use utilities
##class MemorySearcher: 
##    def __init__(self, memory_system, output_location):
##        """
##        Initializes a new MemorySearcher instance with a specific memory system and output location.
##
##        :param memory_system: A list of dictionaries representing the memory system to search.
##        :param output_location: A dictionary where the search results are to be initially stored.
##        """
##        self.memory_system = memory_system
##        self.output_location = output_location
##
##    def search_and_populate(self, query):
##        """
##        Searches the memory system for entries matching the query criteria and populates
##        the output location with the results.
##
##        :param query: A dictionary with at least one key having a value of '?'. The '?'
##                      indicates a value that is to be found in the memory system.
##        """
##        # Initialize a list to store results temporarily.
##        search_results = []
##
##        # Iterate through each entry in the memory system.
##        for entry in self.memory_system:
##            match = True  # Assume a match until proven otherwise.
##            
##            # Check each key, value pair in the query.
##            for key, value in query.items():
##                if value != '?' and entry.get(key, None) != value:
##                    match = False
##                    break  # No need to check further keys for this entry.
##            
##            if match:
##                # If all non-'?' values match, prepare a result entry.
##                result_entry = entry.copy()  # Make a copy to avoid modifying the original entry.
##                for key in query:
##                    if query[key] == '?':
##                        result_entry[key] = entry.get(key, None)
##                search_results.append(result_entry)
##        
##        # Store the results in the specified output location.
##        self.output_location['results'] = search_results
##
##    def update_memory_system(self, new_memory_system):
##        """
##        Updates the memory system of the instance.
##
##        :param new_memory_system: The new memory system to be used for subsequent searches.
##        """
##        self.memory_system = new_memory_system
##
##    def update_output_location(self, new_output_location):
##        """
##        Updates the output location where search results are stored.
##
##        :param new_output_location: The new output location for storing search results.
##        """
##        self.output_location = new_output_location
##



##class DMHandler: # old version of the code above
##    def __init__(self, dm):
##        self.dm = dm  # Initialize with the DM data structure
##
##    def update_dm_buffer(self, working_memory):
##        # Get the current goal from the goalbuffer
##        current_goal = working_memory['goalbuffer']
##        
##        # Construct the cue for matching by copying the current goal and removing the 'process' key
##        matches = {k: v for k, v in current_goal.items() if k != 'process'}
##
##        # Construct the cue with 'matches' and 'negations'
##        cue = {
##            'matches': matches,
##            'negations': {}
##        }
##
##        # Update the 'process' slot of the goal buffer to 'DMrequested'
##        working_memory['goalbuffer']['process'] = 'DMrequested'
##        print(f"Updated goalbuffer's 'process' slot to 'DMrequested'.")
##
##
##        # Find the best chunk matching the cue
##        best_chunk_data = Utility.match_chunks_with_diagnostics(self.dm, cue)
##        
##        # Check if a valid chunk was found and then update DMbuffer
##        if best_chunk_data:
##            working_memory['DMbuffer'] = best_chunk_data
##            print(f"Updated DMbuffer with best chunk data: {best_chunk_data}")
##        else:
##            # No valid chunk was found, create a chunk with 'process': 'failed'
##            failed_chunk = {'process': 'failed'}
##            working_memory['DMbuffer'] = failed_chunk
##            print(f"No matching chunk found. Updated DMbuffer with failed chunk: {failed_chunk}")
##
##        return best_chunk_data
##
##
##
##
