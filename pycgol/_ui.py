import pygame
import pygame_gui

from ._state import State

class UI:
    def __init__(self, width: int, height: int, manager: pygame_gui.UIManager, cell_size: int = 10) -> None:
        self._screen = pygame.display.set_mode((width, height))
        self._manager = manager
        self._context_menu = None
        self._cell_size = cell_size

        # Viewport settings - which part of the game grid we're looking at
        self._viewport_x = 0
        self._viewport_y = 0

    def show_context_menu(self, position: tuple[int, int], is_paused: bool) -> None:
        """Show context menu at the given position with play/pause option."""
        if self._context_menu is not None:
            self._context_menu.kill()

        button_text = "Resume" if is_paused else "Pause"

        self._context_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, (100, 40)),
            text=button_text,
            manager=self._manager,
            object_id="#context_menu_button"
        )

    def hide_context_menu(self) -> None:
        """Hide the context menu if it's visible."""
        if self._context_menu is not None:
            self._context_menu.kill()
            self._context_menu = None

    def has_context_menu(self) -> bool:
        """Check if context menu is currently visible."""
        return self._context_menu is not None

    def is_context_menu_button(self, ui_element) -> bool:
        """Check if the given UI element is the context menu button."""
        return self._context_menu is not None and ui_element == self._context_menu

    def set_viewport(self, x: int, y: int) -> None:
        """Set the viewport position (which part of the game grid to display)."""
        self._viewport_x = x
        self._viewport_y = y

    def render(self, state: State, fps: float = 0.0):
        self._screen.fill("black")

        # Calculate how many cells fit in the viewport
        viewport_cells_width = self._screen.get_width() // self._cell_size
        viewport_cells_height = self._screen.get_height() // self._cell_size

        # Only draw alive cells within the viewport
        for viewport_y in range(viewport_cells_height):
            for viewport_x in range(viewport_cells_width):
                # Calculate the corresponding position in the game grid
                grid_x = self._viewport_x + viewport_x
                grid_y = self._viewport_y + viewport_y

                # Check if this position is within the game grid bounds
                if 0 <= grid_x < state.width and 0 <= grid_y < state.height:
                    if state[grid_x, grid_y]:
                        pygame.draw.rect(
                            self._screen,
                            "white",
                            pygame.Rect(viewport_x * self._cell_size,
                                       viewport_y * self._cell_size,
                                       self._cell_size,
                                       self._cell_size)
                        )

        # Render FPS counter in top right corner with monospaced font
        font = pygame.font.SysFont('monospace', 24, bold=True)
        fps_text = font.render(f"FPS: {fps:5.1f}", True, (0, 255, 0))
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (self._screen.get_width() - 10, 10)
        self._screen.blit(fps_text, fps_rect)

        self._manager.draw_ui(self._screen)

        pygame.display.flip()
