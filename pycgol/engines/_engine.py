from abc import ABC, abstractmethod
from .._state import State

"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""


class Engine(ABC):
    """Base class for Game of Life engine implementations."""

    @classmethod
    @abstractmethod
    def next_state(cls, state: State) -> State:
        """Calculate the next generation of the Game of Life."""
        pass
