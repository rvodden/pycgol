"""Viewport management for panning and zooming in the Game of Life grid."""


class ViewportManager:
    """Manages viewport position, panning, and zooming."""

    def __init__(self, cell_size: int = 10) -> None:
        """
        Initialize the viewport manager.

        Args:
            cell_size: Initial size of each cell in pixels
        """
        self._cell_size = cell_size
        self._viewport_x = 0
        self._viewport_y = 0

        # Mouse drag state for panning
        self._dragging = False
        self._drag_start_pos: tuple[int, int] | None = None
        self._drag_start_viewport: tuple[int, int] | None = None

    @property
    def cell_size(self) -> int:
        """Get current cell size in pixels."""
        return self._cell_size

    @property
    def viewport_x(self) -> int:
        """Get viewport X position in grid cells."""
        return self._viewport_x

    @property
    def viewport_y(self) -> int:
        """Get viewport Y position in grid cells."""
        return self._viewport_y

    def set_viewport(self, x: int, y: int) -> None:
        """Set the viewport position (which part of the game grid to display)."""
        self._viewport_x = x
        self._viewport_y = y

    def start_drag(self, mouse_pos: tuple[int, int]) -> None:
        """Start panning with mouse drag."""
        self._dragging = True
        self._drag_start_pos = mouse_pos
        self._drag_start_viewport = (self._viewport_x, self._viewport_y)

    def update_drag(self, mouse_pos: tuple[int, int]) -> None:
        """Update viewport position during drag."""
        if self._dragging and self._drag_start_pos and self._drag_start_viewport:
            dx = mouse_pos[0] - self._drag_start_pos[0]
            dy = mouse_pos[1] - self._drag_start_pos[1]

            # Convert pixel movement to cell movement
            cell_dx = -dx // self._cell_size
            cell_dy = -dy // self._cell_size

            self._viewport_x = self._drag_start_viewport[0] + cell_dx
            self._viewport_y = self._drag_start_viewport[1] + cell_dy

    def end_drag(self) -> None:
        """End panning drag."""
        self._dragging = False
        self._drag_start_pos = None
        self._drag_start_viewport = None

    def zoom(
        self,
        delta: int,
        mouse_pos: tuple[int, int],
        screen_width: int,
        screen_height: int,
        max_grid_width: int,
        max_grid_height: int,
    ) -> None:
        """
        Zoom in or out, keeping the mouse position stable.

        Args:
            delta: Zoom direction (positive = zoom in, negative = zoom out)
            mouse_pos: Mouse position in screen coordinates
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            max_grid_width: Maximum width of the game grid in cells
            max_grid_height: Maximum height of the game grid in cells
        """
        old_cell_size = self._cell_size

        # Adjust cell size (zoom in/out)
        if delta > 0:  # Zoom in
            self._cell_size = min(self._cell_size + 2, 50)
        else:  # Zoom out
            self._cell_size = max(self._cell_size - 2, 2)

        if old_cell_size != self._cell_size:
            # Calculate which cell is under the mouse before zoom
            mouse_cell_x = mouse_pos[0] // old_cell_size
            mouse_cell_y = mouse_pos[1] // old_cell_size
            grid_cell_x = self._viewport_x + mouse_cell_x
            grid_cell_y = self._viewport_y + mouse_cell_y

            # Adjust viewport to keep the same grid cell under the mouse
            new_mouse_cell_x = mouse_pos[0] // self._cell_size
            new_mouse_cell_y = mouse_pos[1] // self._cell_size

            self._viewport_x = grid_cell_x - new_mouse_cell_x
            self._viewport_y = grid_cell_y - new_mouse_cell_y

            # Clamp viewport to valid bounds
            max_viewport_x = max(0, max_grid_width - (screen_width // self._cell_size))
            max_viewport_y = max(
                0, max_grid_height - (screen_height // self._cell_size)
            )
            self._viewport_x = max(0, min(self._viewport_x, max_viewport_x))
            self._viewport_y = max(0, min(self._viewport_y, max_viewport_y))
