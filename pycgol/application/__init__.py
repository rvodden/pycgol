"""Application components for Conway's Game of Life."""

from ._event_handler import EventHandler
from ._game_loop import GameLoop
from ._world_initializer import WorldInitializer

__all__ = ["EventHandler", "GameLoop", "WorldInitializer"]
