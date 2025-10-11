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

    def render(self, state: State):
        self._screen.fill("black")

        rectangle_width = self._screen.get_width() / state.width
        rectangle_height = self._screen.get_height() / state.height

        for y in range(state.height):
            for x in range(state.width):
                pygame.draw.rect(
                    self._screen,
                    "white" if state[x,y] else "black",
                    pygame.Rect(x * rectangle_width, y * rectangle_height, 
                                rectangle_width, rectangle_height)
                )
        
        self._manager.draw_ui(self._screen)

        pygame.display.flip()
