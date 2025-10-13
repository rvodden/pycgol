"""Game state storage implementations."""

from ._state_interface import StateInterface


class DenseState(StateInterface):
    """Dense 2D array storage for Game of Life state.

    Uses a 2D list to store every cell in the grid. This is memory-intensive
    but provides O(1) access time and is efficient for dense patterns.

    Memory: O(width × height)
    Access: O(1)
    Best for: Dense patterns (>30% alive cells)
    """

    _cells: list[list[bool]]

    def __init__(self, width: int, height: int):
        """
        Initialize a dense state grid.

        Args:
            width: Width of the grid (must be > 0)
            height: Height of the grid (must be > 0)

        Raises:
            ValueError: If width or height is <= 0
        """
        self._cells = []
        if width <= 0 or height <= 0:
            raise ValueError(
                "Grid cannot be empty, neither height nor width can be zero or less."
            )

        for _ in range(height):
            self._cells.append([False] * width)

    @property
    def width(self) -> int:
        """Width of the game grid."""
        return len(self._cells[0])

    @property
    def height(self) -> int:
        """Height of the game grid."""
        return len(self._cells)

    def _validate_bounds(self, index: tuple[int, int]) -> None:
        """Validate that coordinates are within grid bounds."""
        x, y = index
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"({x}, {y}) is outside the bounds ({self.width}, {self.height})."
            )

    def __getitem__(self, index: tuple[int, int]) -> bool:
        """Get cell state at position (x, y)."""
        self._validate_bounds(index)
        x, y = index
        return self._cells[y][x]

    def __setitem__(self, index: tuple[int, int], value: bool) -> None:
        """Set cell state at position (x, y)."""
        self._validate_bounds(index)
        x, y = index
        self._cells[y][x] = value

    def get_live_cells(self) -> set[tuple[int, int]]:
        """
        Get set of all live cell coordinates.

        Scans entire grid to find live cells.
        Complexity: O(width × height)

        Returns:
            Set of (x, y) tuples for all live cells
        """
        live = set()
        for y in range(self.height):
            for x in range(self.width):
                if self._cells[y][x]:
                    live.add((x, y))
        return live

    @classmethod
    def from_state(cls, other: StateInterface) -> "DenseState":
        """
        Create dense state from another state type.

        Args:
            other: Source state to convert from

        Returns:
            New DenseState with same dimensions and live cells
        """
        new_state = cls(other.width, other.height)

        # Try efficient conversion if possible
        if hasattr(other, "get_live_cells"):
            for x, y in other.get_live_cells():
                new_state[x, y] = True
        else:
            # Fallback: scan entire grid
            for y in range(other.height):
                for x in range(other.width):
                    new_state[x, y] = other[x, y]

        return new_state


# Backward compatibility: State is an alias for DenseState
State = DenseState
