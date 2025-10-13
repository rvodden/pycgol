from pycgol.state import DenseState as State
from pycgol.objects._glide_gun import GliderGun


class TestGliderGun:
    def test_glider_gun_placement_no_rotation(self):
        """Test basic placement without rotation."""
        state = State(50, 50)
        gun = GliderGun()
        result_state = gun.place((5, 5), state, rotation=0)

        # Should return the same state object
        assert result_state is state

        # Check a few key cells from the pattern are set
        # Left square
        assert state[5, 9] is True  # (0, 4)
        assert state[5, 10] is True  # (0, 5)
        assert state[6, 9] is True  # (1, 4)
        assert state[6, 10] is True  # (1, 5)

        # Right square
        assert state[39, 7] is True  # (34, 2)
        assert state[39, 8] is True  # (34, 3)
        assert state[40, 7] is True  # (35, 2)
        assert state[40, 8] is True  # (35, 3)

    def test_glider_gun_placement_90_degrees(self):
        """Test placement with 90 degree rotation."""
        state = State(50, 50)
        gun = GliderGun()
        result_state = gun.place((10, 10), state, rotation=90)

        # Check that some cells are set (pattern should be rotated)
        assert result_state is state

        # After 90° CW rotation, the pattern should be rotated
        # Original (0, 4) -> (height - 1 - 4, 0) = (4, 0) in pattern coords
        # Pattern height is 9 (0-8 inclusive), so (0, 4) -> (4, 0)
        assert state[14, 10] is True  # rotated left square cell

    def test_glider_gun_placement_180_degrees(self):
        """Test placement with 180 degree rotation."""
        state = State(50, 50)
        gun = GliderGun()
        result_state = gun.place((10, 10), state, rotation=180)

        assert result_state is state
        # After 180° rotation, pattern should be upside down and flipped
        # Check that at least some cells are set
        cell_count = sum(1 for y in range(50) for x in range(50) if state[x, y])
        assert cell_count == len(GliderGun._CELLS)

    def test_glider_gun_placement_270_degrees(self):
        """Test placement with 270 degree rotation."""
        state = State(50, 50)
        gun = GliderGun()
        result_state = gun.place((10, 10), state, rotation=270)

        assert result_state is state
        # After 270° rotation, pattern should be rotated CCW
        cell_count = sum(1 for y in range(50) for x in range(50) if state[x, y])
        assert cell_count == len(GliderGun._CELLS)

    def test_glider_gun_cells_count(self):
        """Test that the correct number of cells are placed."""
        state = State(60, 60)
        gun = GliderGun()
        gun.place((10, 10), state, rotation=0)

        # Count alive cells
        cell_count = sum(1 for y in range(60) for x in range(60) if state[x, y])
        assert cell_count == len(GliderGun._CELLS)

    def test_glider_gun_pattern_constant(self):
        """Test that _CELLS has the expected number of cells."""
        # Gosper's glider gun has 36 cells
        assert len(GliderGun._CELLS) == 36

    def test_glider_gun_bounding_box(self):
        """Test that pattern fits in expected bounding box."""
        max_x = max(cell[0] for cell in GliderGun._CELLS)
        max_y = max(cell[1] for cell in GliderGun._CELLS)

        # Gosper's glider gun is 36 cells wide (0-35) and 9 cells tall (0-8)
        assert max_x == 35
        assert max_y == 8

    def test_glider_gun_placement_at_origin(self):
        """Test placement at (0, 0)."""
        state = State(50, 50)
        gun = GliderGun()
        gun.place((0, 0), state, rotation=0)

        # Check that cells are placed correctly
        assert state[0, 4] is True
        assert state[0, 5] is True
        assert state[1, 4] is True
        assert state[1, 5] is True

    def test_glider_gun_placement_near_boundary(self):
        """Test placement near the edge where some cells go out of bounds."""
        state = State(40, 15)
        gun = GliderGun()
        gun.place((10, 10), state, rotation=0)

        # Some cells should be placed, but those out of bounds should be skipped
        # Pattern is 36 wide and 9 tall, placed at (10, 10)
        # Right edge goes to 10 + 35 = 45, which exceeds width of 40
        # Bottom edge goes to 10 + 8 = 18, which exceeds height of 15

        # Left square should be placed (within bounds)
        assert state[10, 14] is True  # (0, 4)

        # Check that cells were placed (but not all 36 since some are out of bounds)
        cell_count = sum(1 for y in range(15) for x in range(40) if state[x, y])
        assert 0 < cell_count < len(GliderGun._CELLS)

    def test_glider_gun_placement_completely_out_of_bounds(self):
        """Test placement completely outside the grid."""
        state = State(10, 10)
        gun = GliderGun()
        gun.place((50, 50), state, rotation=0)

        # No cells should be placed
        cell_count = sum(1 for y in range(10) for x in range(10) if state[x, y])
        assert cell_count == 0

    def test_multiple_glider_gun_placements(self):
        """Test placing multiple glider guns."""
        state = State(100, 100)

        gun1 = GliderGun()
        gun1.place((10, 10), state, rotation=0)
        gun2 = GliderGun()
        gun2.place((50, 50), state, rotation=90)

        # Should have cells from both guns
        # (might overlap, so count >= len(_CELLS))
        cell_count = sum(1 for y in range(100) for x in range(100) if state[x, y])
        assert cell_count >= len(GliderGun._CELLS)

    def test_rotate_90_cw_helper(self):
        """Test the _rotate_90_cw helper method."""
        # For a 36x9 bounding box (width=36, height=9)
        # (0, 0) -> (8, 0)
        # (0, 8) -> (0, 0)
        # (35, 0) -> (8, 35)
        # (35, 8) -> (0, 35)

        gun = GliderGun()
        assert gun._rotate_90_cw(0, 0, 36, 9) == (8, 0)
        assert gun._rotate_90_cw(0, 8, 36, 9) == (0, 0)
        assert gun._rotate_90_cw(35, 0, 36, 9) == (8, 35)
        assert gun._rotate_90_cw(35, 8, 36, 9) == (0, 35)

    def test_rotation_preserves_cell_count(self):
        """Test that all rotations place the same number of cells."""
        for rotation in [0, 90, 180, 270]:
            state = State(60, 60)
            gun = GliderGun()
            gun.place((10, 10), state, rotation=rotation)

            cell_count = sum(1 for y in range(60) for x in range(60) if state[x, y])
            assert cell_count == len(GliderGun._CELLS), (
                f"Rotation {rotation} produced {cell_count} cells, expected {len(GliderGun._CELLS)}"
            )

    def test_different_rotations_produce_different_patterns(self):
        """Test that different rotations produce different cell positions."""
        state_0 = State(60, 60)
        state_90 = State(60, 60)

        gun1 = GliderGun()
        gun1.place((10, 10), state_0, rotation=0)
        gun2 = GliderGun()
        gun2.place((10, 10), state_90, rotation=90)

        # Collect cell positions
        cells_0 = {(x, y) for y in range(60) for x in range(60) if state_0[x, y]}
        cells_90 = {(x, y) for y in range(60) for x in range(60) if state_90[x, y]}

        # Patterns should be different
        assert cells_0 != cells_90

    def test_glider_gun_has_no_dead_cells_in_pattern(self):
        """Test that all cells in _CELLS are unique (no duplicates)."""
        assert len(GliderGun._CELLS) == len(set(GliderGun._CELLS))
