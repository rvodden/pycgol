"""Game loop and timing management for Conway's Game of Life."""

from .._state import State
from ..engines import Engine


class GameLoop:
    """Manages the game loop, timing, and update rate control."""

    def __init__(self, updates_per_second: int = 10) -> None:
        """
        Initialize the game loop.

        Args:
            updates_per_second: Number of game state updates per second
        """
        self._update_interval = 1.0 / updates_per_second
        self._time_since_last_update = 0.0
        self._paused = False

    @property
    def is_paused(self) -> bool:
        """Check if the game is paused."""
        return self._paused

    def pause(self) -> None:
        """Pause the game."""
        self._paused = True

    def resume(self) -> None:
        """Resume the game."""
        self._paused = False

    def toggle_pause(self) -> None:
        """Toggle pause state."""
        self._paused = not self._paused

    def update(self, delta_t: float, state: State, engine: type[Engine]) -> State:
        """
        Update the game state based on elapsed time.

        Args:
            delta_t: Time elapsed since last update in seconds
            state: Current game state
            engine: Engine to use for state calculations

        Returns:
            Updated state (may be the same object if not updated)
        """
        if self._paused:
            return state

        self._time_since_last_update += delta_t

        if self._time_since_last_update >= self._update_interval:
            state = engine.next_state(state)
            self._time_since_last_update = 0.0

        return state
