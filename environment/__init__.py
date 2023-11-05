import random

class SimpleEnvironment:
    def __init__(self, board_size=10, apples_positions = None):
        self.board_size = board_size
        self.player_pos = [0, 0]  # Initial player position
        self.apples = []  # List to store apple positions
        self.generate_apples(apples_positions)  # Generate initial set of apples

    def generate_apples(self, apples_positions = None):
        # Generate 3 random apple positions on the board
        if(apples_positions is None):
            self.apples = [[random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)] for _ in range(3)]
        else: 
            self.apples = apples_positions

    def move_player(self, direction):
        # Define possible directions: bottom, bottom-right, right, etc.
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (0, 0)]  # Last one is no movement

        # Update player position based on the chosen direction
        new_pos = [sum(x) for x in zip(self.player_pos, directions[direction])]
        # Ensure the player stays within the board boundaries
        self.player_pos = [max(0, min(new_pos[0], self.board_size - 1)), max(0, min(new_pos[1], self.board_size - 1))]

        # Check if the player caught an apple
        for apple in self.apples:
            if apple == self.player_pos:
                self.apples.remove(apple)
                self.generate_apples()
                return 1  # Player caught an apple, return a reward of 1
        return 0  # No apple caught, return a reward of 0

    def get_state(self):
        # Return the current state of the environment (player position and apple positions)
        return [self.player_pos] + self.apples

    def is_game_over(self):
        # The game is over if there are no more apples on the board
        return len(self.apples) == 0
