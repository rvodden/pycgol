class State:
    _cells: list[list[bool]]

    def __init__(self, width: int, height: int):
        self._cells = []
        if width <= 0 or height <= 0:
            raise ValueError("Grid cannot be empty, neither height nor width can be zero or less.")

        for _ in range(height):
            self._cells.append([False] * width)

    @property
    def width(self):
        return len(self._cells[0])
    
    @property
    def height(self):
        return len(self._cells)

    def _validate_bounds(self, index: tuple[int, int]) -> None:
        x,y = index
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"({x}, {y}) is outside the bounds ({self.width}, {self.height}).")

    def __getitem__(self, index: tuple[int, int]) -> bool:
        self._validate_bounds(index)
        x,y = index
        return self._cells[y][x]
    
    def __setitem__(self, index: tuple[int, int], value: bool) -> None:
        self._validate_bounds(index)
        x,y = index
        self._cells[y][x] = value