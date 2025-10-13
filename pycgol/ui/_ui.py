"""UI facade that coordinates viewport, components, and rendering."""

import pygame
import pygame_gui

from ..state import StateInterface
from ._viewport_manager import ViewportManager
from ._ui_components import UIComponents
from ._renderer import Renderer


class UI:
    """
    Facade for UI management, coordinating viewport, components, and rendering.

    This class delegates to specialized components:
    - ViewportManager: handles pan/zoom
    - UIComponents: handles buttons/menus/popups
    - Renderer: handles drawing to screen
    """

    def __init__(
        self,
        width: int,
        height: int,
        manager: pygame_gui.UIManager,
        cell_size: int = 10,
        viewport: ViewportManager | None = None,
        components: UIComponents | None = None,
        renderer: Renderer | None = None,
    ) -> None:
        """
        Initialize the UI facade with dependency injection.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            manager: pygame_gui UIManager instance
            cell_size: Initial size of each cell in pixels
            viewport: Optional ViewportManager instance (created if None)
            components: Optional UIComponents instance (created if None)
            renderer: Optional Renderer instance (created if None)
        """
        self._screen = pygame.display.set_mode((width, height))
        self._manager = manager

        # Use injected components or create defaults
        self._viewport = (
            viewport if viewport is not None else ViewportManager(cell_size)
        )
        self._components = (
            components
            if components is not None
            else UIComponents(manager, width, height)
        )
        self._renderer = (
            renderer if renderer is not None else Renderer(self._screen, manager)
        )

    # Viewport delegation methods
    def set_viewport(self, x: int, y: int) -> None:
        """Set the viewport position."""
        self._viewport.set_viewport(x, y)

    def start_drag(self, mouse_pos: tuple[int, int]) -> None:
        """Start panning with mouse drag."""
        self._viewport.start_drag(mouse_pos)

    def update_drag(self, mouse_pos: tuple[int, int]) -> None:
        """Update viewport position during drag."""
        self._viewport.update_drag(mouse_pos)

    def end_drag(self) -> None:
        """End panning drag."""
        self._viewport.end_drag()

    def zoom(
        self,
        delta: int,
        mouse_pos: tuple[int, int],
        max_grid_width: int,
        max_grid_height: int,
    ) -> None:
        """Zoom in or out, keeping the mouse position stable."""
        self._viewport.zoom(
            delta,
            mouse_pos,
            self._screen.get_width(),
            self._screen.get_height(),
            max_grid_width,
            max_grid_height,
        )

    # UI Components delegation methods
    def show_context_menu(
        self, position: tuple[int, int], is_paused: bool, available_engines: list[str], current_engine: str, fps_limit: int = 60
    ) -> None:
        """Show context menu at the given position with engine selection and FPS limit toggle."""
        self._components.show_context_menu(position, is_paused, available_engines, current_engine, fps_limit)

    def hide_context_menu(self) -> None:
        """Hide the context menu."""
        self._components.hide_context_menu()

    def has_context_menu(self) -> bool:
        """Check if context menu is visible."""
        return self._components.has_context_menu()

    def is_click_inside_context_menu(self, position: tuple[int, int]) -> bool:
        """Check if a click position is inside the context menu."""
        return self._components.is_click_inside_context_menu(position)

    def is_pause_button(self, ui_element: pygame_gui.core.UIElement) -> bool:
        """Check if UI element is the pause button."""
        return self._components.is_pause_button(ui_element)

    def is_fps_limit_button(self, ui_element: pygame_gui.core.UIElement) -> bool:
        """Check if UI element is the FPS limit button."""
        return self._components.is_fps_limit_button(ui_element)

    def get_engine_from_button(self, ui_element: pygame_gui.core.UIElement) -> str | None:
        """Get engine name if UI element is an engine selection button."""
        return self._components.get_engine_from_button(ui_element)

    def is_help_button(self, ui_element: pygame_gui.core.UIElement) -> bool:
        """Check if UI element is the help button."""
        return self._components.is_help_button(ui_element)

    def show_help_popup(self) -> None:
        """Show help popup with usage instructions."""
        self._components.show_help_popup()

    def hide_help_popup(self) -> None:
        """Hide the help popup."""
        self._components.hide_help_popup()

    def has_help_popup(self) -> bool:
        """Check if help popup is visible."""
        return self._components.has_help_popup()

    # Rendering delegation method
    def render(self, state: StateInterface, fps: float = 0.0) -> None:
        """Render the game state and UI."""
        self._renderer.render(state, self._viewport, fps)
