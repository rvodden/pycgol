import pygame
import pygame_gui

from .ui._ui import UI
from .engines import Engine, EngineRegistry, LoopEngine, NumpyEngine
from .application import EventHandler, GameLoop, WorldInitializer

_SCREEN_WIDTH: int = 1280
_SCREEN_HEIGHT: int = 720
_CELL_SIZE: int = 10
_BORDER_CELLS: int = 100  # Large border for exploration


class Application:
    def __init__(
        self,
        gol_updates_per_second: int = 10,
        engine: type[Engine] = NumpyEngine,
        engine_registry: EngineRegistry | None = None,
        world_initializer: WorldInitializer | None = None,
        game_loop: GameLoop | None = None,
        event_handler: EventHandler | None = None
    ) -> None:
        """
        Initialize the Application.

        Args:
            gol_updates_per_second: Number of game state updates per second
            engine: Initial engine class to use
            engine_registry: Optional custom engine registry
            world_initializer: Optional custom world initializer
            game_loop: Optional custom game loop
            event_handler: Optional custom event handler
        """
        pygame.init()
        self._manager = pygame_gui.UIManager((_SCREEN_WIDTH, _SCREEN_HEIGHT))

        # Preload fonts to avoid warnings
        self._manager.preload_fonts(
            [
                {
                    "name": "noto_sans",
                    "point_size": 14,
                    "style": "bold",
                    "antialiased": "1",
                }
            ]
        )

        self._ui = UI(_SCREEN_WIDTH, _SCREEN_HEIGHT, self._manager, _CELL_SIZE)

        # Initialize world
        if world_initializer is None:
            world_initializer = WorldInitializer(
                _SCREEN_WIDTH, _SCREEN_HEIGHT, _CELL_SIZE, _BORDER_CELLS
            )
        self._world_initializer = world_initializer
        self._state = world_initializer.create_initial_state()

        # Set initial viewport position
        viewport_x, viewport_y = world_initializer.get_initial_viewport_position()
        self._ui.set_viewport(viewport_x, viewport_y)

        # Initialize game loop
        if game_loop is None:
            game_loop = GameLoop(gol_updates_per_second)
        self._game_loop = game_loop

        # Initialize event handler
        if event_handler is None:
            event_handler = EventHandler(self._ui, self._game_loop)
        self._event_handler = event_handler

        self._clock = pygame.time.Clock()

        # Engine registry for runtime engine switching
        if engine_registry is None:
            self._engine_registry = EngineRegistry()
            self._engine_registry.register("numpy", NumpyEngine, is_default=True)
            self._engine_registry.register("loop", LoopEngine)
        else:
            self._engine_registry = engine_registry

        # Set current engine (for backward compatibility with direct engine parameter)
        self._engine = engine

        # Find the name of the current engine in the registry
        current_engine_name = "numpy"  # default
        for name in self._engine_registry.list_engines():
            if self._engine_registry.get(name) == self._engine:
                current_engine_name = name
                break

        # Configure event handler with engine information
        self._event_handler.set_engine_info(
            self._engine_registry.list_engines(),
            current_engine_name
        )
        self._event_handler.set_engine_change_callback(self.set_engine_by_name)

    def get_engine_registry(self) -> EngineRegistry:
        """Get the engine registry."""
        return self._engine_registry

    def get_current_engine(self) -> type[Engine]:
        """Get the currently active engine."""
        return self._engine

    def set_engine(self, engine: type[Engine]) -> None:
        """
        Set the current engine.

        Args:
            engine: The engine class to use for next_state calculations
        """
        self._engine = engine

    def set_engine_by_name(self, name: str) -> None:
        """
        Set the current engine by registry name.

        Args:
            name: The name of the engine in the registry

        Raises:
            KeyError: If no engine with the given name is registered
        """
        self._engine = self._engine_registry.get(name)

    def run(self) -> None:
        """Run the main game loop."""
        running = True

        while running:
            delta_t = self._clock.tick(60) / 1000.0

            # Process events
            for event in pygame.event.get():
                self._manager.process_events(event)

                # Handle event and check if we should quit
                should_quit = self._event_handler.handle_event(event, self._state)
                if should_quit:
                    running = False

            # Update UI manager
            self._manager.update(delta_t)

            # Update game state
            self._state = self._game_loop.update(delta_t, self._state, self._engine)

            # Render
            fps = self._clock.get_fps()
            self._ui.render(self._state, fps)

        pygame.quit()
