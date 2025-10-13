from ._object import Object


class Glider(Object):
    """A glider pattern that moves diagonally across the grid."""

    _CELLS = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)]

    def __init__(self) -> None:
        """Initialize a Glider object."""
        super().__init__(self._CELLS)
