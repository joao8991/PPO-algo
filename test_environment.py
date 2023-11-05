import pytest
from environment import SimpleEnvironment

@pytest.fixture
def environment():
    return SimpleEnvironment(apples_positions=[[0,1], [4,2], [8,8]])

def test_initial_state(environment):
    assert environment.player_pos == [0, 0]
    assert len(environment.apples) == 3

def test_move_player(environment):
    assert environment.move_player(0) == 0  # Move bottom (no apple caught)
    assert environment.move_player(1) == 0  # Move bottom-right (no apple caught)
    assert environment.move_player(2) == 0  # Move right (no apple caught)
    assert environment.move_player(3) == 0  # Move top-right (no apple caught)
    assert environment.move_player(4) == 0  # Move top (no apple caught)
    assert environment.move_player(5) == 0  # Move top-left (no apple caught)
    assert environment.move_player(6) == 1  # Move left (no apple caught)
    assert environment.move_player(7) == 0  # Move bottom-left (no apple caught)
    assert environment.move_player(8) == 0  # Stay (caught an apple)
    assert len(environment.apples) == 3  # There should be 3 apples after catching one

def test_get_state(environment):
    state = environment.get_state()
    assert len(state) == 4  # Player position + 3 apple positions

def test_game_over(environment):
    assert not environment.is_game_over()  # Game is not over initially
    environment.apples = []  # Remove all apples
    assert environment.is_game_over()  # Game is over when there are no apples
