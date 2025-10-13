"""Tests for SparseState implementation."""

import pytest

from pycgol.state import SparseState, DenseState


class TestSparseState:
    """Test the SparseState implementation."""

    def test_dimensions(self):
        """Test that dimensions are correctly set."""
        state = SparseState(10, 20)
        assert state.width == 10
        assert state.height == 20

    def test_initialization_default_values(self):
        """Test that all cells are dead by default."""
        state = SparseState(5, 5)
        for x in range(5):
            for y in range(5):
                assert state[x, y] is False

    def test_set_and_get_cell(self):
        """Test setting and getting individual cells."""
        state = SparseState(10, 10)
        state[3, 4] = True
        assert state[3, 4] is True
        assert state[3, 5] is False

    def test_bounds_validation_valid_coordinates(self):
        """Test that valid coordinates don't raise exceptions."""
        state = SparseState(10, 10)
        state[0, 0] = True
        state[9, 9] = True
        assert state[0, 0] is True
        assert state[9, 9] is True

    def test_bounds_validation_invalid_coordinates(self):
        """Test that invalid coordinates raise ValueError."""
        state = SparseState(10, 10)
        with pytest.raises(ValueError):
            state[-1, 0] = True
        with pytest.raises(ValueError):
            state[10, 0] = True
        with pytest.raises(ValueError):
            state[0, -1] = True
        with pytest.raises(ValueError):
            state[0, 10] = True

    def test_bounds_validation_on_get(self):
        """Test that bounds validation works on get operations."""
        state = SparseState(10, 10)
        with pytest.raises(ValueError):
            _ = state[10, 0]
        with pytest.raises(ValueError):
            _ = state[0, 10]

    def test_rectangular_grid(self):
        """Test non-square grids work correctly."""
        state = SparseState(20, 10)
        state[19, 9] = True
        assert state[19, 9] is True
        assert state.width == 20
        assert state.height == 10

    def test_single_cell_grid(self):
        """Test minimum size grid (1x1)."""
        state = SparseState(1, 1)
        assert state.width == 1
        assert state.height == 1
        state[0, 0] = True
        assert state[0, 0] is True

    def test_width_property_empty_grid_edge_case(self):
        """Test that zero width raises error."""
        with pytest.raises(ValueError):
            SparseState(0, 10)

    def test_height_property_empty_grid_edge_case(self):
        """Test that zero height raises error."""
        with pytest.raises(ValueError):
            SparseState(10, 0)

    def test_get_live_cells_empty(self):
        """Test get_live_cells returns empty set for dead grid."""
        state = SparseState(10, 10)
        live_cells = state.get_live_cells()
        assert len(live_cells) == 0

    def test_get_live_cells_single(self):
        """Test get_live_cells returns single live cell."""
        state = SparseState(10, 10)
        state[5, 5] = True
        live_cells = state.get_live_cells()
        assert len(live_cells) == 1
        assert (5, 5) in live_cells

    def test_get_live_cells_multiple(self):
        """Test get_live_cells returns multiple live cells."""
        state = SparseState(10, 10)
        state[1, 2] = True
        state[3, 4] = True
        state[5, 6] = True
        live_cells = state.get_live_cells()
        assert len(live_cells) == 3
        assert (1, 2) in live_cells
        assert (3, 4) in live_cells
        assert (5, 6) in live_cells

    def test_set_cell_to_false_removes_from_live_cells(self):
        """Test that setting a cell to False removes it from live cells."""
        state = SparseState(10, 10)
        state[5, 5] = True
        assert len(state.get_live_cells()) == 1
        state[5, 5] = False
        assert len(state.get_live_cells()) == 0
        assert state[5, 5] is False

    def test_from_state_dense_to_sparse(self):
        """Test conversion from DenseState to SparseState."""
        dense = DenseState(10, 10)
        dense[2, 3] = True
        dense[5, 7] = True

        sparse = SparseState.from_state(dense)
        assert sparse.width == 10
        assert sparse.height == 10
        assert sparse[2, 3] is True
        assert sparse[5, 7] is True
        assert len(sparse.get_live_cells()) == 2

    def test_from_state_sparse_to_sparse(self):
        """Test conversion from SparseState to SparseState (copy)."""
        sparse1 = SparseState(10, 10)
        sparse1[3, 4] = True
        sparse1[6, 7] = True

        sparse2 = SparseState.from_state(sparse1)
        assert sparse2.width == 10
        assert sparse2.height == 10
        assert sparse2[3, 4] is True
        assert sparse2[6, 7] is True
        assert len(sparse2.get_live_cells()) == 2

        # Verify it's a copy, not a reference
        sparse2[8, 9] = True
        assert sparse2[8, 9] is True
        assert sparse1[8, 9] is False


class TestDenseState:
    """Test DenseState methods added by StateInterface."""

    def test_get_live_cells_empty(self):
        """Test get_live_cells returns empty set for dead grid."""
        state = DenseState(10, 10)
        live_cells = state.get_live_cells()
        assert len(live_cells) == 0

    def test_get_live_cells_with_pattern(self):
        """Test get_live_cells returns correct cells."""
        state = DenseState(10, 10)
        state[2, 3] = True
        state[4, 5] = True
        state[6, 7] = True

        live_cells = state.get_live_cells()
        assert len(live_cells) == 3
        assert (2, 3) in live_cells
        assert (4, 5) in live_cells
        assert (6, 7) in live_cells

    def test_from_state_sparse_to_dense(self):
        """Test conversion from SparseState to DenseState."""
        sparse = SparseState(10, 10)
        sparse[3, 4] = True
        sparse[7, 8] = True

        dense = DenseState.from_state(sparse)
        assert dense.width == 10
        assert dense.height == 10
        assert dense[3, 4] is True
        assert dense[7, 8] is True
        assert len(dense.get_live_cells()) == 2

    def test_from_state_dense_to_dense(self):
        """Test conversion from DenseState to DenseState (copy)."""
        dense1 = DenseState(10, 10)
        dense1[2, 3] = True
        dense1[5, 6] = True

        dense2 = DenseState.from_state(dense1)
        assert dense2.width == 10
        assert dense2.height == 10
        assert dense2[2, 3] is True
        assert dense2[5, 6] is True

        # Verify it's a copy
        dense2[8, 9] = True
        assert dense2[8, 9] is True
        assert dense1[8, 9] is False
