from abc import ABC
from .._state import State


class Object(ABC):
    """Base class for Game of Life objects with rotation and placement support."""

    def __init__(self, cells: list[tuple[int, int]]) -> None:
        """
        Initialize a Game of Life object.

        Args:
            cells: List of (x, y) coordinates defining the object's pattern
        """
        self._cells = cells

    @staticmethod
    def _rotate_90_cw(x: int, y: int, width: int, height: int) -> tuple[int, int]:
        """
        Rotate a point 90 degrees clockwise around the pattern's bounding box.

        Args:
            x: X coordinate in pattern
            y: Y coordinate in pattern
            width: Width of pattern bounding box
            height: Height of pattern bounding box

        Returns:
            Rotated (x, y) coordinates
        """
        return (height - 1 - y, x)

    def _get_bounding_box(self) -> tuple[int, int]:
        """
        Calculate the bounding box dimensions of the pattern.

        Returns:
            (width, height) of the bounding box
        """
        max_x = max(cell[0] for cell in self._cells) + 1
        max_y = max(cell[1] for cell in self._cells) + 1
        return max_x, max_y

    def _apply_rotation(self, rotation: int) -> list[tuple[int, int]]:
        """
        Apply rotation to the cell pattern.

        Args:
            rotation: Rotation in degrees (0, 90, 180, 270)

        Returns:
            List of rotated (x, y) coordinates
        """
        if rotation == 0:
            return self._cells

        max_x, max_y = self._get_bounding_box()
        cells = self._cells

        if rotation == 90:
            cells = [self._rotate_90_cw(u, v, max_x, max_y) for u, v in cells]
        elif rotation == 180:
            cells = [
                self._rotate_90_cw(
                    *self._rotate_90_cw(u, v, max_x, max_y), max_y, max_x
                )
                for u, v in cells
            ]
        elif rotation == 270:
            cells = [
                self._rotate_90_cw(
                    *self._rotate_90_cw(
                        *self._rotate_90_cw(u, v, max_x, max_y), max_y, max_x
                    ),
                    max_x,
                    max_y,
                )
                for u, v in cells
            ]
        else:
            raise ValueError(
                f"Invalid rotation: {rotation}. Must be 0, 90, 180, or 270."
            )

        return cells

    def place(
        self, position: tuple[int, int], state: State, rotation: int = 0
    ) -> State:
        """
        Place the object at the given position with optional rotation.

        Args:
            position: (x, y) coordinates for placement
            state: The game state
            rotation: Rotation in degrees (0, 90, 180, 270). Default is 0.

        Returns:
            The modified state object (same object, not a copy)
        """
        x, y = position
        cells = self._apply_rotation(rotation)

        for u, v in cells:
            if 0 <= x + u < state.width and 0 <= y + v < state.height:
                state[x + u, y + v] = True

        return state
