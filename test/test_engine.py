import pytest

from pycgol.engines import LoopEngine, NumpyEngine
from pycgol._state import State


class TestLoopEngine:
    """Test the original nested loop implementation."""

    def test_neighbours_corner_cell(self):
        neighbours = LoopEngine._neighbours((0, 0), 10, 10)
        assert set(neighbours) == set([(1, 0), (1, 1), (0, 1)])

    def test_neighbours_center_cell(self):
        neighbours = LoopEngine._neighbours((5, 5), 10, 10)
        expected = [(4, 4), (5, 4), (6, 4), (4, 5), (6, 5), (4, 6), (5, 6), (6, 6)]
        assert set(neighbours) == set(expected)
        assert len(neighbours) == 8

    def test_neighbours_edge_cell(self):
        neighbours = LoopEngine._neighbours((5, 0), 10, 10)
        expected = [(4, 0), (6, 0), (4, 1), (5, 1), (6, 1)]
        assert set(neighbours) == set(expected)

    def test_neighbours_bottom_right_corner(self):
        neighbours = LoopEngine._neighbours((9, 9), 10, 10)
        expected = [(8, 8), (9, 8), (8, 9)]
        assert set(neighbours) == set(expected)

    def test_neighbours_invalid_coordinates(self):
        with pytest.raises(ValueError):
            LoopEngine._neighbours((10, 9), 10, 10)

        with pytest.raises(ValueError):
            LoopEngine._neighbours((9, 10), 10, 10)

        with pytest.raises(ValueError):
            LoopEngine._neighbours((-1, 5), 10, 10)

    def test_alive_neighbours_count(self):
        state = State(5, 5)
        state[1, 1] = True  # top-left
        state[2, 1] = True  # top
        state[3, 2] = True  # right

        alive_count = LoopEngine._alive_neighbours((2, 2), state)
        assert alive_count == 3

    def test_alive_neighbours_no_neighbours(self):
        state = State(5, 5)
        alive_count = LoopEngine._alive_neighbours((2, 2), state)
        assert alive_count == 0

    def test_next_cell_state_underpopulation(self):
        """Any live cell with fewer than two live neighbours dies"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # one neighbour

        result = LoopEngine._next_cell_state((2, 2), state)
        assert result is False

    def test_next_cell_state_survival_two_neighbours(self):
        """Any live cell with two neighbours survives"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2

        result = LoopEngine._next_cell_state((2, 2), state)
        assert result is True

    def test_next_cell_state_survival_three_neighbours(self):
        """Any live cell with three neighbours survives"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2
        state[1, 3] = True  # neighbour 3

        result = LoopEngine._next_cell_state((2, 2), state)
        assert result is True

    def test_next_cell_state_overpopulation(self):
        """Any live cell with more than three live neighbours dies"""
        state = State(5, 5)
        state[2, 2] = True  # alive cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2
        state[1, 3] = True  # neighbour 3
        state[2, 1] = True  # neighbour 4

        result = LoopEngine._next_cell_state((2, 2), state)
        assert result is False

    def test_next_cell_state_reproduction(self):
        """Any dead cell with exactly three live neighbours becomes alive"""
        state = State(5, 5)
        state[2, 2] = False  # dead cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2
        state[1, 3] = True  # neighbour 3

        result = LoopEngine._next_cell_state((2, 2), state)
        assert result is True

    def test_next_cell_state_dead_cell_insufficient_neighbours(self):
        """Dead cell with fewer than three neighbours stays dead"""
        state = State(5, 5)
        state[2, 2] = False  # dead cell
        state[1, 1] = True  # neighbour 1
        state[1, 2] = True  # neighbour 2

        result = LoopEngine._next_cell_state((2, 2), state)
        assert result is False

    def test_next_state_blinker_pattern(self):
        """Test the classic blinker pattern (oscillates between horizontal and vertical)"""
        state = State(5, 5)
        state[1, 2] = True
        state[2, 2] = True
        state[3, 2] = True

        next_state = LoopEngine.next_state(state)

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

        next_state = LoopEngine.next_state(state)

        assert next_state[1, 1] is True
        assert next_state[1, 2] is True
        assert next_state[2, 1] is True
        assert next_state[2, 2] is True

    def test_next_state_empty_grid(self):
        """Test that empty grid stays empty"""
        state = State(5, 5)
        next_state = LoopEngine.next_state(state)

        for y in range(5):
            for x in range(5):
                assert next_state[x, y] is False

    def test_next_state_dimensions_preserved(self):
        """Test that the dimensions of the state are preserved"""
        state = State(7, 3)
        next_state = LoopEngine.next_state(state)

        assert next_state.width == 7
        assert next_state.height == 3


class TestNumpyEngine:
    """Test the numpy-optimized implementation."""

    def test_next_state_blinker_pattern(self):
        """Test the classic blinker pattern"""
        state = State(5, 5)
        state[1, 2] = True
        state[2, 2] = True
        state[3, 2] = True

        next_state = NumpyEngine.next_state(state)

        assert next_state[2, 1] is True
        assert next_state[2, 2] is True
        assert next_state[2, 3] is True
        assert next_state[1, 2] is False
        assert next_state[3, 2] is False

    def test_next_state_block_pattern(self):
        """Test the block pattern (still life)"""
        state = State(4, 4)
        state[1, 1] = True
        state[1, 2] = True
        state[2, 1] = True
        state[2, 2] = True

        next_state = NumpyEngine.next_state(state)

        assert next_state[1, 1] is True
        assert next_state[1, 2] is True
        assert next_state[2, 1] is True
        assert next_state[2, 2] is True

    def test_next_state_empty_grid(self):
        """Test that empty grid stays empty"""
        state = State(5, 5)
        next_state = NumpyEngine.next_state(state)

        for y in range(5):
            for x in range(5):
                assert next_state[x, y] is False

    def test_next_state_dimensions_preserved(self):
        """Test that dimensions are preserved"""
        state = State(7, 3)
        next_state = NumpyEngine.next_state(state)

        assert next_state.width == 7
        assert next_state.height == 3

    def test_underpopulation(self):
        """Test that live cells with < 2 neighbors die"""
        state = State(5, 5)
        state[2, 2] = True
        state[1, 1] = True  # one neighbor

        next_state = NumpyEngine.next_state(state)
        assert next_state[2, 2] is False

    def test_survival(self):
        """Test that live cells with 2-3 neighbors survive"""
        state = State(5, 5)
        state[2, 2] = True
        state[1, 1] = True
        state[1, 2] = True  # two neighbors

        next_state = NumpyEngine.next_state(state)
        assert next_state[2, 2] is True

    def test_overpopulation(self):
        """Test that live cells with > 3 neighbors die"""
        state = State(5, 5)
        state[2, 2] = True
        state[1, 1] = True
        state[1, 2] = True
        state[1, 3] = True
        state[2, 1] = True  # four neighbors

        next_state = NumpyEngine.next_state(state)
        assert next_state[2, 2] is False

    def test_reproduction(self):
        """Test that dead cells with exactly 3 neighbors become alive"""
        state = State(5, 5)
        state[1, 1] = True
        state[1, 2] = True
        state[1, 3] = True

        next_state = NumpyEngine.next_state(state)
        assert next_state[2, 2] is True


class TestEngineEquivalence:
    """Test that both engines produce the same results."""

    @pytest.mark.parametrize(
        "pattern_setup",
        [
            # Blinker
            lambda s: (
                s.__setitem__((1, 2), True),
                s.__setitem__((2, 2), True),
                s.__setitem__((3, 2), True),
            ),
            # Block
            lambda s: (
                s.__setitem__((1, 1), True),
                s.__setitem__((1, 2), True),
                s.__setitem__((2, 1), True),
                s.__setitem__((2, 2), True),
            ),
            # Glider
            lambda s: (
                s.__setitem__((1, 0), True),
                s.__setitem__((2, 1), True),
                s.__setitem__((0, 2), True),
                s.__setitem__((1, 2), True),
                s.__setitem__((2, 2), True),
            ),
        ],
    )
    def test_engines_produce_same_results(self, pattern_setup):
        """Verify both engines produce identical results for various patterns."""
        # Setup state for LoopEngine
        state_loop = State(10, 10)
        pattern_setup(state_loop)

        # Setup identical state for NumpyEngine
        state_numpy = State(10, 10)
        pattern_setup(state_numpy)

        # Run one generation on both
        next_loop = LoopEngine.next_state(state_loop)
        next_numpy = NumpyEngine.next_state(state_numpy)

        # Compare all cells
        for y in range(10):
            for x in range(10):
                assert next_loop[x, y] == next_numpy[x, y], (
                    f"Mismatch at ({x}, {y}): Loop={next_loop[x, y]}, Numpy={next_numpy[x, y]}"
                )
