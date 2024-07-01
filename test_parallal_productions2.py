from utility import Utility
from production_cycle import ProductionCycle

### works - the first productions in both production systems fire off of both memories

working_memory = {'focusbuffer': {'state': 'a'}}
environment_memory = {'button1': {'state': '1'}}
memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory
}

ProceduralProductions = []

def pp1(memories):
    memories['working_memory']['focusbuffer']['state'] = 'b'
    print(f"pp1 executed. Updated working_memory: {memories['working_memory']}")

ProceduralProductions.append({
    'matches': {'environment_memory': {'button1': {'state': '1'}},'working_memory': {'focusbuffer': {'state': 'a'}}},
    'negations': {},
    'utility': 10,
    'action': pp1,
    'report': "match to focusbuffer, change state from a to b"
})

def pp2(memories):
    memories['working_memory']['focusbuffer']['state'] = '*'
    print(f"pp2 executed. Updated working_memory: {memories['working_memory']}")

ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'b'}}},
    'negations': {},
    'utility': 10,
    'action': pp2,
    'report': "match to focusbuffer, change state from b to *"
})

MotorProductions = []

def mp1(memories):
    memories['environment_memory']['button1']['state'] = '2'
    print(f"mp1 executed. Updated environment_memory: {memories['environment_memory']}")

MotorProductions.append({
    'matches': {'environment_memory': {'button1': {'state': '1'}},'working_memory': {'focusbuffer': {'state': 'a'}}},
    'negations': {},
    'utility': 10,
    'action': mp1,
    'report': "match to button1, change state from 1 to 2"
})

def mp2(memories):
    memories['environment_memory']['button1']['state'] = '*'
    print(f"mp2 executed. Updated environment_memory: {memories['environment_memory']}")

MotorProductions.append({
    'matches': {'environment_memory': {'button1': {'state': '2'}}},
    'negations': {},
    'utility': 10,
    'action': mp2,
    'report': "match to button1, change state from 2 to *"
})

# Production system delays in ticks
ProductionSystem1_Countdown = 1
ProductionSystem2_Countdown = 1

# Stores the number of cycles for a production system to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown
}

# Dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown]
}

# Initialize ProductionCycle
ps = ProductionCycle()

# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=10, millisecpercycle=10)
