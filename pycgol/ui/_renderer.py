"""Rendering of Game of Life state to the screen."""

import pygame
import pygame_gui

from ..state import State
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

        # Fill the in-bounds area with black
        # Calculate the screen-space rectangle that corresponds to the in-bounds grid area
        viewport_start_x = max(0, -viewport.viewport_x)
        viewport_start_y = max(0, -viewport.viewport_y)
        viewport_cells_width = self._screen.get_width() // viewport.cell_size
        viewport_cells_height = self._screen.get_height() // viewport.cell_size
        viewport_end_x = min(viewport_cells_width, state.width - viewport.viewport_x)
        viewport_end_y = min(viewport_cells_height, state.height - viewport.viewport_y)

        if viewport_end_x > viewport_start_x and viewport_end_y > viewport_start_y:
            pygame.draw.rect(
                self._screen,
                "black",
                pygame.Rect(
                    viewport_start_x * viewport.cell_size,
                    viewport_start_y * viewport.cell_size,
                    (viewport_end_x - viewport_start_x) * viewport.cell_size,
                    (viewport_end_y - viewport_start_y) * viewport.cell_size,
                ),
            )

        # Draw only live cells (more efficient than checking every cell)
        for grid_x, grid_y in state.get_live_cells():
            # Check if the live cell is within the viewport
            viewport_x = grid_x - viewport.viewport_x
            viewport_y = grid_y - viewport.viewport_y

            if (0 <= viewport_x < viewport_cells_width and
                0 <= viewport_y < viewport_cells_height):
                # Draw white cell
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
