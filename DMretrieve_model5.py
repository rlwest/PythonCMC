
import random

from utility import Utility
from Cognitive_Functions import match_chunks_with_diagnostics
from production_cycle import ProductionCycle


# Working Memory

working_memory = {
    'goalbuffer': {'goal': 'dog'}, 
    'dmIN_buffer': {},
    'dmOUT_buffer': {}
}

# Other Memories

memory_system = {
    'chunk1': {'type': 'task', 'status': 'complete', 'utility': 5},
    'chunk2': {'type': 'task', 'status': 'incomplete', 'utility': 8},
    'chunk3': {'type': 'event', 'status': 'upcoming', 'utility': 3}
}


# Main Production System

PS1_list = []
def request_dm(working_memory):
    buffer = memory_system
    cue = {'matches': {'type': 'task'}, 'negations': {'status': 'complete'}}
    
    # Capture the return value of match_chunks_with_diagnostics
    best_chunk_data = match_chunks_with_diagnostics(buffer, cue)
    
    # Now you can use best_chunk_data in the rest of your function
    print("Retrieved best chunk data:", best_chunk_data)
    
    # Update the goal to reflect the new state
    working_memory['goalbuffer']['goal'] = 'wait'
    print("Current goal in the goalbuffer:", working_memory['goalbuffer']['goal'])

    return 2
PS1_list.append({
    'matches': {'goalbuffer': {'goal': 'dog'}},
    'negations': {},
    'utility': 10,
    'action': request_dm,
    'report': "PS1-Production1"
})

def report_name(working_memory):
    return 0
PS1_list.append({
    'matches': {'goalbuffer': {'goal': 'wait'}},
    'negations': {},
    'utility': 10,
    'action': report_name,
    'report': "PS1-Production2"
})

PS2_list = []



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

# Initialize ProductionCycle
ps = ProductionCycle()
# Run the cycle with custom parameters
ps.run_cycles(working_memory, AllProductionSystems, DelayResetValues, cycles=10, millisecpercycle=20)


