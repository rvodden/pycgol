"""Abstract interface for game state storage."""

from abc import ABC, abstractmethod


class StateInterface(ABC):
    """Abstract base class for Game of Life state storage.

    This interface allows different storage strategies (dense, sparse)
    while maintaining a consistent API for engines and rendering.
    """

    @property
    @abstractmethod
    def width(self) -> int:
        """Width of the game grid."""
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        """Height of the game grid."""
        pass

    @abstractmethod
    def __getitem__(self, index: tuple[int, int]) -> bool:
        """
        Get cell state at position (x, y).

        Args:
            index: Tuple of (x, y) coordinates

        Returns:
            True if cell is alive, False if dead

        Raises:
            ValueError: If coordinates are out of bounds
        """
        pass

    @abstractmethod
    def __setitem__(self, index: tuple[int, int], value: bool) -> None:
        """
        Set cell state at position (x, y).

        Args:
            index: Tuple of (x, y) coordinates
            value: True for alive, False for dead

        Raises:
            ValueError: If coordinates are out of bounds
        """
        pass

    @abstractmethod
    def get_live_cells(self) -> set[tuple[int, int]]:
        """
        Get set of all live cell coordinates.

        This method is crucial for sparse algorithms, allowing O(live cells)
        iteration instead of O(grid size).

        Returns:
            Set of (x, y) tuples for all live cells
        """
        pass

    @classmethod
    @abstractmethod
    def from_state(cls, other: "StateInterface") -> "StateInterface":
        """
        Create instance of this state type from another state.

        This enables conversion between state types (e.g., dense to sparse)
        when engines switch.

        Args:
            other: Source state to convert from

        Returns:
            New state of this type with same dimensions and live cells
        """
        pass

    @abstractmethod
    def _validate_bounds(self, index: tuple[int, int]) -> None:
        """
        Validate that coordinates are within grid bounds.

        Args:
            index: Tuple of (x, y) coordinates

        Raises:
            ValueError: If coordinates are out of bounds
        """
        pass
