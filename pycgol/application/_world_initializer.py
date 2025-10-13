"""World initialization for Conway's Game of Life."""

from ..state import StateInterface
from ..objects import GliderGun


class WorldInitializer:
    """Handles initialization of the game world with patterns."""

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        cell_size: int,
        border_cells: int = 100
    ) -> None:
        """
        Initialize the world initializer.

        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            cell_size: Size of each cell in pixels
            border_cells: Number of border cells around the visible area
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._cell_size = cell_size
        self._border_cells = border_cells

    def create_initial_state(self) -> StateInterface:
        """
        Create the initial game state with patterns.

        Returns:
            A State object with the initial pattern configuration
        """
        # Calculate grid dimensions: viewport cells + border on all sides
        viewport_cells_width = self._screen_width // self._cell_size
        viewport_cells_height = self._screen_height // self._cell_size
        grid_width = viewport_cells_width + (2 * self._border_cells)
        grid_height = viewport_cells_height + (2 * self._border_cells)

        state = State(grid_width, grid_height)

        # Place first glider gun in top-left, shooting down-right
        gun1_x = self._border_cells + 10  # 10 cells from left edge
        gun1_y = self._border_cells + 10  # 10 cells from top edge
        gun1 = GliderGun()
        state = gun1.place((gun1_x, gun1_y), state, rotation=0)

        # Place second glider gun rotated 90 degrees to shoot down-left
        # Position it to the right so the glider streams will collide
        gun2_x = gun1_x + 84  # 84 cells to the right for collision
        gun2_y = gun1_y + 4   # Offset by 4 cells to adjust collision timing
        gun2 = GliderGun()
        state = gun2.place((gun2_x, gun2_y), state, rotation=90)

        return state

    def get_initial_viewport_position(self) -> tuple[int, int]:
        """
        Get the initial viewport position (centered on the grid).

        Returns:
            Tuple of (viewport_x, viewport_y) in grid cells
        """
        return (self._border_cells, self._border_cells)
