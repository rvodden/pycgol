"""UI components for buttons, menus, and popups."""

import pygame
import pygame_gui


class UIComponents:
    """Manages UI elements like buttons, context menus, and popups."""

    def __init__(
        self, manager: pygame_gui.UIManager, screen_width: int, screen_height: int
    ) -> None:
        """
        Initialize UI components.

        Args:
            manager: pygame_gui UIManager instance
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
        """
        self._manager = manager
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._context_menu_panel: pygame_gui.elements.UIPanel | None = None
        self._context_menu_buttons: dict[str, pygame_gui.elements.UIButton] = {}
        self._help_popup: pygame_gui.windows.UIMessageWindow | None = None

        # Create help button in bottom left corner
        self._help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, screen_height - 50), (40, 40)),
            text="?",
            manager=self._manager,
            object_id="#help_button",
        )

    def show_context_menu(
        self, position: tuple[int, int], is_paused: bool, available_engines: list[str], current_engine: str, fps_limit: int = 60
    ) -> None:
        """
        Show context menu at the given position with play/pause, FPS limit toggle, and engine selection.

        Args:
            position: Screen position for the menu
            is_paused: Whether the game is currently paused
            available_engines: List of available engine names
            current_engine: Name of the currently active engine
            fps_limit: Current FPS limit (60 for limited, 0 for unlimited)
        """
        self.hide_context_menu()

        # Calculate menu size based on number of items
        button_height = 35
        button_width = 150
        menu_height = button_height * (3 + len(available_engines))  # Pause + FPS limit + separator + engines
        menu_width = button_width

        # Create panel for the menu
        self._context_menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(position, (menu_width, menu_height)),
            manager=self._manager,
            object_id="#context_menu_panel",
        )

        # Add pause/resume button
        button_text = "Resume" if is_paused else "Pause"
        pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (button_width, button_height)),
            text=button_text,
            manager=self._manager,
            container=self._context_menu_panel,
            object_id="#pause_button",
        )
        self._context_menu_buttons["pause"] = pause_button

        # Add FPS limit toggle button
        y_offset = button_height
        fps_text = "[*] Limit 60 FPS" if fps_limit == 60 else "    Limit 60 FPS"
        fps_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, y_offset), (button_width, button_height)),
            text=fps_text,
            manager=self._manager,
            container=self._context_menu_panel,
            object_id="#fps_limit_button",
        )
        self._context_menu_buttons["fps_limit"] = fps_button

        # Add engine selection buttons
        y_offset += button_height
        for engine_name in available_engines:
            # Use [*] as indicator since ✓ may not render in default font
            button_text = f"[*] {engine_name}" if engine_name == current_engine else f"    {engine_name}"
            engine_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((0, y_offset), (button_width, button_height)),
                text=button_text,
                manager=self._manager,
                container=self._context_menu_panel,
                object_id=f"#engine_{engine_name}",
            )
            self._context_menu_buttons[f"engine_{engine_name}"] = engine_button
            y_offset += button_height

    def hide_context_menu(self) -> None:
        """Hide the context menu if it's visible."""
        if self._context_menu_panel is not None:
            self._context_menu_panel.kill()
            self._context_menu_panel = None
        self._context_menu_buttons.clear()

    def has_context_menu(self) -> bool:
        """Check if context menu is currently visible."""
        return self._context_menu_panel is not None

    def is_click_inside_context_menu(self, position: tuple[int, int]) -> bool:
        """
        Check if a click position is inside the context menu.

        Args:
            position: Screen position (x, y) of the click

        Returns:
            True if click is inside context menu, False otherwise
        """
        if self._context_menu_panel is None:
            return False

        rect = self._context_menu_panel.get_abs_rect()
        x, y = position
        return rect.collidepoint(x, y)

    def is_pause_button(self, ui_element: pygame_gui.core.UIElement) -> bool:
        """Check if the given UI element is the pause button."""
        return "pause" in self._context_menu_buttons and ui_element == self._context_menu_buttons["pause"]

    def is_fps_limit_button(self, ui_element: pygame_gui.core.UIElement) -> bool:
        """Check if the given UI element is the FPS limit button."""
        return "fps_limit" in self._context_menu_buttons and ui_element == self._context_menu_buttons["fps_limit"]

    def get_engine_from_button(self, ui_element: pygame_gui.core.UIElement) -> str | None:
        """
        Get the engine name if the UI element is an engine selection button.

        Args:
            ui_element: The UI element to check

        Returns:
            Engine name if this is an engine button, None otherwise
        """
        for key, button in self._context_menu_buttons.items():
            if button == ui_element and key.startswith("engine_"):
                return key.replace("engine_", "")
        return None

    def is_help_button(self, ui_element: pygame_gui.core.UIElement) -> bool:
        """Check if the given UI element is the help button."""
        return ui_element == self._help_button

    def show_help_popup(self) -> None:
        """Show help popup with usage instructions."""
        if self._help_popup is not None:
            return  # Already showing

        help_text = """<b>Conway's Game of Life - Controls</b><br>
<b>Mouse Controls:</b><br>
* Left Click + Drag: Pan the view<br>
* Mouse Wheel: Zoom in/out<br>
* Right Click: Open context menu<br>
  - Pause/Resume simulation<br>
  - Toggle FPS limit (60 FPS / unlimited)<br>
  - Switch between engines (numpy/loop/sparse)<br>
* Left Click outside menu: Close menu<br>
* Click '?' button: Show this help<br>
<br>
<b>About:</b><br>
Two Gosper's Glider Guns are placed to create colliding glider streams.
"""

        popup_width = 400
        popup_height = 350

        self._help_popup = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect(
                (self._screen_width - popup_width) // 2,
                (self._screen_height - popup_height) // 2,
                popup_width,
                popup_height,
            ),
            html_message=help_text,
            manager=self._manager,
            window_title="Help",
        )

    def hide_help_popup(self) -> None:
        """Hide the help popup if it's visible."""
        if self._help_popup is not None:
            self._help_popup.kill()
            self._help_popup = None

    def has_help_popup(self) -> bool:
        """Check if help popup is currently visible."""
        return self._help_popup is not None
