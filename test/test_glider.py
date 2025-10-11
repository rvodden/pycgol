import pytest

from pycgol._state import State
from pycgol.objects._glider import Glider


class TestGlider:

    def test_glider_placement_valid_position(self):
        state = State(10, 10)
        result_state = Glider.place((3, 3), state)

        # Check that glider cells are set correctly
        expected_cells = [
            (3, 3), (4, 3), (5, 3),  # bottom row
            (5, 4),                   # middle right
            (4, 5)                    # top middle
        ]

        for x, y in expected_cells:
            assert result_state[x, y] is True

        # Check that other cells remain False
        for y in range(10):
            for x in range(10):
                if (x, y) not in expected_cells:
                    assert result_state[x, y] is False

    def test_glider_placement_returns_same_state_object(self):
        state = State(10, 10)
        result_state = Glider.place((3, 3), state)

        # Should return the same state object, not a copy
        assert result_state is state

    def test_glider_placement_near_boundary(self):
        state = State(10, 10)

        # Place glider near the boundary but still valid
        result_state = Glider.place((7, 7), state)

        # Only cells within bounds should be set
        expected_cells = [
            (7, 7), (8, 7), (9, 7),  # bottom row (all within bounds)
            (9, 8),                   # middle right (within bounds)
            (8, 9)                    # top middle (within bounds)
        ]

        for x, y in expected_cells:
            assert result_state[x, y] is True

    def test_glider_placement_partial_out_of_bounds(self):
        state = State(5, 5)

        # Place glider so some cells would be out of bounds
        result_state = Glider.place((3, 3), state)

        # Only cells within bounds should be set
        # Glider pattern at (3,3): (3,3), (4,3), (5,3), (5,4), (4,5)
        # But (5,3), (5,4), (4,5) are out of bounds in a 5x5 grid
        expected_cells = [
            (3, 3), (4, 3)   # Only these two cells are within bounds
        ]

        for x, y in expected_cells:
            assert result_state[x, y] is True

        # Verify that other cells remain False
        for y in range(5):
            for x in range(5):
                if (x, y) not in expected_cells:
                    assert result_state[x, y] is False

    def test_glider_placement_completely_out_of_bounds(self):
        state = State(5, 5)

        # Place glider completely out of bounds
        result_state = Glider.place((10, 10), state)

        # No cells should be set since all glider cells would be out of bounds
        for y in range(5):
            for x in range(5):
                assert result_state[x, y] is False

    def test_glider_placement_at_origin(self):
        state = State(10, 10)
        result_state = Glider.place((0, 0), state)

        expected_cells = [
            (0, 0), (1, 0), (2, 0),  # bottom row
            (2, 1),                   # middle right
            (1, 2)                    # top middle
        ]

        for x, y in expected_cells:
            assert result_state[x, y] is True

    def test_glider_cells_constant(self):
        # Test that the _CELLS constant has the correct glider pattern
        expected_pattern = [
            (0, 0), (1, 0), (2, 0),
            (2, 1),
            (1, 2)
        ]

        assert set(Glider._CELLS) == set(expected_pattern)

    def test_multiple_glider_placements(self):
        state = State(15, 15)

        # Place two gliders
        Glider.place((1, 1), state)
        Glider.place((8, 8), state)

        # Check first glider
        first_glider_cells = [(1, 1), (2, 1), (3, 1), (3, 2), (2, 3)]
        for x, y in first_glider_cells:
            assert state[x, y] is True

        # Check second glider
        second_glider_cells = [(8, 8), (9, 8), (10, 8), (10, 9), (9, 10)]
        for x, y in second_glider_cells:
            assert state[x, y] is True

    def test_glider_placement_edge_cases(self):
        # Test very small grid
        state = State(3, 3)
        result_state = Glider.place((0, 0), state)

        # Should place what fits
        expected_cells = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)]
        for x, y in expected_cells:
            assert result_state[x, y] is True