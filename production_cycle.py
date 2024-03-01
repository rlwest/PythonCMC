


from utility import Utility

class ProductionCycle: # This class runs the production cycle
    def __init__(self):
        self.pending_actions = []

    def match_productions(self, working_memory, AllProductionSystems):
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
                is_match_for_all_buffers = True
                for buffer_key in production['matches'].keys():
                    matches = production['matches'].get(buffer_key, {})
                    negations = production['negations'].get(buffer_key, {})
                    if not Utility.buffer_match_eval(working_memory.get(buffer_key, {}), matches, negations):
                        is_match_for_all_buffers = False
                        break

                if is_match_for_all_buffers:
                    grouped_matched_productions[prod_system_key].append(production)
                    print('PRODUCTION MATCHED')
                    print(f"Matched Production in {prod_system_key}: {production.get('report')}")

        return grouped_matched_productions


    def process_pending_actions(self, working_memory, AllProductionSystems, DelayResetValues):
        """
        Processes pending actions that are scheduled to be executed.
        Deals with the execution and management of actions that were previously scheduled and are now due

        This method iterates through the list of pending actions in reverse order,
        executing those that have completed their delay period and updating the delay
        for others.

        Args:
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            DelayResetValues (dict): Dictionary containing the original delays for each production system.
        """
        for i in range(len(self.pending_actions) - 1, -1, -1):
            prod_system_key, production, delay = self.pending_actions[i]
            
            # Check if the delay period is completed
            if delay <= 1:
                # Execute the action associated with the production
                production['action'](working_memory)
                report_info = production.get('report')
                print(f'[ACTION TAKEN] Executing action for production {production.get("report")}.')
                print(f'[REPORT] {report_info}')
                
                # Reset the delay for the production system to its original value
                AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]
                print(f'[INFO] Delay for production system {prod_system_key} reset to original value.')

                # Remove the action from pending actions
                del self.pending_actions[i]
            else:
                # If the delay is not yet completed, decrement it
                self.pending_actions[i] = (prod_system_key, production, delay - 1)
                print(f'[INFO] Delay for action in production {production.get("report")} decremented. Remaining delay: {delay - 1}')

    
        

    def filter_and_execute_productions(self, grouped_productions, working_memory, AllProductionSystems, DelayResetValues):
        """
        Selects the production with the highest utility matched production for each production system.
        Executes the selected production's action if there is no delay
        Manages action delays by scheduling them for future execution
        Resetting the production system delay for production systems that fired

        Args:
            grouped_productions (dict): A dictionary of matched productions grouped by production system.
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            DelayResetValues (dict): Dictionary containing the original delays for each production system.
        """
        for prod_system_key, productions in grouped_productions.items():
            highest_utility_production = Utility.find_max(productions)
            # Find the production with the highest utility in the current production system
            
            if highest_utility_production:
                # Reporting the selected production
                print(f"[INFO] Production System '{prod_system_key}' selected production: '{highest_utility_production.get('report')}'")

                # Execute the action associated with the selected production
                delay = highest_utility_production['action'](working_memory)

                if delay > 0:
                    # If the action has a delay, add it to the pending actions
                    self.pending_actions.append((prod_system_key, highest_utility_production, delay))
                    print(f"[INFO] Action from production '{highest_utility_production.get('report')}' has been scheduled with a delay of {delay} cycles.")
                else:
                    # If no delay, print the action report and reset the production system delay
                    report_info = highest_utility_production.get('report')
                    print('[ACTION TAKEN] ' + report_info)
                    AllProductionSystems[prod_system_key][1] = DelayResetValues[prod_system_key]
                    print(f"[INFO] Production System '{prod_system_key}' delay reset to its original value.")



    def execute_actions(self, working_memory, matched_productions, AllProductionSystems, DelayResetValues):
        """
        Executes actions based on matched productions.
        """

        # Process any actions that are pending from previous cycles
        print("[INFO] Processing pending actions.")
        self.process_pending_actions(working_memory, AllProductionSystems, DelayResetValues)

        # The matched_productions dictionary is already grouped by production system keys
        print("[INFO] Filtering and executing matched productions.")
        self.filter_and_execute_productions(matched_productions, working_memory, AllProductionSystems, DelayResetValues)


    def run_cycles(self, working_memory, AllProductionSystems, DelayResetValues, cycles=5, millisecpercycle=10):
        """
        Runs the production cycle for a specified number of cycles and milliseconds per cycle.

        Args:
            working_memory (dict): The current state of all buffers.
            AllProductionSystems (dict): Dictionary containing production systems and their current delays.
            DelayResetValues (dict): Dictionary containing the original delays for each production system.
            cycles (int): Number of cycles to run. Default is 5.
            millisecpercycle (int): Milliseconds per cycle. Default is 10.
        """
        for cycle_number in range(cycles):
            print(f'\nMilliseconds {(cycle_number + 1) * millisecpercycle} ---------------------------------------')
            matched_productions = self.match_productions(working_memory, AllProductionSystems)
            self.execute_actions(working_memory, matched_productions, AllProductionSystems, DelayResetValues)

