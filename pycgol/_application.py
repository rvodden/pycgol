import pygame
import pygame_gui

from ._state import State
from ._ui import UI
from ._model import Model

from .objects import Glider
    
_SCREEN_WIDTH: int = 1280
_SCREEN_HEIGHT: int = 720


class Application:

    def __init__(self, gol_updates_per_second: int = 10) -> None:
        pygame.init()
        self._manager = pygame_gui.UIManager((_SCREEN_WIDTH, _SCREEN_HEIGHT))
        self._ui = UI(_SCREEN_WIDTH, _SCREEN_HEIGHT, self._manager)
        self._state = State(_SCREEN_WIDTH // 10, _SCREEN_HEIGHT // 10)

        self._state = Glider.place((5, _SCREEN_HEIGHT // 10 - 5), self._state)
        self._clock = pygame.time.Clock()

        # Game of Life update rate control
        self._gol_update_interval = 1.0 / gol_updates_per_second
        self._time_since_last_update = 0.0

    def run(self) -> None:
        running = True

        while running:
            delta_t = self._clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self._manager.process_events(event)

            self._manager.update(delta_t)

            # Only update Game of Life state at configured rate
            self._time_since_last_update += delta_t
            if self._time_since_last_update >= self._gol_update_interval:
                self._state = Model.next_state(self._state)
                self._time_since_last_update = 0.0

            fps = self._clock.get_fps()
            self._ui.render(self._state, fps)

        pygame.quit()