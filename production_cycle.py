class ProductionCycle:



    def match_productions(self, memories, AllProductionSystems):
        matched_productions = {}

        for prod_system_key, prod_system in AllProductionSystems.items():
            productions = prod_system[0]
            matched_productions[prod_system_key] = []

            for production in productions:
                matches = production['matches']
                negations = production['negations']

                match_found = True
                for memory_store, conditions in matches.items():
                    memory = memories.get(memory_store, {})
                    #print(f"Checking matches in {memory_store}: {memory}")
                    for buffer, slots in conditions.items():
                        for slot, value in slots.items():
                            actual_value = memory.get(buffer, {}).get(slot, None)
                            #print(f"Checking {memory_store} -> {buffer}.{slot} == {value}, actual: {actual_value}")
                            if actual_value != value:
                                match_found = False
                                #print(f"Match failed: {memory_store} -> {buffer}.{slot} (expected: {value}, actual: {actual_value})")
                                break
                        if not match_found:
                            break
                    if not match_found:
                        break

                if not match_found:
                    continue

                negation_found = False
                for memory_store, conditions in negations.items():
                    memory = memories.get(memory_store, {})
                    #print(f"Checking negations in {memory_store}: {memory}")
                    for buffer, slots in conditions.items():
                        for slot, value in slots.items():
                            actual_value = memory.get(buffer, {}).get(slot, None)
                            #print(f"Checking {memory_store} -> {buffer}.{slot} != {value}, actual: {actual_value}")
                            if actual_value == value:
                                negation_found = True
                                #print(f"Negation found: {memory_store} -> {buffer}.{slot} == {value}")
                                break
                        if negation_found:
                            break
                    if negation_found:
                        break

                if match_found and not negation_found:
                    matched_productions[prod_system_key].append(production)
                    print(f"Production matched: {production['report']}")

        return matched_productions

    def filter_and_execute_productions(self, matched_productions, memories, AllProductionSystems, DelayResetValues):
        for prod_system_key, productions in matched_productions.items():
            if productions and AllProductionSystems[prod_system_key][1] == 0:
                production = max(productions, key=lambda p: p['utility'])
                report_info = production['report']
                action = production['action']
                memory_type = AllProductionSystems[prod_system_key][2]
                memory = memories.get(memory_type, {})
                print(f"Executing action: {report_info} on {memory_type}")
                action(memory)
                print(f'[ACTION TAKEN] {report_info}')
                AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]  # Reset the delay
                print(f'Resetting delay for {prod_system_key} to {DelayResetValues[prod_system_key]}')
            else:
                AllProductionSystems[prod_system_key][1] -= 1  # Decrement the delay if not zero
                print(f'Decrementing delay for {prod_system_key} to {AllProductionSystems[prod_system_key][1]}')

    def run_cycles(self, memories, AllProductionSystems, DelayResetValues, cycles=5, millisecpercycle=10):
        for cycle_number in range(cycles):
            print(f'\nMilliseconds {(cycle_number + 1) * millisecpercycle} ---------------------------------------')
            matched_productions = self.match_productions(memories, AllProductionSystems)
            print(f'Matched productions: {matched_productions}')
            self.execute_actions(memories, matched_productions, AllProductionSystems, DelayResetValues)

    def execute_actions(self, memories, matched_productions, AllProductionSystems, DelayResetValues):
        self.filter_and_execute_productions(matched_productions, memories, AllProductionSystems, DelayResetValues)
