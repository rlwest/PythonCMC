"""
this program runs one production system and counts from zero to two
"""

from utility import Utility
from production_cycle import ProductionCycle

working_memory = {'focusbuffer': {'focus': 'zero'}}

ProceduralProductions = []

def count_0(working_memory):
    working_memory['focusbuffer']['focus'] = 'one'
    return 0
ProceduralProductions.append({
    'matches': {'focusbuffer': {'focus': 'zero'}},
    'negations': {},
    'utility': 10,
    'action': count_0,
    'report': "count_0"
})

def count_1(working_memory):
    working_memory['focusbuffer']['focus'] = 'two'
    return 0
ProceduralProductions.append({
    'matches': {'focusbuffer': {'focus': 'one'}},
    'negations': {},
    'utility': 10,
    'action': count_1,
    'report': "count_1"
})

def count_2(working_memory):
    working_memory['focusbuffer']['focus'] = 'three'
    return 0
ProceduralProductions.append({
    'matches': {'focusbuffer': {'focus': 'two'}},
    'negations': {},
    'utility': 10,
    'action': count_2,
    'report': "count_2"
})



# production system delays in ticks
ProductionSystem1_Countdown=5

# stores the number of cycles for a production system to fire and reset
DelayResetValues = {'ProductionSystem1': ProductionSystem1_Countdown}

# dictionary of all production systems and delays
AllProductionSystems = {'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown]}



##### run the cycle #################################################################

# Initialize ProductionCycle
ps = ProductionCycle()
# Run the cycle with custom parameters
ps.run_cycles(working_memory, AllProductionSystems, DelayResetValues, cycles=20, millisecpercycle=10)


