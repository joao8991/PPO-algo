import random

class AppleEnvironment:
    def __init__(self, board_size=12, apples_positions = None):
        self.board_size = board_size
        self.player_pos = [0, 0]  # Initial player position
        self.apples = []  # List to store apple positions
        self.generate_apples(apples_positions)  # Generate initial set of apples

    def reset_state(self):
        self.player_pos = [0,0]  # Initial player position
        self.apples = []  # List to store apple positions
        self.generate_apples()  # Generate initial set of apples

    def distance_to_apple(self):
        if(len(self.apples) > 0):
            apple = self.apples[0]
            return pow(pow(self.player_pos[0]-apple[0],2)+pow(self.player_pos[1]-apple[1],2),0.5)
        return 0

    def generate_apples(self, apples_positions = None):
        # Generate 3 random apple positions on the board
        if(apples_positions is None):
            self.apples = [[random.randint(3, self.board_size - 1), random.randint(3, self.board_size - 1)] for _ in range(1)]
            # self.apples = [[9,9]]
        else: 
            self.apples = apples_positions

    def distance_from_closer_apple(self):
        max_distance = pow(pow(self.board_size,2)+pow(self.board_size,2),0.5)
        distances = []
        for apple in self.apples:
            apple_distance  = pow(pow(self.player_pos[0]-apple[0],2)+pow(self.player_pos[1]-apple[1],2),0.5)
            if apple_distance == 0:
                self.apples.remove(apple)
                # self.generate_apples()
                return 2
            else:
                distances.append(apple_distance) 
        if(len(distances) > 0):
            return 1-(min(distances)/max_distance)
        return 1
    
    def move_player(self, direction):
        # Define possible directions: bottom, bottom-right, right, etc.
        directions = [(1, 0), (0, 1), (-1, 0),  (0, -1)]  # Last one is no movement

        distance_from_apple_before = self.distance_from_closer_apple()
        # Update player position based on the chosen direction
        new_pos = [sum(x) for x in zip(self.player_pos, directions[direction])]
        # Ensure the player stays within the board boundaries
        fitness = 0
        if(new_pos[0] > self.board_size-1 or new_pos[0] < 0):
            fitness -= 1
        if(new_pos[1] > self.board_size-1 or new_pos[1] < 0):
            fitness -= 1
        self.player_pos = [max(0, min(new_pos[0], self.board_size - 1)), max(0, min(new_pos[1], self.board_size - 1))]

        gained_distance = (self.distance_from_closer_apple() - distance_from_apple_before)* 2
        # Check if the player caught an apple
        return gained_distance + fitness

    def get_state(self):
        # Return the current state of the environment (player position and apple positions)
        if(len(self.apples) > 0):
            state_array =  [self.player_pos] + self.apples + [[self.player_pos[0] - self.apples[0][0], self.player_pos[1] - self.apples[0][1]]]
        else:
            state_array =  [self.player_pos] + self.apples + [[0, 0]]
        reshaped_array = [num for sublist in state_array for num in sublist]
        return reshaped_array


    def is_game_over(self):
        # The game is over if there are no more apples on the board
        return len(self.apples) == 0
