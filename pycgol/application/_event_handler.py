"""Event handling for Conway's Game of Life application."""

from collections.abc import Callable

import pygame
import pygame_gui

from ..ui._ui import UI
from .._state import State
from ._game_loop import GameLoop


class EventHandler:
    """Handles pygame and UI events."""

    def __init__(self, ui: UI, game_loop: GameLoop) -> None:
        """
        Initialize the event handler.

        Args:
            ui: The UI instance to interact with
            game_loop: The game loop instance for pause control
        """
        self._ui = ui
        self._game_loop = game_loop
        self._engine_change_callback: Callable[[str], None] | None = None
        self._available_engines: list[str] = []
        self._current_engine_name: str = ""

    def set_engine_info(self, available_engines: list[str], current_engine_name: str) -> None:
        """
        Set engine information for context menu display.

        Args:
            available_engines: List of available engine names
            current_engine_name: Name of the currently active engine
        """
        self._available_engines = available_engines
        self._current_engine_name = current_engine_name

    def set_engine_change_callback(self, callback: Callable[[str], None]) -> None:
        """
        Set the callback function for engine changes.

        Args:
            callback: Function to call when user selects a new engine (receives engine name)
        """
        self._engine_change_callback = callback

    def handle_event(self, event: pygame.event.Event, state: State) -> bool:
        """
        Handle a single pygame event.

        Args:
            event: The pygame event to handle
            state: Current game state (for passing dimensions to UI)

        Returns:
            True if the application should quit, False otherwise
        """
        if event.type == pygame.QUIT:
            return True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button_down(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up(event)

        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

        elif event.type == pygame.MOUSEWHEEL:
            self._handle_mouse_wheel(event, state)

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            self._handle_button_pressed(event)

        elif event.type == pygame_gui.UI_WINDOW_CLOSE:
            self._handle_window_close()

        return False

    def _handle_mouse_button_down(self, event: pygame.event.Event) -> None:
        """Handle mouse button down events."""
        if event.button == 1:  # Left click
            if not self._ui.has_help_popup():
                # Close context menu if clicking outside of it
                if self._ui.has_context_menu() and not self._ui.is_click_inside_context_menu(event.pos):
                    self._ui.hide_context_menu()
                else:
                    self._ui.start_drag(event.pos)
        elif event.button == 3:  # Right click
            if not self._ui.has_help_popup():
                self._ui.show_context_menu(
                    event.pos,
                    self._game_loop.is_paused,
                    self._available_engines,
                    self._current_engine_name
                )

    def _handle_mouse_button_up(self, event: pygame.event.Event) -> None:
        """Handle mouse button up events."""
        if event.button == 1:  # Left release
            self._ui.end_drag()

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Handle mouse motion events."""
        self._ui.update_drag(event.pos)

    def _handle_mouse_wheel(self, event: pygame.event.Event, state: State) -> None:
        """Handle mouse wheel events."""
        if not self._ui.has_help_popup():
            mouse_pos = pygame.mouse.get_pos()
            self._ui.zoom(event.y, mouse_pos, state.width, state.height)

    def _handle_button_pressed(self, event: pygame.event.Event) -> None:
        """Handle UI button press events."""
        # Check if it's the pause button
        if self._ui.is_pause_button(event.ui_element):
            self._game_loop.toggle_pause()
            self._ui.hide_context_menu()
        # Check if it's an engine selection button
        elif (engine_name := self._ui.get_engine_from_button(event.ui_element)) is not None:
            if self._engine_change_callback is not None:
                self._engine_change_callback(engine_name)
                self._current_engine_name = engine_name  # Update for next menu display
            self._ui.hide_context_menu()
        # Check if it's the help button
        elif self._ui.is_help_button(event.ui_element):
            self._ui.show_help_popup()

    def _handle_window_close(self) -> None:
        """Handle window close events."""
        if self._ui.has_help_popup():
            self._ui.hide_help_popup()
