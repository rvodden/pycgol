import pygame
import pygame_gui

from ._state import State
from ._ui import UI
from ._model import Model

from .objects import GliderGun
    
_SCREEN_WIDTH: int = 1280
_SCREEN_HEIGHT: int = 720
_CELL_SIZE: int = 10
_BORDER_CELLS: int = 15  # Extra cells beyond the viewport edge for gliders to travel


class Application:

    def __init__(self, gol_updates_per_second: int = 10) -> None:
        pygame.init()
        self._manager = pygame_gui.UIManager((_SCREEN_WIDTH, _SCREEN_HEIGHT))
        self._ui = UI(_SCREEN_WIDTH, _SCREEN_HEIGHT, self._manager, _CELL_SIZE)

        # Calculate grid dimensions: viewport cells + border on all sides
        viewport_cells_width = _SCREEN_WIDTH // _CELL_SIZE
        viewport_cells_height = _SCREEN_HEIGHT // _CELL_SIZE
        grid_width = viewport_cells_width + (2 * _BORDER_CELLS)
        grid_height = viewport_cells_height + (2 * _BORDER_CELLS)

        self._state = State(grid_width, grid_height)

        # Center the viewport on the grid (offset by border cells)
        self._ui.set_viewport(_BORDER_CELLS, _BORDER_CELLS)

        # Place first glider gun in top-left, shooting down-right
        # Gun is 36 cells wide and 9 cells tall
        gun1_x = _BORDER_CELLS + 10  # 10 cells from left edge
        gun1_y = _BORDER_CELLS + 10  # 10 cells from top edge
        self._state = GliderGun.place((gun1_x, gun1_y), self._state, rotation=0)

        # Place second glider gun rotated 90 degrees to shoot down-left
        # Position it to the right so the glider streams will collide
        # The first gun shoots from (gun1_x, gun1_y) diagonally down-right
        # Gliders travel at 45 degrees, so after T steps, glider is at (gun1_x+T, gun1_y+T)
        # Second gun at 90° shoots down-left, so gliders go (gun2_x-T, gun2_y+T)
        # For collision: gun1_x + T = gun2_x - T, so gun2_x = gun1_x + 2T
        # With T ≈ 40 steps for mid-screen collision: gun2_x ≈ gun1_x + 80
        gun2_x = gun1_x + 80
        gun2_y = gun1_y
        self._state = GliderGun.place((gun2_x, gun2_y), self._state, rotation=90)

        self._clock = pygame.time.Clock()

        # Game of Life update rate control
        self._gol_update_interval = 1.0 / gol_updates_per_second
        self._time_since_last_update = 0.0
        self._paused = False

    def run(self) -> None:
        running = True

        while running:
            delta_t = self._clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self._manager.process_events(event)

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # Right click - show context menu
                    self._ui.show_context_menu(event.pos, self._paused)
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # Check if this is our context menu button
                    if self._ui.is_context_menu_button(event.ui_element):
                        self._paused = not self._paused
                        self._ui.hide_context_menu()

            self._manager.update(delta_t)

            # Only update Game of Life state at configured rate and when not paused
            if not self._paused:
                self._time_since_last_update += delta_t
                if self._time_since_last_update >= self._gol_update_interval:
                    self._state = Model.next_state(self._state)
                    self._time_since_last_update = 0.0

            fps = self._clock.get_fps()
            self._ui.render(self._state, fps)

        pygame.quit()