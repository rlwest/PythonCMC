from utility import Utility

class DMHandler:
    def __init__(self, dm, in_buffer_name, out_buffer_name):
        self.dm = dm
        self.in_buffer_name = in_buffer_name
        self.out_buffer_name = out_buffer_name


    def process_request(self, working_memory):
        request_details = working_memory[self.in_buffer_name]
        cue = {
            'matches': {k: v for k, v in request_details.items() if k != 'process'},
            'negations': {}
        }

        # Capture the single return value directly
        best_chunk_data = Utility.match_chunks_with_diagnostics(self.dm, cue)
        
        if best_chunk_data:
            working_memory[self.out_buffer_name] = best_chunk_data
            print(f"Updated {self.out_buffer_name} with: {best_chunk_data}")
        else:
            working_memory[self.out_buffer_name] = {'process': 'failed'}
            print(f"No matching chunk found. Updated {self.out_buffer_name} with failure status.")

