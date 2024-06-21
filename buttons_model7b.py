from utility import Utility
from production_cycle import ProductionCycle

working_memory = {'focusbuffer': {'focus': 'zero'},'motorbuffer': {'do': 'nothing'}}
environment_memory = {'button1': {'state': 'up'}, 'button2': {'state': 'up'}, 'button3': {'state': 'up'}}
memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory
}

ProceduralProductions = []

def count_0(working_memory):
    print("Executing count_0")
    working_memory['focusbuffer']['focus'] = 'one'
    print(f"Updated working_memory: {working_memory}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'focus': 'zero'}}},
    'negations': {},
    'utility': 10,
    'action': count_0,
    'report': "count_0"
})

def count_1(working_memory):
    print("Executing count_1")
    working_memory['focusbuffer']['focus'] = 'two'
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'focus': 'one'}}},
    'negations': {},
    'utility': 10,
    'action': count_1,
    'report': "count_1"
})

def count_2(working_memory):
    print("Executing count_2")
    working_memory['focusbuffer']['focus'] = 'three'
    print(f"Updated working_memory: {working_memory}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'focus': 'two'}}},
    'negations': {},
    'utility': 10,
    'action': count_2,
    'report': "count_2"
})

MotorProductions = []

def button_1(environment_memory):
    environment_memory['button1']['state'] = 'down'
    print(f"Updated environment_memory: {environment_memory}")
MotorProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'focus': 'zero'}}},
    'negations': {},
    'utility': 10,
    'action': button_1,
    'report': "action - button1:state=down"
})

def button_2(environment_memory):
    print("Executing button_2")
    environment_memory['button2']['state'] = 'down'
MotorProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'focus': 'one'}}},
    'negations': {},
    'utility': 10,
    'action': button_2,
    'report': "action - button2:state=down"
})

def button_3(environment_memory):
    print("Executing button_3")
    environment_memory['button3']['state'] = 'down'
    print(f"Updated environment_memory: {environment_memory}")
MotorProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'focus': 'two'}}},
    'negations': {},
    'utility': 10,
    'action': button_3,
    'report': "action - button3:state=down"
})

# production system delays in ticks
ProductionSystem1_Countdown = 0
ProductionSystem2_Countdown = 0

# stores the number of cycles for a production system to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown
}

# dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown, 'working_memory'],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown, 'environment_memory']
}

# Initialize ProductionCycle
ps = ProductionCycle()
# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=5, millisecpercycle=10)
