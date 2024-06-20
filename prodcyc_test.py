import unittest
from production_cycle import ProductionCycle


class TestProductionCycle(unittest.TestCase):

    def setUp(self):
        self.pc = ProductionCycle()

        self.memories = {
            'working_memory': {'focusbuffer': {'focus': 'zero'}},
            'environment_memory': {'button1': {'state': 'up'}, 'button2': {'state': 'up'}, 'button3': {'state': 'up'}}
        }

        self.working_memory_productions = [
            {
                'matches': {'working_memory': {'focusbuffer': {'focus': 'zero'}}},
                'negations': {},
                'utility': 10,
                'action': lambda wm: wm.update({'focusbuffer': {'focus': 'one'}}),
                'report': 'count_0'
            },
            {
                'matches': {'working_memory': {'focusbuffer': {'focus': 'one'}}},
                'negations': {},
                'utility': 10,
                'action': lambda wm: wm.update({'focusbuffer': {'focus': 'two'}}),
                'report': 'count_1'
            }
        ]

        self.environment_memory_productions = [
            {
                'matches': {'working_memory': {'focusbuffer': {'focus': 'zero'}}},
                'negations': {},
                'utility': 10,
                'action': lambda em: em.update({'button1': {'state': 'down'}}),
                'report': 'button_1_down'
            },
            {
                'matches': {'working_memory': {'focusbuffer': {'focus': 'one'}}},
                'negations': {},
                'utility': 10,
                'action': lambda em: em.update({'button2': {'state': 'down'}}),
                'report': 'button_2_down'
            }
        ]

        self.AllProductionSystems = {
            'ProductionSystem1': [self.working_memory_productions, 0, 'working_memory'],
            'ProductionSystem2': [self.environment_memory_productions, 0, 'environment_memory']
        }

        self.DelayResetValues = {
            'ProductionSystem1': 5,
            'ProductionSystem2': 5
        }

    def test_match_productions(self):
        matched_productions = self.pc.match_productions(self.memories, self.AllProductionSystems)
        self.assertEqual(len(matched_productions['ProductionSystem1']), 1)
        self.assertEqual(len(matched_productions['ProductionSystem2']), 1)

    def test_filter_and_execute_productions(self):
        matched_productions = self.pc.match_productions(self.memories, self.AllProductionSystems)
        self.pc.filter_and_execute_productions(matched_productions, self.memories, self.AllProductionSystems,
                                               self.DelayResetValues)
        self.assertEqual(self.memories['working_memory']['focusbuffer']['focus'], 'one')
        self.assertEqual(self.memories['environment_memory']['button1']['state'], 'down')

    def test_run_cycles(self):
        self.pc.run_cycles(self.memories, self.AllProductionSystems, self.DelayResetValues, cycles=1,
                           millisecpercycle=10)
        self.assertEqual(self.memories['working_memory']['focusbuffer']['focus'], 'one')
        self.assertEqual(self.memories['environment_memory']['button1']['state'], 'down')


if __name__ == '__main__':
    unittest.main()
