"""Sparse state storage implementation."""

from ._state_interface import StateInterface


class SparseState(StateInterface):
    """Sparse storage using set of live cell coordinates.

    Only stores coordinates of live cells, making it memory-efficient for
    sparse patterns. Dead cells are implicitly represented by absence.

    Memory: O(live cells)
    Access: O(1) with hash lookup
    Best for: Sparse patterns (<10% alive cells)
    """

    def __init__(self, width: int, height: int):
        """
        Initialize a sparse state grid.

        Args:
            width: Width of the grid (must be > 0)
            height: Height of the grid (must be > 0)

        Raises:
            ValueError: If width or height is <= 0
        """
        if width <= 0 or height <= 0:
            raise ValueError(
                "Grid cannot be empty, neither height nor width can be zero or less."
            )

        self._width = width
        self._height = height
        self._live_cells: set[tuple[int, int]] = set()

    @property
    def width(self) -> int:
        """Width of the game grid."""
        return self._width

    @property
    def height(self) -> int:
        """Height of the game grid."""
        return self._height

    def _validate_bounds(self, index: tuple[int, int]) -> None:
        """Validate that coordinates are within grid bounds."""
        x, y = index
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"({x}, {y}) is outside the bounds ({self.width}, {self.height})."
            )

    def __getitem__(self, index: tuple[int, int]) -> bool:
        """
        Get cell state at position (x, y).

        Complexity: O(1) average case (hash lookup)
        """
        self._validate_bounds(index)
        return index in self._live_cells

    def __setitem__(self, index: tuple[int, int], value: bool) -> None:
        """
        Set cell state at position (x, y).

        Complexity: O(1) average case (hash set operations)
        """
        self._validate_bounds(index)
        if value:
            self._live_cells.add(index)
        else:
            self._live_cells.discard(index)

    def get_live_cells(self) -> set[tuple[int, int]]:
        """
        Get set of all live cell coordinates.

        This is O(1) for sparse state since we already store the set.

        Returns:
            Copy of the set of (x, y) tuples for all live cells
        """
        return self._live_cells.copy()

    @classmethod
    def from_state(cls, other: StateInterface) -> "SparseState":
        """
        Create sparse state from another state type.

        Args:
            other: Source state to convert from

        Returns:
            New SparseState with same dimensions and live cells
        """
        new_state = cls(other.width, other.height)

        # Efficient conversion: only copy live cells
        if hasattr(other, "get_live_cells"):
            for x, y in other.get_live_cells():
                new_state[x, y] = True
        else:
            # Fallback: scan entire grid (slow for dense states)
            for y in range(other.height):
                for x in range(other.width):
                    if other[x, y]:
                        new_state[x, y] = True

        return new_state
