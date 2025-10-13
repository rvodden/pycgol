import pytest
from pycgol._state import State


class TestState:
    def test_dimensions(self):
        undertest = State(10, 10)

        assert undertest.width == 10
        assert undertest.height == 10

    def test_initialization_default_values(self):
        undertest = State(3, 3)

        # All cells should be False by default
        for y in range(3):
            for x in range(3):
                assert undertest[x, y] is False

    def test_set_and_get_cell(self):
        undertest = State(5, 5)

        # Test setting a cell to True
        undertest[2, 3] = True
        assert undertest[2, 3] is True

        # Test setting a cell to False
        undertest[2, 3] = False
        assert undertest[2, 3] is False

    def test_bounds_validation_valid_coordinates(self):
        undertest = State(10, 10)

        # Test valid corner coordinates
        undertest[0, 0] = True
        assert undertest[0, 0] is True

        undertest[9, 9] = True
        assert undertest[9, 9] is True

        # Test valid middle coordinates
        undertest[5, 5] = True
        assert undertest[5, 5] is True

    def test_bounds_validation_invalid_coordinates(self):
        undertest = State(10, 10)

        # Test negative coordinates
        with pytest.raises(
            ValueError, match=r"\(-1, 0\) is outside the bounds \(10, 10\)"
        ):
            undertest[-1, 0] = True

        with pytest.raises(
            ValueError, match=r"\(0, -1\) is outside the bounds \(10, 10\)"
        ):
            undertest[0, -1] = True

        # Test coordinates beyond bounds
        with pytest.raises(
            ValueError, match=r"\(10, 5\) is outside the bounds \(10, 10\)"
        ):
            undertest[10, 5] = True

        with pytest.raises(
            ValueError, match=r"\(5, 10\) is outside the bounds \(10, 10\)"
        ):
            undertest[5, 10] = True

    def test_bounds_validation_on_get(self):
        undertest = State(5, 5)

        # Test that getting invalid coordinates also raises ValueError
        with pytest.raises(
            ValueError, match=r"\(5, 0\) is outside the bounds \(5, 5\)"
        ):
            _ = undertest[5, 0]

        with pytest.raises(
            ValueError, match=r"\(0, 5\) is outside the bounds \(5, 5\)"
        ):
            _ = undertest[0, 5]

    def test_rectangular_grid(self):
        # Test non-square grid
        undertest = State(3, 7)

        assert undertest.width == 3
        assert undertest.height == 7

        # Test that we can access all valid coordinates
        undertest[2, 6] = True
        assert undertest[2, 6] is True

        # Test that invalid coordinates are rejected
        with pytest.raises(ValueError):
            undertest[3, 6] = True

        with pytest.raises(ValueError):
            undertest[2, 7] = True

    def test_single_cell_grid(self):
        undertest = State(1, 1)

        assert undertest.width == 1
        assert undertest.height == 1

        undertest[0, 0] = True
        assert undertest[0, 0] is True

    def test_width_property_empty_grid_edge_case(self):
        # Test edge case: what happens with 0 width?
        with pytest.raises(ValueError):
            _ = State(0, 5)

    def test_height_property_empty_grid_edge_case(self):
        # Test edge case: what happens with 0 height?
        with pytest.raises(ValueError):
            _ = State(5, 0)
