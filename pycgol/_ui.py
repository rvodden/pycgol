import pygame
import pygame_gui

from ._state import State

class UI:
    def __init__(self, width: int, height: int, manager: pygame_gui.UIManager) -> None:
        self._screen = pygame.display.set_mode((width, height))
        self._manager = manager

        self._button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250,275),(100, 50)),
            text='Say Hello!',
            manager = self._manager
        )

    def render(self, state: State, fps: float = 0.0):
        self._screen.fill("black")

        rectangle_width = self._screen.get_width() / state.width
        rectangle_height = self._screen.get_height() / state.height

        # Only draw alive cells (much faster than drawing all cells)
        for y in range(state.height):
            for x in range(state.width):
                if state[x, y]:
                    pygame.draw.rect(
                        self._screen,
                        "white",
                        pygame.Rect(x * rectangle_width, y * rectangle_height,
                                    rectangle_width, rectangle_height)
                    )

        # Render FPS counter in top right corner
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {fps:.1f}", True, (0, 255, 0))
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (self._screen.get_width() - 10, 10)
        self._screen.blit(fps_text, fps_rect)

        self._manager.draw_ui(self._screen)

        pygame.display.flip()
