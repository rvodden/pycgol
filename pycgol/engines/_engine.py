"""Base class for Game of Life engines.

Conway's Game of Life Rules:
- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

from abc import ABC, abstractmethod
from ..state import StateInterface


class Engine(ABC):
    """Base class for Game of Life engine implementations.

    Engines can optionally declare a preferred_state_type to optimize performance.
    The optimize_state method will convert states to the preferred type when beneficial.
    """

    # Optional: declare preferred state type for this engine
    # Set to None if engine works equally well with any state type
    preferred_state_type: type[StateInterface] | None = None

    @classmethod
    @abstractmethod
    def next_state(cls, state: StateInterface) -> StateInterface:
        """
        Calculate the next generation of the Game of Life.

        Args:
            state: Current state (any StateInterface implementation)

        Returns:
            New state for next generation (type may change based on engine preference)
        """
        pass

    @classmethod
    def optimize_state(cls, state: StateInterface) -> StateInterface:
        """
        Convert state to preferred type if beneficial.

        This method is called by engines that have a preferred_state_type.
        It converts the state on the first call after an engine switch,
        then subsequent calls are fast since the state type matches.

        Args:
            state: Current state (any type)

        Returns:
            State converted to preferred type, or original if no preference
        """
        # If no preference, return unchanged
        if cls.preferred_state_type is None:
            return state

        # If already correct type, return unchanged
        if isinstance(state, cls.preferred_state_type):
            return state

        # Convert to preferred type
        return cls.preferred_state_type.from_state(state)
