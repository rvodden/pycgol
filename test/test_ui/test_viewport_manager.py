from pycgol.ui._viewport_manager import ViewportManager


class TestViewportManager:
    """Test the ViewportManager class."""

    def test_init_default_values(self):
        """Test that ViewportManager initializes with correct defaults."""
        viewport = ViewportManager(cell_size=10)

        assert viewport.cell_size == 10
        assert viewport.viewport_x == 0
        assert viewport.viewport_y == 0

    def test_init_custom_cell_size(self):
        """Test initialization with custom cell size."""
        viewport = ViewportManager(cell_size=20)

        assert viewport.cell_size == 20

    def test_set_viewport(self):
        """Test setting viewport position."""
        viewport = ViewportManager()

        viewport.set_viewport(50, 100)

        assert viewport.viewport_x == 50
        assert viewport.viewport_y == 100

    def test_start_drag(self):
        """Test starting a drag operation."""
        viewport = ViewportManager()
        viewport.set_viewport(10, 20)

        viewport.start_drag((100, 200))

        # Dragging state should be enabled
        assert viewport._dragging is True
        assert viewport._drag_start_pos == (100, 200)
        assert viewport._drag_start_viewport == (10, 20)

    def test_update_drag_moves_viewport(self):
        """Test that update_drag changes viewport position correctly."""
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(50, 50)
        viewport.start_drag((100, 100))

        # Drag 50 pixels right and 30 pixels down
        viewport.update_drag((150, 130))

        # Movement is inverted: right drag = move viewport left
        # 50 pixels right / 10 cell_size = 5 cells left
        # 30 pixels down / 10 cell_size = 3 cells up
        assert viewport.viewport_x == 50 - 5  # 45
        assert viewport.viewport_y == 50 - 3  # 47

    def test_update_drag_without_start_does_nothing(self):
        """Test that update_drag without start_drag does nothing."""
        viewport = ViewportManager()
        viewport.set_viewport(10, 20)

        viewport.update_drag((100, 200))

        # Viewport should not change
        assert viewport.viewport_x == 10
        assert viewport.viewport_y == 20

    def test_end_drag(self):
        """Test ending a drag operation."""
        viewport = ViewportManager()
        viewport.start_drag((100, 200))

        viewport.end_drag()

        assert viewport._dragging is False
        assert viewport._drag_start_pos is None
        assert viewport._drag_start_viewport is None

    def test_drag_workflow(self):
        """Test complete drag workflow: start, update, end."""
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(100, 100)

        # Start drag
        viewport.start_drag((500, 500))
        assert viewport.viewport_x == 100
        assert viewport.viewport_y == 100

        # Drag 100 pixels left (viewport moves right)
        viewport.update_drag((400, 500))
        assert viewport.viewport_x == 110  # 100 + (100 / 10)
        assert viewport.viewport_y == 100

        # Continue drag
        viewport.update_drag((350, 450))
        assert viewport.viewport_x == 115  # 100 + (150 / 10)
        assert viewport.viewport_y == 105  # 100 + (50 / 10)

        # End drag
        viewport.end_drag()

        # Further updates should not change viewport
        viewport.update_drag((200, 200))
        assert viewport.viewport_x == 115
        assert viewport.viewport_y == 105

    def test_zoom_in_increases_cell_size(self):
        """Test that positive zoom delta increases cell size."""
        viewport = ViewportManager(cell_size=10)

        viewport.zoom(
            delta=1,
            mouse_pos=(100, 100),
            screen_width=800,
            screen_height=600,
            max_grid_width=200,
            max_grid_height=150,
        )

        assert viewport.cell_size == 12  # 10 + 2

    def test_zoom_out_decreases_cell_size(self):
        """Test that negative zoom delta decreases cell size."""
        viewport = ViewportManager(cell_size=10)

        viewport.zoom(
            delta=-1,
            mouse_pos=(100, 100),
            screen_width=800,
            screen_height=600,
            max_grid_width=200,
            max_grid_height=150,
        )

        assert viewport.cell_size == 8  # 10 - 2

    def test_zoom_respects_minimum_cell_size(self):
        """Test that zoom cannot reduce cell size below 2."""
        viewport = ViewportManager(cell_size=4)

        # Try to zoom out twice (would go to 0)
        viewport.zoom(-1, (100, 100), 800, 600, 200, 150)
        assert viewport.cell_size == 2

        viewport.zoom(-1, (100, 100), 800, 600, 200, 150)
        assert viewport.cell_size == 2  # Still 2, not 0

    def test_zoom_respects_maximum_cell_size(self):
        """Test that zoom cannot increase cell size above 50."""
        viewport = ViewportManager(cell_size=48)

        # Try to zoom in twice (would go to 52)
        viewport.zoom(1, (100, 100), 800, 600, 200, 150)
        assert viewport.cell_size == 50

        viewport.zoom(1, (100, 100), 800, 600, 200, 150)
        assert viewport.cell_size == 50  # Still 50, not 52

    def test_zoom_adjusts_viewport_to_keep_mouse_position_stable(self):
        """Test that zoom adjusts viewport so the cell under mouse stays in place."""
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(0, 0)

        # Mouse at (100, 100) = grid cell (10, 10)
        # After zoom in, cell size becomes 12
        # Mouse at (100, 100) = grid cell (8, 8) in new zoom
        # Need to adjust viewport to keep grid cell (10, 10) under mouse
        viewport.zoom(1, (100, 100), 800, 600, 200, 150)

        # New cell size is 12
        assert viewport.cell_size == 12

        # Viewport should adjust to keep same grid cell under mouse
        # Expected viewport_x = 10 - (100 // 12) = 10 - 8 = 2
        # Expected viewport_y = 10 - (100 // 12) = 10 - 8 = 2
        assert viewport.viewport_x == 2
        assert viewport.viewport_y == 2

    def test_zoom_clamps_viewport_to_valid_bounds(self):
        """Test that zoom doesn't allow viewport to go outside grid bounds."""
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(100, 100)

        # Zoom in significantly
        for _ in range(10):
            viewport.zoom(1, (400, 300), 800, 600, 150, 120)

        # Viewport should be clamped to valid range
        assert viewport.viewport_x >= 0
        assert viewport.viewport_y >= 0

        # Maximum viewport is grid_size - visible_cells
        # visible_cells = screen_size / cell_size
        max_viewport_x = max(0, 150 - (800 // viewport.cell_size))
        max_viewport_y = max(0, 120 - (600 // viewport.cell_size))

        assert viewport.viewport_x <= max_viewport_x
        assert viewport.viewport_y <= max_viewport_y

    def test_zoom_no_change_when_already_at_limit(self):
        """Test that viewport doesn't change when zoom is at limit."""
        viewport = ViewportManager(cell_size=2)
        viewport.set_viewport(10, 20)

        # Try to zoom out (already at minimum)
        viewport.zoom(-1, (100, 100), 800, 600, 200, 150)

        # Viewport should not change because cell size didn't change
        assert viewport.viewport_x == 10
        assert viewport.viewport_y == 20

    def test_properties_are_readonly(self):
        """Test that viewport properties expose internal state correctly."""
        viewport = ViewportManager(cell_size=15)
        viewport.set_viewport(25, 35)

        assert viewport.cell_size == 15
        assert viewport.viewport_x == 25
        assert viewport.viewport_y == 35

        # Properties should reflect changes
        viewport._cell_size = 20
        viewport._viewport_x = 50
        viewport._viewport_y = 60

        assert viewport.cell_size == 20
        assert viewport.viewport_x == 50
        assert viewport.viewport_y == 60
