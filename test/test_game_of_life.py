import pytest

from pycgol._model import Model
from pycgol._state import State


class TestGameOfLife:
    def test_neighbours_corner_cell(self):
        neighbours = Model._neighbours((0,0), 10, 10)
        assert set(neighbours) == set([(1, 0), (1, 1), (0, 1)])

    def test_neighbours_center_cell(self):
        neighbours = Model._neighbours((5, 5), 10, 10)
        expected = [
            (4, 4), (5, 4), (6, 4),
            (4, 5),         (6, 5),
            (4, 6), (5, 6), (6, 6)
        ]
        assert set(neighbours) == set(expected)
        assert len(neighbours) == 8

    def test_neighbours_edge_cell(self):
        # Test cell on edge but not corner
        neighbours = Model._neighbours((5, 0), 10, 10)
        expected = [
            (4, 0), (6, 0),
            (4, 1), (5, 1), (6, 1)
        ]
        assert set(neighbours) == set(expected)

    def test_neighbours_bottom_right_corner(self):
        neighbours = Model._neighbours((9, 9), 10, 10)
        expected = [(8, 8), (9, 8), (8, 9)]
        assert set(neighbours) == set(expected)

    def test_neighbours_invalid_coordinates(self):
        with pytest.raises(ValueError):
            Model._neighbours((10, 9), 10, 10)

        with pytest.raises(ValueError):
            Model._neighbours((9, 10), 10, 10)

        with pytest.raises(ValueError):
            Model._neighbours((-1, 5), 10, 10)

    def test_alive_neighbours_count(self):
        state = State(5, 5)
        # Set up a pattern: alive cell at (2,2) with some alive neighbours
        state[1, 1] = True  # top-left
        state[2, 1] = True  # top
        state[3, 2] = True  # right

        alive_count = Model._alive_neighbours((2, 2), state)
        assert alive_count == 3

    def test_alive_neighbours_no_neighbours(self):
        state = State(5, 5)
        # Cell with no alive neighbours
        alive_count = Model._alive_neighbours((2, 2), state)
        assert alive_count == 0

    def test_next_cell_state_underpopulation(self):
        """Any live cell with fewer than two live neighbours dies"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # one neighbour

        result = Model._next_cell_state((2, 2), state)
        assert result is False

    def test_next_cell_state_survival_two_neighbours(self):
        """Any live cell with two neighbours survives"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2

        result = Model._next_cell_state((2, 2), state)
        assert result is True

    def test_next_cell_state_survival_three_neighbours(self):
        """Any live cell with three neighbours survives"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2
        state[1, 3] = True  # neighbour 3

        result = Model._next_cell_state((2, 2), state)
        assert result is True

    def test_next_cell_state_overpopulation(self):
        """Any live cell with more than three live neighbours dies"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2
        state[1, 3] = True  # neighbour 3
        state[2, 1] = True  # neighbour 4

        result = Model._next_cell_state((2, 2), state)
        assert result is False

    def test_next_cell_state_reproduction(self):
        """Any dead cell with exactly three live neighbours becomes alive"""
        state = State(5, 5)
        state[2, 2] = False  # dead cell
        state[1, 1] = True   # neighbour 1
        state[1, 2] = True   # neighbour 2
        state[1, 3] = True   # neighbour 3

        result = Model._next_cell_state((2, 2), state)
        assert result is True

    def test_next_cell_state_dead_cell_insufficient_neighbours(self):
        """Dead cell with fewer than three neighbours stays dead"""
        state = State(5, 5)
        state[2, 2] = False  # dead cell
        state[1, 1] = True   # neighbour 1
        state[1, 2] = True   # neighbour 2

        result = Model._next_cell_state((2, 2), state)
        assert result is False

    def test_next_state_blinker_pattern(self):
        """Test the classic blinker pattern (oscillates between horizontal and vertical)"""
        # Initial horizontal blinker
        state = State(5, 5)
        state[1, 2] = True
        state[2, 2] = True
        state[3, 2] = True

        # After one generation, should become vertical
        next_state = Model.next_state(state)

        assert next_state[2, 1] is True
        assert next_state[2, 2] is True
        assert next_state[2, 3] is True
        assert next_state[1, 2] is False
        assert next_state[3, 2] is False

    def test_next_state_block_pattern(self):
        """Test the block pattern (still life - doesn't change)"""
        state = State(4, 4)
        state[1, 1] = True
        state[1, 2] = True
        state[2, 1] = True
        state[2, 2] = True

        next_state = Model.next_state(state)

        # Block should remain unchanged
        assert next_state[1, 1] is True
        assert next_state[1, 2] is True
        assert next_state[2, 1] is True
        assert next_state[2, 2] is True

    def test_next_state_empty_grid(self):
        """Test that empty grid stays empty"""
        state = State(5, 5)
        next_state = Model.next_state(state)

        for y in range(5):
            for x in range(5):
                assert next_state[x, y] is False

    def test_next_state_dimensions_preserved(self):
        """Test that the dimensions of the state are preserved"""
        state = State(7, 3)
        next_state = Model.next_state(state)

        assert next_state.width == 7
        assert next_state.height == 3
