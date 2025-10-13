from unittest.mock import Mock, patch


from pycgol.ui._ui_components import UIComponents


class TestUIComponents:
    """Test the UIComponents class."""

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_init_creates_help_button(self, mock_button_class):
        """Test that UIComponents creates a help button on initialization."""
        mock_manager = Mock()

        _ = UIComponents(mock_manager, 800, 600)

        # Should create help button with correct parameters
        mock_button_class.assert_called_once()
        call_args = mock_button_class.call_args

        # Check the button text is "?"
        assert call_args.kwargs["text"] == "?"
        assert call_args.kwargs["manager"] == mock_manager
        assert call_args.kwargs["object_id"] == "#help_button"

        # Check button position (bottom left: 10px from left, 50px from bottom)
        rect = call_args.kwargs["relative_rect"]
        assert rect.topleft == (10, 550)  # 600 - 50 = 550
        assert rect.size == (40, 40)

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_when_paused(self, mock_button_class, mock_panel_class):
        """Test showing context menu with 'Resume' text when paused."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Reset mock to ignore help button creation
        mock_button_class.reset_mock()

        components.show_context_menu((100, 200), is_paused=True, available_engines=["numpy", "loop"], current_engine="numpy")

        # Should create button with "Resume" text
        calls = mock_button_class.call_args_list
        pause_button_call = calls[0]
        assert pause_button_call.kwargs["text"] == "Resume"
        assert pause_button_call.kwargs["object_id"] == "#pause_button"

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_when_not_paused(self, mock_button_class, mock_panel_class):
        """Test showing context menu with 'Pause' text when not paused."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Reset mock to ignore help button creation
        mock_button_class.reset_mock()

        components.show_context_menu((100, 200), is_paused=False, available_engines=["numpy", "loop"], current_engine="numpy")

        # Should create button with "Pause" text
        calls = mock_button_class.call_args_list
        pause_button_call = calls[0]
        assert pause_button_call.kwargs["text"] == "Pause"

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_at_position(self, mock_button_class, mock_panel_class):
        """Test that context menu is created at the correct position."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Reset mock to ignore help button creation
        mock_button_class.reset_mock()

        components.show_context_menu((150, 250), is_paused=False, available_engines=["numpy"], current_engine="numpy")

        # Check panel position
        panel_call_args = mock_panel_class.call_args
        rect = panel_call_args.kwargs["relative_rect"]
        assert rect.topleft == (150, 250)

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_replaces_existing(self, mock_button_class, mock_panel_class):
        """Test that showing context menu kills existing menu."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Show first menu
        mock_button_class.reset_mock()
        mock_panel_class.reset_mock()
        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        first_panel = components._context_menu_panel

        # Show second menu
        components.show_context_menu((200, 200), is_paused=True, available_engines=["numpy"], current_engine="numpy")

        # First menu should be killed
        first_panel.kill.assert_called_once()

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_hide_context_menu(self, mock_button_class, mock_panel_class):
        """Test hiding context menu."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Show menu
        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        panel = components._context_menu_panel

        # Hide menu
        components.hide_context_menu()

        # Should kill the panel and set to None
        panel.kill.assert_called_once()
        assert components._context_menu_panel is None

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_hide_context_menu_when_none(self, mock_button_class):
        """Test that hiding context menu when none exists doesn't error."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Should not raise exception
        components.hide_context_menu()
        assert components._context_menu_panel is None

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_has_context_menu_returns_true_when_visible(self, mock_button_class, mock_panel_class):
        """Test has_context_menu returns True when menu is visible."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")

        assert components.has_context_menu() is True

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_has_context_menu_returns_false_when_not_visible(self, mock_button_class):
        """Test has_context_menu returns False when no menu."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        assert components.has_context_menu() is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_has_context_menu_returns_false_after_hide(self, mock_button_class, mock_panel_class):
        """Test has_context_menu returns False after hiding."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        components.hide_context_menu()

        assert components.has_context_menu() is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_pause_button_returns_true_for_pause_button(
        self, mock_button_class, mock_panel_class
    ):
        """Test is_pause_button correctly identifies pause button."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        pause_button = components._context_menu_buttons["pause"]

        assert components.is_pause_button(pause_button) is True

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_pause_button_returns_false_for_other_element(
        self, mock_button_class, mock_panel_class
    ):
        """Test is_pause_button returns False for other elements."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        other_element = Mock()

        assert components.is_pause_button(other_element) is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_pause_button_returns_false_when_no_menu(self, mock_button_class):
        """Test is_pause_button returns False when no menu exists."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        some_element = Mock()

        assert components.is_pause_button(some_element) is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_fps_limit_button_returns_true_for_fps_limit_button(
        self, mock_button_class, mock_panel_class
    ):
        """Test is_fps_limit_button correctly identifies FPS limit button."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        fps_limit_button = components._context_menu_buttons["fps_limit"]

        assert components.is_fps_limit_button(fps_limit_button) is True

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_fps_limit_button_returns_false_for_other_element(
        self, mock_button_class, mock_panel_class
    ):
        """Test is_fps_limit_button returns False for other elements."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        other_element = Mock()

        assert components.is_fps_limit_button(other_element) is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_fps_limit_button_returns_false_when_no_menu(self, mock_button_class):
        """Test is_fps_limit_button returns False when no menu exists."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        some_element = Mock()

        assert components.is_fps_limit_button(some_element) is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_fps_limit_enabled(
        self, mock_button_class, mock_panel_class
    ):
        """Test context menu shows FPS limit as enabled when fps_limit=60."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Reset mock to ignore help button created during init
        mock_button_class.reset_mock()

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy", fps_limit=60)

        # Check FPS limit button text (second button: pause, fps_limit, engine)
        calls = mock_button_class.call_args_list
        fps_button_call = calls[1]  # Second button is FPS limit
        assert "[*] Limit 60 FPS" in fps_button_call.kwargs["text"]

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_fps_limit_disabled(
        self, mock_button_class, mock_panel_class
    ):
        """Test context menu shows FPS limit as disabled when fps_limit=0."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Reset mock to ignore help button created during init
        mock_button_class.reset_mock()

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy", fps_limit=0)

        # Check FPS limit button text (second button: pause, fps_limit, engine)
        calls = mock_button_class.call_args_list
        fps_button_call = calls[1]  # Second button is FPS limit
        assert "    Limit 60 FPS" in fps_button_call.kwargs["text"]
        assert "[*]" not in fps_button_call.kwargs["text"]

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_get_engine_from_button_returns_engine_name(
        self, mock_button_class, mock_panel_class
    ):
        """Test get_engine_from_button returns engine name for engine button."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy", "loop"], current_engine="numpy")
        numpy_button = components._context_menu_buttons["engine_numpy"]

        assert components.get_engine_from_button(numpy_button) == "numpy"

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_get_engine_from_button_returns_none_for_pause_button(
        self, mock_button_class, mock_panel_class
    ):
        """Test get_engine_from_button returns None for pause button."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Need to ensure each button is a unique mock object
        button_instances = [Mock(), Mock(), Mock()]  # pause, fps_limit, engine
        mock_button_class.side_effect = button_instances

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")

        # First button created should be pause button
        pause_button = button_instances[0]

        assert components.get_engine_from_button(pause_button) is None

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_get_engine_from_button_returns_none_for_other_element(
        self, mock_button_class, mock_panel_class
    ):
        """Test get_engine_from_button returns None for other elements."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")
        other_element = Mock()

        assert components.get_engine_from_button(other_element) is None

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_context_menu_creates_engine_buttons(
        self, mock_button_class, mock_panel_class
    ):
        """Test that show_context_menu creates buttons for all engines."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        mock_button_class.reset_mock()

        components.show_context_menu(
            (100, 100), is_paused=False,
            available_engines=["numpy", "loop", "custom"],
            current_engine="loop"
        )

        # Should create 1 pause button + 1 fps limit button + 3 engine buttons = 5 total
        assert mock_button_class.call_count == 5

        # Check that engine buttons were created with correct text
        calls = mock_button_class.call_args_list
        engine_calls = calls[2:]  # Skip first two calls (pause button and fps_limit button)

        # numpy should not have indicator
        assert "numpy" in engine_calls[0].kwargs["text"]
        assert "[*]" not in engine_calls[0].kwargs["text"]

        # loop should have indicator (current engine)
        assert "loop" in engine_calls[1].kwargs["text"]
        assert "[*]" in engine_calls[1].kwargs["text"]

        # custom should not have indicator
        assert "custom" in engine_calls[2].kwargs["text"]
        assert "[*]" not in engine_calls[2].kwargs["text"]

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_click_inside_context_menu_returns_true_for_inside_click(
        self, mock_button_class, mock_panel_class
    ):
        """Test is_click_inside_context_menu returns True for clicks inside menu."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Create mock panel with a rect
        mock_panel = Mock()
        mock_rect = Mock()
        mock_rect.collidepoint.return_value = True
        mock_panel.get_abs_rect.return_value = mock_rect
        mock_panel_class.return_value = mock_panel

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")

        assert components.is_click_inside_context_menu((120, 120)) is True
        mock_rect.collidepoint.assert_called_once_with(120, 120)

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIPanel")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_click_inside_context_menu_returns_false_for_outside_click(
        self, mock_button_class, mock_panel_class
    ):
        """Test is_click_inside_context_menu returns False for clicks outside menu."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Create mock panel with a rect
        mock_panel = Mock()
        mock_rect = Mock()
        mock_rect.collidepoint.return_value = False
        mock_panel.get_abs_rect.return_value = mock_rect
        mock_panel_class.return_value = mock_panel

        components.show_context_menu((100, 100), is_paused=False, available_engines=["numpy"], current_engine="numpy")

        assert components.is_click_inside_context_menu((500, 500)) is False
        mock_rect.collidepoint.assert_called_once_with(500, 500)

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_click_inside_context_menu_returns_false_when_no_menu(self, mock_button_class):
        """Test is_click_inside_context_menu returns False when no menu exists."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        assert components.is_click_inside_context_menu((100, 100)) is False

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_help_button_returns_true_for_help_button(self, mock_button_class):
        """Test is_help_button correctly identifies help button."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        help_button = components._help_button

        assert components.is_help_button(help_button) is True

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_is_help_button_returns_false_for_other_element(self, mock_button_class):
        """Test is_help_button returns False for other elements."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        other_element = Mock()

        assert components.is_help_button(other_element) is False

    @patch("pycgol.ui._ui_components.pygame_gui.windows.UIMessageWindow")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_help_popup(self, mock_button_class, mock_window_class):
        """Test showing help popup."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_help_popup()

        # Should create message window
        mock_window_class.assert_called_once()
        call_args = mock_window_class.call_args

        assert call_args.kwargs["manager"] == mock_manager
        assert call_args.kwargs["window_title"] == "Help"
        assert "Conway's Game of Life" in call_args.kwargs["html_message"]
        assert "Controls" in call_args.kwargs["html_message"]

    @patch("pycgol.ui._ui_components.pygame_gui.windows.UIMessageWindow")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_help_popup_centered(self, mock_button_class, mock_window_class):
        """Test that help popup is centered on screen."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_help_popup()

        call_args = mock_window_class.call_args
        rect = call_args.kwargs["rect"]

        # Popup is 400x350, should be centered
        # X: (800 - 400) / 2 = 200
        # Y: (600 - 350) / 2 = 125
        assert rect.x == 200
        assert rect.y == 125
        assert rect.width == 400
        assert rect.height == 350

    @patch("pycgol.ui._ui_components.pygame_gui.windows.UIMessageWindow")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_show_help_popup_when_already_showing(
        self, mock_button_class, mock_window_class
    ):
        """Test that showing help popup twice doesn't create second popup."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_help_popup()
        mock_window_class.reset_mock()

        components.show_help_popup()

        # Should not create second popup
        mock_window_class.assert_not_called()

    @patch("pycgol.ui._ui_components.pygame_gui.windows.UIMessageWindow")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_hide_help_popup(self, mock_button_class, mock_window_class):
        """Test hiding help popup."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_help_popup()
        popup = components._help_popup

        components.hide_help_popup()

        # Should kill popup and set to None
        popup.kill.assert_called_once()
        assert components._help_popup is None

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_hide_help_popup_when_none(self, mock_button_class):
        """Test that hiding help popup when none exists doesn't error."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        # Should not raise exception
        components.hide_help_popup()
        assert components._help_popup is None

    @patch("pycgol.ui._ui_components.pygame_gui.windows.UIMessageWindow")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_has_help_popup_returns_true_when_visible(
        self, mock_button_class, mock_window_class
    ):
        """Test has_help_popup returns True when popup is visible."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_help_popup()

        assert components.has_help_popup() is True

    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_has_help_popup_returns_false_when_not_visible(self, mock_button_class):
        """Test has_help_popup returns False when no popup."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        assert components.has_help_popup() is False

    @patch("pycgol.ui._ui_components.pygame_gui.windows.UIMessageWindow")
    @patch("pycgol.ui._ui_components.pygame_gui.elements.UIButton")
    def test_has_help_popup_returns_false_after_hide(
        self, mock_button_class, mock_window_class
    ):
        """Test has_help_popup returns False after hiding."""
        mock_manager = Mock()
        components = UIComponents(mock_manager, 800, 600)

        components.show_help_popup()
        components.hide_help_popup()

        assert components.has_help_popup() is False
