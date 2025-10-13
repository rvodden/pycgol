from ._engine import Engine
from .._state import State


class LoopEngine(Engine):
    """Original nested loop implementation."""

    @classmethod
    def _neighbours(
        cls, cell: tuple[int, int], width: int, height: int
    ) -> list[tuple[int, int]]:
        x, y = cell

        if x < 0 or x >= width or y < 0 or y >= height:
            raise ValueError(f"({x}, {y}) is outside of the bounds ({width}, {height})")

        retval = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        return [(x, y) for (x, y) in retval if 0 <= x < width and 0 <= y < height]

    @classmethod
    def _alive_neighbours(cls, cell: tuple[int, int], state: State) -> int:
        neighbours = cls._neighbours(cell, state.width, state.height)
        alive_neighbours = [state[x, y] for x, y in neighbours]
        return sum(alive_neighbours)

    @classmethod
    def _next_cell_state(cls, cell: tuple[int, int], state: State) -> bool:
        x, y = cell
        alive_neighbours = cls._alive_neighbours(cell, state)
        if state[x, y]:  # cell is alive
            if alive_neighbours < 2 or alive_neighbours > 3:
                return False
            return True
        else:
            if alive_neighbours == 3:
                return True
            return False

    @classmethod
    def next_state(cls, state: State) -> State:
        next_state = State(state.width, state.height)
        for y in range(state.height):
            for x in range(state.width):
                next_state[x, y] = cls._next_cell_state((x, y), state)
        return next_state
