import pytest
from unittest.mock import Mock, patch

from pycgol._application import Application
from pycgol.engines import EngineRegistry, LoopEngine, NumpyEngine


def create_mock_world_initializer():
    """Helper to create a mock WorldInitializer."""
    mock_state = Mock()
    mock_state.width = 328
    mock_state.height = 272

    mock_initializer = Mock()
    mock_initializer.create_initial_state.return_value = mock_state
    mock_initializer.get_initial_viewport_position.return_value = (100, 100)

    return mock_initializer, mock_state


class TestApplication:
    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    @patch("pycgol._application.WorldInitializer")
    def test_application_initialization(
        self,
        mock_world_initializer_class,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        mock_initializer, mock_state = create_mock_world_initializer()
        mock_world_initializer_class.return_value = mock_initializer

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock
        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        _ = Application()

        # Verify pygame.init was called
        mock_pygame.init.assert_called_once()

        # Verify UI was created with correct dimensions and cell size
        mock_ui_class.assert_called_once_with(
            1280, 720, mock_pygame_gui.UIManager.return_value, 10
        )

        # Verify WorldInitializer was created with correct parameters
        mock_world_initializer_class.assert_called_once_with(1280, 720, 10, 100)

        # Verify clock was created
        mock_pygame.time.Clock.assert_called_once()

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    @patch("pycgol._application.EventHandler")
    @patch("pycgol._application.GameLoop")
    def test_run_game_loop_quit_event(
        self,
        mock_game_loop_class,
        mock_event_handler_class,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        # Setup mocks
        mock_initializer, mock_state = create_mock_world_initializer()

        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        mock_game_loop_instance = Mock()
        mock_game_loop_instance.update.return_value = mock_state
        mock_game_loop_class.return_value = mock_game_loop_instance

        mock_event_handler_instance = Mock()
        mock_event_handler_instance.handle_event.return_value = True  # Signal quit
        mock_event_handler_class.return_value = mock_event_handler_instance

        mock_clock = Mock()
        mock_clock.tick.return_value = 16  # ~60 FPS
        mock_clock.get_fps.return_value = 60.0
        mock_pygame.time.Clock.return_value = mock_clock

        mock_manager = Mock()
        mock_pygame_gui.UIManager.return_value = mock_manager

        # Create quit event
        quit_event = Mock()
        quit_event.type = mock_pygame.QUIT
        mock_pygame.event.get.return_value = [quit_event]

        # Mock engine
        mock_engine = Mock()
        mock_engine.next_state.return_value = mock_state

        # Inject the world initializer
        app = Application(engine=mock_engine, world_initializer=mock_initializer)
        app.run()

        # Verify pygame.quit was called when exiting
        mock_pygame.quit.assert_called_once()

        # Verify UI render was called with fps
        assert mock_ui_instance.render.called
        render_call_args = mock_ui_instance.render.call_args
        assert render_call_args[0][0] == mock_state  # state argument
        assert render_call_args[0][1] == 60.0  # fps argument

        # Verify clock tick was called
        mock_clock.tick.assert_called_with(60)

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    @patch("pycgol._application.EventHandler")
    @patch("pycgol._application.GameLoop")
    def test_pause_functionality(
        self,
        mock_game_loop_class,
        mock_event_handler_class,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        # Setup mocks
        mock_initializer, mock_state = create_mock_world_initializer()

        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        mock_game_loop_instance = Mock()
        mock_game_loop_instance.update.return_value = mock_state
        mock_game_loop_class.return_value = mock_game_loop_instance

        mock_event_handler_instance = Mock()
        # First call doesn't quit, second call quits
        mock_event_handler_instance.handle_event.side_effect = [False, True]
        mock_event_handler_class.return_value = mock_event_handler_instance

        mock_clock = Mock()
        mock_clock.tick.return_value = 1000  # 1 second to trigger state update
        mock_clock.get_fps.return_value = 60.0
        mock_pygame.time.Clock.return_value = mock_clock

        mock_manager = Mock()
        mock_pygame_gui.UIManager.return_value = mock_manager

        # Mock engine
        mock_engine = Mock()
        mock_engine.next_state.return_value = mock_state

        button_event = Mock()
        quit_event = Mock()
        mock_pygame.event.get.side_effect = [[button_event], [quit_event]]

        app = Application(engine=mock_engine, world_initializer=mock_initializer)
        app.run()

        # Verify game loop update was called
        assert mock_game_loop_instance.update.called

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    @patch("pycgol._application.EventHandler")
    @patch("pycgol._application.GameLoop")
    def test_different_update_rate(
        self,
        mock_game_loop_class,
        mock_event_handler_class,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that the update rate parameter works correctly."""
        mock_initializer, mock_state = create_mock_world_initializer()

        mock_ui_instance = Mock()
        mock_ui_class.return_value = mock_ui_instance

        mock_game_loop_instance = Mock()
        mock_game_loop_instance.update.return_value = mock_state
        mock_game_loop_class.return_value = mock_game_loop_instance

        mock_event_handler_instance = Mock()
        # Return True on 5th call to quit
        mock_event_handler_instance.handle_event.side_effect = [False, False, False, False, True]
        mock_event_handler_class.return_value = mock_event_handler_instance

        mock_clock = Mock()
        mock_clock.tick.return_value = 50  # 0.05 seconds per frame
        mock_clock.get_fps.return_value = 60.0
        mock_pygame.time.Clock.return_value = mock_clock

        mock_manager = Mock()
        mock_pygame_gui.UIManager.return_value = mock_manager

        mock_pygame.event.get.return_value = [Mock()]

        mock_engine = Mock()
        mock_engine.next_state.return_value = mock_state

        # Set update rate to 20 updates per second
        app = Application(
            gol_updates_per_second=20,
            engine=mock_engine,
            world_initializer=mock_initializer
        )
        app.run()

        # Verify GameLoop was created with correct rate
        mock_game_loop_class.assert_called_once_with(20)

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    def test_engine_registry_is_created_by_default(
        self,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that Application creates a default EngineRegistry."""
        mock_initializer, _ = create_mock_world_initializer()

        app = Application(world_initializer=mock_initializer)

        registry = app.get_engine_registry()
        assert isinstance(registry, EngineRegistry)
        assert registry.is_registered("numpy")
        assert registry.is_registered("loop")
        assert registry.get_default_name() == "numpy"

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    def test_can_provide_custom_engine_registry(
        self,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that a custom EngineRegistry can be provided."""
        mock_initializer, _ = create_mock_world_initializer()

        custom_registry = EngineRegistry()
        custom_registry.register("loop", LoopEngine, is_default=True)

        app = Application(engine_registry=custom_registry, world_initializer=mock_initializer)

        registry = app.get_engine_registry()
        assert registry is custom_registry
        assert registry.get_default_name() == "loop"

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    def test_get_current_engine(
        self,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that get_current_engine returns the active engine."""
        mock_initializer, _ = create_mock_world_initializer()

        app = Application(engine=LoopEngine, world_initializer=mock_initializer)

        assert app.get_current_engine() == LoopEngine

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    def test_set_engine(
        self,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that set_engine changes the active engine."""
        mock_initializer, _ = create_mock_world_initializer()

        app = Application(engine=NumpyEngine, world_initializer=mock_initializer)
        assert app.get_current_engine() == NumpyEngine

        app.set_engine(LoopEngine)
        assert app.get_current_engine() == LoopEngine

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    def test_set_engine_by_name(
        self,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that set_engine_by_name changes the active engine using registry."""
        mock_initializer, _ = create_mock_world_initializer()

        app = Application(engine=NumpyEngine, world_initializer=mock_initializer)
        assert app.get_current_engine() == NumpyEngine

        app.set_engine_by_name("loop")
        assert app.get_current_engine() == LoopEngine

    @patch("pycgol._application.pygame")
    @patch("pycgol._application.pygame_gui")
    @patch("pycgol._application.UI")
    def test_set_engine_by_name_raises_for_unknown_engine(
        self,
        mock_ui_class,
        mock_pygame_gui,
        mock_pygame,
    ):
        """Test that set_engine_by_name raises KeyError for unknown engine."""
        mock_initializer, _ = create_mock_world_initializer()

        app = Application(world_initializer=mock_initializer)

        with pytest.raises(KeyError):
            app.set_engine_by_name("nonexistent")
