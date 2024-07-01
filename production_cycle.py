from utility import Utility


class ProductionCycle:
    def __init__(self):
        self.pending_actions = []

    def match_productions(self, memories, AllProductionSystems):
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
                is_match_for_all_conditions = True

                for memory_system_key, buffer_conditions in production['matches'].items():
                    for buffer_key, match_criteria in buffer_conditions.items():
                        if memory_system_key in memories and buffer_key in memories[memory_system_key]:
                            memory_content = memories[memory_system_key][buffer_key]
                            print(f"Checking production {production.get('report')} in {prod_system_key}")
                            print(f"Memory system: {memory_system_key}, Buffer key: {buffer_key}")
                            print(f"Memory content: {memory_content}")
                            print(f"Matches: {match_criteria}")
                            print(
                                f"Negations: {production['negations'].get(memory_system_key, {}).get(buffer_key, {})}")

                            if not Utility.buffer_match_eval(
                                    memory_content,
                                    match_criteria,
                                    production['negations'].get(memory_system_key, {}).get(buffer_key, {})
                            ):
                                print(f"Buffer {buffer_key} did not match in memory system {memory_system_key}")
                                is_match_for_all_conditions = False
                                break
                        else:
                            print(f"Buffer key {buffer_key} not found in memory system {memory_system_key}")
                            is_match_for_all_conditions = False
                            break
                    if not is_match_for_all_conditions:
                        break

                if is_match_for_all_conditions:
                    grouped_matched_productions[prod_system_key].append(production)
                    print(f"Matched Production in {prod_system_key}: {production.get('report')}")

        return grouped_matched_productions

    def process_pending_actions(self, memories, AllProductionSystems, DelayResetValues):
        for i in range(len(self.pending_actions) - 1, -1, -1):
            prod_system_key, production, delay = self.pending_actions[i]

            if delay <= 1:
                production['action'](memories)
                report_info = production.get('report')
                print(f'[ACTION TAKEN] Execute action for production {production.get("report")}.')

                AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]
                del self.pending_actions[i]
            else:
                self.pending_actions[i] = (prod_system_key, production, delay - 1)

    def filter_and_execute_productions(self, grouped_productions, memories, AllProductionSystems, DelayResetValues):
        for prod_system_key, productions in grouped_productions.items():
            highest_utility_production = Utility.find_max(productions)
            if highest_utility_production:
                highest_utility_production['action'](memories)
                report_info = highest_utility_production.get('report')
                print(f'[ACTION TAKEN] {report_info}')
                AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]

    def execute_actions(self, memories, matched_productions, AllProductionSystems, DelayResetValues):
        self.process_pending_actions(memories, AllProductionSystems, DelayResetValues)
        self.filter_and_execute_productions(matched_productions, memories, AllProductionSystems, DelayResetValues)

    def run_cycles(self, memories, AllProductionSystems, DelayResetValues, cycles=5, millisecpercycle=10):
        for cycle_number in range(cycles):
            print(f'\nMilliseconds {(cycle_number + 1) * millisecpercycle} ---------------------------------------')
            matched_productions = self.match_productions(memories, AllProductionSystems)
            print(f'Matched productions: {matched_productions}')
            self.execute_actions(memories, matched_productions, AllProductionSystems, DelayResetValues)
            for prod_system_key, prod_system_value in AllProductionSystems.items():
                print(f'Decrementing delay for {prod_system_key} to {prod_system_value[1]}')
