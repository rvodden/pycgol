import pytest
from unittest.mock import Mock, patch, MagicMock

from pycgol._application import Application


class TestApplication:

    @patch('pycgol._application.pygame')
    @patch('pycgol._application.UI')
    @patch('pycgol._application.State')
    @patch('pycgol._application.Glider')
    def test_application_initialization(self, mock_glider, mock_state_class, mock_ui_class, mock_pygame):
        mock_state_instance = Mock()
        mock_state_class.return_value = mock_state_instance
        mock_glider.place.return_value = mock_state_instance
        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        app = Application()

        # Verify pygame.init was called
        mock_pygame.init.assert_called_once()

        # Verify UI was created with correct dimensions
        mock_ui_class.assert_called_once_with(1280, 720)

        # Verify State was created with correct dimensions (screen size / 10)
        mock_state_class.assert_called_once_with(128, 72)

        # Verify Glider was placed at the correct position
        mock_glider.place.assert_called_once_with((5, 67), mock_state_instance)

        # Verify clock was created
        mock_pygame.time.Clock.assert_called_once()

    @patch('pycgol._application.pygame')
    @patch('pycgol._application.UI')
    @patch('pycgol._application.State')
    @patch('pycgol._application.Glider')
    @patch('pycgol._application.Model')
    def test_run_game_loop_quit_event(self, mock_model, mock_glider, mock_state_class, mock_ui_class, mock_pygame):
        # Setup mocks
        mock_state_instance = Mock()
        mock_state_class.return_value = mock_state_instance
        mock_glider.place.return_value = mock_state_instance

        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        # Create quit event
        quit_event = Mock()
        quit_event.type = mock_pygame.QUIT
        mock_pygame.event.get.return_value = [quit_event]

        mock_model.next_state.return_value = mock_state_instance

        app = Application()
        app.run()

        # Verify pygame.quit was called when exiting
        mock_pygame.quit.assert_called_once()

        # Verify UI render was called
        mock_ui_instance.render.assert_called_with(mock_state_instance)

        # Verify clock tick was called
        mock_clock.tick.assert_called_with(60)

        # Verify Model.next_state was called
        mock_model.next_state.assert_called_with(mock_state_instance)

    @patch('pycgol._application.pygame')
    @patch('pycgol._application.UI')
    @patch('pycgol._application.State')
    @patch('pycgol._application.Glider')
    @patch('pycgol._application.Model')
    def test_run_game_loop_no_events(self, mock_model, mock_glider, mock_state_class, mock_ui_class, mock_pygame):
        # Setup mocks
        mock_state_instance = Mock()
        mock_state_class.return_value = mock_state_instance
        mock_glider.place.return_value = mock_state_instance

        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        mock_model.next_state.return_value = mock_state_instance

        # Simulate empty events for a few iterations, then quit
        call_count = 0
        def mock_event_get():
            nonlocal call_count
            call_count += 1
            if call_count >= 3:  # After 3 iterations, send quit event
                quit_event = Mock()
                quit_event.type = mock_pygame.QUIT
                return [quit_event]
            return []  # No events

        mock_pygame.event.get.side_effect = mock_event_get

        app = Application()
        app.run()

        # Verify Model.next_state was called multiple times
        assert mock_model.next_state.call_count >= 3

        # Verify UI render was called multiple times
        assert mock_ui_instance.render.call_count >= 3

        # Verify clock tick was called multiple times
        assert mock_clock.tick.call_count >= 3

    @patch('pycgol._application.pygame')
    @patch('pycgol._application.UI')
    @patch('pycgol._application.State')
    @patch('pycgol._application.Glider')
    @patch('pycgol._application.Model')
    def test_run_game_loop_multiple_events(self, mock_model, mock_glider, mock_state_class, mock_ui_class, mock_pygame):
        # Setup mocks
        mock_state_instance = Mock()
        mock_state_class.return_value = mock_state_instance
        mock_glider.place.return_value = mock_state_instance

        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        mock_model.next_state.return_value = mock_state_instance

        # Create various events, including quit
        other_event = Mock()
        other_event.type = "SOME_OTHER_EVENT"
        quit_event = Mock()
        quit_event.type = mock_pygame.QUIT

        mock_pygame.event.get.return_value = [other_event, quit_event]

        app = Application()
        app.run()

        # Should still quit properly even with other events
        mock_pygame.quit.assert_called_once()

    @patch('pycgol._application.pygame')
    @patch('pycgol._application.UI')
    @patch('pycgol._application.State')
    @patch('pycgol._application.Glider')
    def test_constants_used_correctly(self, mock_glider, mock_state_class, mock_ui_class, mock_pygame):
        mock_state_instance = Mock()
        mock_state_class.return_value = mock_state_instance
        mock_glider.place.return_value = mock_state_instance

        Application()

        # Verify the constants are used correctly
        # Screen dimensions: 1280x720
        # State dimensions: 128x72 (screen/10)
        # Glider position: (5, 67) where 67 = 72 - 5
        mock_ui_class.assert_called_once_with(1280, 720)
        mock_state_class.assert_called_once_with(128, 72)
        mock_glider.place.assert_called_once_with((5, 67), mock_state_instance)