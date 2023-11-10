def divide_elements(array, divisor):
    result = []
    for element in array:
        result.append(element / divisor)
    return result

def calc_weighted_moving_average(time_constant, initial_constant, array):
        calculated_value = initial_constant

        calculated_array = []

        for tss in array:
            calc_yesterday = calculated_value

            calc_today = calc_yesterday + (tss - calc_yesterday) * (
                1 / time_constant
            )

            calculated_array.append(calc_today)

            calculated_value = calc_today
        return calculated_array

class RunningEnvironment:
    def __init__(self, changeble_days = 28, initial_fitness = 0, initial_fatigue = 0):
        self.changeble_days = changeble_days
        self.initial_fitness = initial_fitness
        self.initial_fatigue = initial_fatigue

        self.tss = [0 for _ in range(changeble_days)]

        self.step = 0

    def reset_state(self):
        pass

    def calculate_fitness(self):
        return calc_weighted_moving_average(42, self.initial_fitness, self.tss)
    
    def calculate_fatigue(self):
        return calc_weighted_moving_average(7, self.initial_fatigue, self.tss)


    def act(self, choice):
        # Define possible directions: bottom, bottom-right, right, etc.
        actions = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]  # Last one is no movement

        running_fitness_before = sum(self.calculate_fitness())
        self.tss[self.step] = actions[choice]
        self.step += 1
        if(self.step > 27):
            self.step = 0

        running_fitness_after = sum(self.calculate_fitness())
        # Ensure the player stays within the board boundaries
        fitness = running_fitness_after - running_fitness_before
        # Check if the player caught an apple
        return fitness

    def get_state(self):
        # Return the current state of the environment
        calculated_fitness = self.calculate_fitness()
        state_array = divide_elements(self.tss + calculated_fitness + self.calculate_fatigue(), 150)

        return state_array + [self.step/self.changeble_days] , calculated_fitness[-1]


    def is_game_over(self):
        return False
