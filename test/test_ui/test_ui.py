from unittest.mock import Mock, patch

from pycgol.ui._ui import UI
from pycgol.state import DenseState


class TestUI:
    """Test the UI facade - it should delegate to its components."""

    @patch("pycgol.ui._ui.pygame")
    @patch("pycgol.ui._ui.UIComponents")
    @patch("pycgol.ui._ui.ViewportManager")
    @patch("pycgol.ui._ui.Renderer")
    def test_ui_initialization_with_defaults(
        self, mock_renderer_cls, mock_viewport_cls, mock_components_cls, mock_pygame
    ):
        """Test that UI creates default components when none provided."""
        mock_display = Mock()
        mock_pygame.display.set_mode.return_value = mock_display
        mock_manager = Mock()

        ui = UI(800, 600, mock_manager, cell_size=10)

        # Check screen setup
        mock_pygame.display.set_mode.assert_called_once_with((800, 600))
        assert ui._screen == mock_display
        assert ui._manager == mock_manager
        # Verify factories were called to create components
        mock_viewport_cls.assert_called_once_with(10)
        mock_components_cls.assert_called_once_with(mock_manager, 800, 600)
        mock_renderer_cls.assert_called_once_with(mock_display, mock_manager)

    @patch("pycgol.ui._ui.pygame")
    def test_ui_initialization_with_injected_components(self, mock_pygame):
        """Test that UI uses injected components."""
        mock_display = Mock()
        mock_pygame.display.set_mode.return_value = mock_display
        mock_manager = Mock()

        # Create mock components
        mock_viewport = Mock()
        mock_components = Mock()
        mock_renderer = Mock()

        ui = UI(
            800,
            600,
            mock_manager,
            cell_size=10,
            viewport=mock_viewport,
            components=mock_components,
            renderer=mock_renderer,
        )

        # Verify injected components are used
        assert ui._viewport is mock_viewport
        assert ui._components is mock_components
        assert ui._renderer is mock_renderer

    @patch("pycgol.ui._ui.pygame")
    def test_set_viewport_delegates(self, mock_pygame):
        """Test that set_viewport delegates to ViewportManager."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_viewport = Mock()

        ui = UI(
            800, 600, Mock(), cell_size=10, viewport=mock_viewport, components=Mock()
        )
        ui.set_viewport(5, 10)

        mock_viewport.set_viewport.assert_called_once_with(5, 10)

    @patch("pycgol.ui._ui.pygame")
    def test_start_drag_delegates(self, mock_pygame):
        """Test that start_drag delegates to ViewportManager."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_viewport = Mock()

        ui = UI(
            800, 600, Mock(), cell_size=10, viewport=mock_viewport, components=Mock()
        )
        ui.start_drag((100, 200))

        mock_viewport.start_drag.assert_called_once_with((100, 200))

    @patch("pycgol.ui._ui.pygame")
    def test_update_drag_delegates(self, mock_pygame):
        """Test that update_drag delegates to ViewportManager."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_viewport = Mock()

        ui = UI(
            800, 600, Mock(), cell_size=10, viewport=mock_viewport, components=Mock()
        )
        ui.update_drag((130, 120))

        mock_viewport.update_drag.assert_called_once_with((130, 120))

    @patch("pycgol.ui._ui.pygame")
    def test_end_drag_delegates(self, mock_pygame):
        """Test that end_drag delegates to ViewportManager."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_viewport = Mock()

        ui = UI(
            800, 600, Mock(), cell_size=10, viewport=mock_viewport, components=Mock()
        )
        ui.end_drag()

        mock_viewport.end_drag.assert_called_once()

    @patch("pycgol.ui._ui.pygame")
    def test_zoom_delegates(self, mock_pygame):
        """Test that zoom delegates to ViewportManager."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 800
        mock_screen.get_height.return_value = 600
        mock_pygame.display.set_mode.return_value = mock_screen
        mock_viewport = Mock()

        ui = UI(
            800, 600, Mock(), cell_size=10, viewport=mock_viewport, components=Mock()
        )
        ui.zoom(1, (400, 300), 100, 100)

        mock_viewport.zoom.assert_called_once_with(1, (400, 300), 800, 600, 100, 100)

    @patch("pycgol.ui._ui.pygame")
    def test_show_context_menu_delegates(self, mock_pygame):
        """Test that show_context_menu delegates to UIComponents."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_components = Mock()

        ui = UI(800, 600, Mock(), cell_size=10, components=mock_components)
        ui.show_context_menu((100, 200), is_paused=False, available_engines=["numpy", "loop"], current_engine="numpy", fps_limit=60)

        mock_components.show_context_menu.assert_called_once_with((100, 200), False, ["numpy", "loop"], "numpy", 60)

    @patch("pycgol.ui._ui.pygame")
    def test_hide_context_menu_delegates(self, mock_pygame):
        """Test that hide_context_menu delegates to UIComponents."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_components = Mock()

        ui = UI(800, 600, Mock(), cell_size=10, components=mock_components)
        ui.hide_context_menu()

        mock_components.hide_context_menu.assert_called_once()

    @patch("pycgol.ui._ui.pygame")
    def test_has_context_menu_delegates(self, mock_pygame):
        """Test that has_context_menu delegates to UIComponents."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_components = Mock()
        mock_components.has_context_menu.return_value = True

        ui = UI(800, 600, Mock(), cell_size=10, components=mock_components)
        result = ui.has_context_menu()

        assert result is True
        mock_components.has_context_menu.assert_called_once()

    @patch("pycgol.ui._ui.pygame")
    def test_is_click_inside_context_menu_delegates(self, mock_pygame):
        """Test that is_click_inside_context_menu delegates to UIComponents."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_components = Mock()
        mock_components.is_click_inside_context_menu.return_value = True

        ui = UI(800, 600, Mock(), cell_size=10, components=mock_components)
        result = ui.is_click_inside_context_menu((100, 200))

        assert result is True
        mock_components.is_click_inside_context_menu.assert_called_once_with((100, 200))

    @patch("pycgol.ui._ui.pygame")
    def test_show_help_popup_delegates(self, mock_pygame):
        """Test that show_help_popup delegates to UIComponents."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_components = Mock()

        ui = UI(800, 600, Mock(), cell_size=10, components=mock_components)
        ui.show_help_popup()

        mock_components.show_help_popup.assert_called_once()

    @patch("pycgol.ui._ui.pygame")
    def test_render_delegates(self, mock_pygame):
        """Test that render delegates to Renderer."""
        mock_pygame.display.set_mode.return_value = Mock()
        mock_renderer = Mock()
        mock_viewport = Mock()

        ui = UI(
            800,
            600,
            Mock(),
            cell_size=10,
            viewport=mock_viewport,
            renderer=mock_renderer,
            components=Mock(),
        )
        state = DenseState(10, 10)
        ui.render(state, fps=60.0)

        mock_renderer.render.assert_called_once_with(state, mock_viewport, 60.0)
