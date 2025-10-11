import pytest
from unittest.mock import Mock, patch, MagicMock

from pycgol._ui import UI
from pycgol._state import State


class TestUI:

    @patch('pycgol._ui.pygame')
    def test_ui_initialization(self, mock_pygame):
        mock_display = Mock()
        mock_pygame.display.set_mode.return_value = mock_display

        ui = UI(800, 600)

        mock_pygame.display.set_mode.assert_called_once_with((800, 600))
        assert ui._screen == mock_display

    @patch('pycgol._ui.pygame')
    def test_render_calls_pygame_methods(self, mock_pygame):
        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen
        mock_screen.get_width.return_value = 400
        mock_screen.get_height.return_value = 300

        ui = UI(400, 300)
        state = State(4, 3)
        state[1, 1] = True

        ui.render(state)

        # Verify screen.fill was called
        mock_screen.fill.assert_called_once_with("black")

        # Verify pygame.draw.rect was called for each cell
        assert mock_pygame.draw.rect.call_count == 12  # 4x3 grid

        # Verify pygame.display.flip was called
        mock_pygame.display.flip.assert_called_once()

    @patch('pycgol._ui.pygame')
    def test_render_cell_colors(self, mock_pygame):
        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen
        mock_screen.get_width.return_value = 200
        mock_screen.get_height.return_value = 200

        # Mock pygame.Rect to return a mock with controllable attributes
        def mock_rect_factory(x, y, width, height):
            rect = Mock()
            rect.x = x
            rect.y = y
            rect.width = width
            rect.height = height
            return rect

        mock_pygame.Rect.side_effect = mock_rect_factory

        ui = UI(200, 200)
        state = State(2, 2)
        state[0, 0] = True  # Alive cell

        ui.render(state)

        # Check that draw.rect was called with correct colors
        calls = mock_pygame.draw.rect.call_args_list

        # Should have 4 calls (2x2 grid)
        assert len(calls) == 4

        # Find the call for the alive cell (0,0) - should be white
        alive_cell_call = None
        for call in calls:
            args, kwargs = call
            screen, color, rect = args
            if rect.x == 0 and rect.y == 0:  # This is cell (0,0)
                alive_cell_call = call
                break

        assert alive_cell_call is not None
        args, kwargs = alive_cell_call
        screen, color, rect = args
        assert color == "white"

    @patch('pycgol._ui.pygame')
    def test_render_rectangle_dimensions(self, mock_pygame):
        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen
        mock_screen.get_width.return_value = 300
        mock_screen.get_height.return_value = 200

        # Mock pygame.Rect to return a mock with controllable attributes
        def mock_rect_factory(x, y, width, height):
            rect = Mock()
            rect.x = x
            rect.y = y
            rect.width = width
            rect.height = height
            return rect

        mock_pygame.Rect.side_effect = mock_rect_factory

        ui = UI(300, 200)
        state = State(3, 2)  # 3x2 grid

        ui.render(state)

        # Verify rectangle dimensions are calculated correctly
        calls = mock_pygame.draw.rect.call_args_list

        # Each cell should be 100x100 pixels (300/3 = 100, 200/2 = 100)
        for call in calls:
            args, kwargs = call
            screen, color, rect = args
            assert rect.width == 100.0
            assert rect.height == 100.0

    @patch('pycgol._ui.pygame')
    def test_render_empty_state(self, mock_pygame):
        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100

        ui = UI(100, 100)
        state = State(2, 2)  # All cells are False by default

        ui.render(state)

        # All cells should be rendered as black
        calls = mock_pygame.draw.rect.call_args_list
        assert len(calls) == 4

        for call in calls:
            args, kwargs = call
            screen, color, rect = args
            assert color == "black"