
import random

from utility import Utility
from production_cycle import ProductionCycle
from Cog_Functions import DMHandler


# Working Memory

working_memory = {
    'goalbuffer': {'goal': 'cat_name'}, 
    'dmIN_buffer': {'process': 'DMretrieve', 'animal': 'cat', 'colour': 'white'},
    'dmOUT_buffer': {}
}

# Other Memories

DM = {
    'chunk1': {'animal': 'cat', 'colour': 'brown', 'utility': 25},
    'chunk2': {'animal': 'cat', 'colour': 'white', 'name': 'whitney', 'utility': 30},
    'chunk3': {'animal': 'fish', 'colour': 'blue', 'utility': 15}
    }

# Cognitive Functions

global dm_handler_for_cats
dm_handler_for_cats = DMHandler(DM, 'dmIN_buffer', 'dmOUT_buffer')


# Main Production System

PS1_list = []
def request_name(working_memory):
    dm_handler_for_cats.process_request(working_memory)
    working_memory['goalbuffer']['goal'] = 'wait_for_name'
    return 0
PS1_list.append({
    'matches': {'goalbuffer': {'goal': 'cat_name'}},
    'negations': {},
    'utility': 10,
    'action': request_name,
    'report': "PS1-Production1"
})


def report_name(working_memory):
    print('##############name found#####################')
    return 0
PS1_list.append({
    'matches': {'dmOUT_buffer':{'animal':'cat','name':'*'}},
    'negations': {},
    'utility': 10,
    'action': report_name,
    'report': "PS1-Production1"
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


