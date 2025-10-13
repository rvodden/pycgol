from ._object import Object


class GliderGun(Object):
    """Gosper's Glider Gun - a pattern that periodically emits gliders."""

    _CELLS = [
        # Left square
        (0, 4),
        (0, 5),
        (1, 4),
        (1, 5),
        # Left shooter
        (10, 4),
        (10, 5),
        (10, 6),
        (11, 3),
        (11, 7),
        (12, 2),
        (12, 8),
        (13, 2),
        (13, 8),
        (14, 5),
        (15, 3),
        (15, 7),
        (16, 4),
        (16, 5),
        (16, 6),
        (17, 5),
        # Right shooter
        (20, 2),
        (20, 3),
        (20, 4),
        (21, 2),
        (21, 3),
        (21, 4),
        (22, 1),
        (22, 5),
        (24, 0),
        (24, 1),
        (24, 5),
        (24, 6),
        # Right square
        (34, 2),
        (34, 3),
        (35, 2),
        (35, 3),
    ]

    def __init__(self) -> None:
        """Initialize a GliderGun object."""
        super().__init__(self._CELLS)
