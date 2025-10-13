"""Rendering of Game of Life state to the screen."""

import pygame
import pygame_gui

from .._state import State
from ._viewport_manager import ViewportManager


class Renderer:
    """Handles rendering of the game state and UI elements."""

    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager) -> None:
        """
        Initialize the renderer.

        Args:
            screen: pygame display surface to render to
            manager: pygame_gui UIManager for UI elements
        """
        self._screen = screen
        self._manager = manager

    def render(self, state: State, viewport: ViewportManager, fps: float = 0.0) -> None:
        """
        Render the game state and UI.

        Args:
            state: Current game state
            viewport: Viewport manager for camera position and zoom
            fps: Current frames per second
        """
        # Fill with dark blue for out-of-bounds area
        self._screen.fill((20, 30, 60))

        # Calculate how many cells fit in the viewport
        viewport_cells_width = self._screen.get_width() // viewport.cell_size
        viewport_cells_height = self._screen.get_height() // viewport.cell_size

        # Draw background for in-bounds area and cells
        for viewport_y in range(viewport_cells_height):
            for viewport_x in range(viewport_cells_width):
                # Calculate the corresponding position in the game grid
                grid_x = viewport.viewport_x + viewport_x
                grid_y = viewport.viewport_y + viewport_y

                # Check if this position is within the game grid bounds
                if 0 <= grid_x < state.width and 0 <= grid_y < state.height:
                    # Draw black background for in-bounds cells
                    pygame.draw.rect(
                        self._screen,
                        "black",
                        pygame.Rect(
                            viewport_x * viewport.cell_size,
                            viewport_y * viewport.cell_size,
                            viewport.cell_size,
                            viewport.cell_size,
                        ),
                    )
                    # Draw white cell if alive
                    if state[grid_x, grid_y]:
                        pygame.draw.rect(
                            self._screen,
                            "white",
                            pygame.Rect(
                                viewport_x * viewport.cell_size,
                                viewport_y * viewport.cell_size,
                                viewport.cell_size,
                                viewport.cell_size,
                            ),
                        )

        # Render FPS counter in top right corner with monospaced font
        font = pygame.font.SysFont("monospace", 24, bold=True)
        fps_text = font.render(f"FPS: {fps:5.1f}", True, (0, 255, 0))
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (self._screen.get_width() - 10, 10)
        self._screen.blit(fps_text, fps_rect)

        # Draw UI elements
        self._manager.draw_ui(self._screen)

        # Update display
        pygame.display.flip()
