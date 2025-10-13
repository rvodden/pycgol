from unittest.mock import Mock, patch


from pycgol.ui._renderer import Renderer
from pycgol.ui._viewport_manager import ViewportManager
from pycgol.state import DenseState as State


class TestRenderer:
    """Test the Renderer class."""

    @patch("pycgol.ui._renderer.pygame")
    def test_render_fills_screen_with_background(self, mock_pygame):
        """Test that render fills screen with dark blue background."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(10, 10)
        viewport = ViewportManager(cell_size=10)

        renderer.render(state, viewport)

        # Should fill screen with dark blue (20, 30, 60)
        mock_screen.fill.assert_called_once_with((20, 30, 60))

    @patch("pycgol.ui._renderer.pygame")
    def test_render_draws_cells(self, mock_pygame):
        """Test that render draws cells at correct positions."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(20, 20)
        state[5, 5] = True  # One alive cell
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(0, 0)

        renderer.render(state, viewport)

        # Should draw rectangles
        # 10x10 viewport (100/10 = 10 cells in each direction)
        # Should draw black background for each cell + white for alive cells
        # Total calls = background fills + alive cell fills
        assert mock_pygame.draw.rect.call_count > 0

    @patch("pycgol.ui._renderer.pygame")
    def test_render_draws_alive_cell_in_white(self, mock_pygame):
        """Test that alive cells are drawn in white."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(20, 20)
        state[5, 5] = True
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(0, 0)

        renderer.render(state, viewport)

        # Find calls with "white" color
        white_calls = [
            c
            for c in mock_pygame.draw.rect.call_args_list
            if len(c.args) >= 2 and c.args[1] == "white"
        ]

        assert len(white_calls) > 0

    @patch("pycgol.ui._renderer.pygame")
    def test_render_draws_black_background_for_cells(self, mock_pygame):
        """Test that in-bounds cells have black background."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(20, 20)
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(0, 0)

        renderer.render(state, viewport)

        # Find calls with "black" color
        black_calls = [
            c
            for c in mock_pygame.draw.rect.call_args_list
            if len(c.args) >= 2 and c.args[1] == "black"
        ]

        # Should draw black background for all visible cells
        # 10x10 cells visible
        assert len(black_calls) == 100

    @patch("pycgol.ui._renderer.pygame.display")
    @patch("pycgol.ui._renderer.pygame.font")
    @patch("pycgol.ui._renderer.pygame.draw")
    def test_render_with_viewport_offset(self, mock_draw, mock_font, mock_display):
        """Test that cells are drawn correctly with viewport offset."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(50, 50)
        state[15, 15] = True  # Alive cell at grid (15, 15)

        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(10, 10)  # Viewport shows grid cells (10-19, 10-19)

        renderer.render(state, viewport)

        # Cell (15, 15) in grid should be at viewport position (5, 5)
        # Which is screen pixel position (50, 50) with cell_size=10
        white_calls = [
            c
            for c in mock_draw.rect.call_args_list
            if len(c.args) >= 2 and c.args[1] == "white"
        ]

        # Check that white cell was drawn at correct position
        assert len(white_calls) == 1
        drawn_rect = white_calls[0].args[2]
        assert drawn_rect.x == 50  # (15 - 10) * 10
        assert drawn_rect.y == 50  # (15 - 10) * 10

    @patch("pycgol.ui._renderer.pygame")
    def test_render_skips_out_of_bounds_cells(self, mock_pygame):
        """Test that cells outside grid bounds are not drawn."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        # Small grid
        state = State(5, 5)
        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(0, 0)

        renderer.render(state, viewport)

        # Should only draw black backgrounds for cells within grid
        # Grid is 5x5, but viewport is 10x10
        # Should only draw 5x5 = 25 black backgrounds
        black_calls = [
            c
            for c in mock_pygame.draw.rect.call_args_list
            if len(c.args) >= 2 and c.args[1] == "black"
        ]

        assert len(black_calls) == 25

    @patch("pycgol.ui._renderer.pygame")
    def test_render_draws_fps_counter(self, mock_pygame):
        """Test that FPS counter is drawn."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 800
        mock_screen.get_height.return_value = 600
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        mock_font = Mock()
        mock_font_surface = Mock()
        mock_font_rect = Mock()
        mock_font_surface.get_rect.return_value = mock_font_rect
        mock_font.render.return_value = mock_font_surface
        mock_pygame.font.SysFont.return_value = mock_font

        state = State(10, 10)
        viewport = ViewportManager(cell_size=10)

        renderer.render(state, viewport, fps=60.5)

        # Should create monospace font
        mock_pygame.font.SysFont.assert_called_once_with("monospace", 24, bold=True)

        # Should render FPS text
        mock_font.render.assert_called_once()
        fps_text = mock_font.render.call_args.args[0]
        assert "FPS:" in fps_text
        assert "60.5" in fps_text

        # Should blit to screen
        mock_screen.blit.assert_called_once_with(mock_font_surface, mock_font_rect)

    @patch("pycgol.ui._renderer.pygame")
    def test_render_fps_counter_in_top_right(self, mock_pygame):
        """Test that FPS counter is positioned in top right corner."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 800
        mock_screen.get_height.return_value = 600
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        mock_font = Mock()
        mock_font_surface = Mock()
        mock_font_rect = Mock()
        mock_font_surface.get_rect.return_value = mock_font_rect
        mock_font.render.return_value = mock_font_surface
        mock_pygame.font.SysFont.return_value = mock_font

        state = State(10, 10)
        viewport = ViewportManager(cell_size=10)

        renderer.render(state, viewport, fps=60.0)

        # Should set topright to (screen_width - 10, 10)
        assert mock_font_rect.topright == (790, 10)  # 800 - 10 = 790

    @patch("pycgol.ui._renderer.pygame")
    def test_render_calls_manager_draw_ui(self, mock_pygame):
        """Test that render calls UIManager.draw_ui."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(10, 10)
        viewport = ViewportManager(cell_size=10)

        renderer.render(state, viewport)

        # Should draw UI elements
        mock_manager.draw_ui.assert_called_once_with(mock_screen)

    @patch("pycgol.ui._renderer.pygame")
    def test_render_calls_display_flip(self, mock_pygame):
        """Test that render calls pygame.display.flip to update screen."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(10, 10)
        viewport = ViewportManager(cell_size=10)

        renderer.render(state, viewport)

        # Should flip display
        mock_pygame.display.flip.assert_called_once()

    @patch("pycgol.ui._renderer.pygame.display")
    @patch("pycgol.ui._renderer.pygame.font")
    @patch("pycgol.ui._renderer.pygame.draw")
    def test_render_with_different_cell_sizes(self, mock_draw, mock_font, mock_display):
        """Test rendering with different cell sizes."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 200
        mock_screen.get_height.return_value = 200
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(50, 50)
        state[5, 5] = True

        # Test with cell_size=20
        viewport = ViewportManager(cell_size=20)
        viewport.set_viewport(0, 0)

        renderer.render(state, viewport)

        # Find white cell draw call
        white_calls = [
            c
            for c in mock_draw.rect.call_args_list
            if len(c.args) >= 2 and c.args[1] == "white"
        ]

        assert len(white_calls) == 1
        drawn_rect = white_calls[0].args[2]
        assert drawn_rect.width == 20
        assert drawn_rect.height == 20

    @patch("pycgol.ui._renderer.pygame")
    def test_render_default_fps_is_zero(self, mock_pygame):
        """Test that default FPS parameter is 0.0."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        mock_font = Mock()
        mock_font_surface = Mock()
        mock_font_rect = Mock()
        mock_font_surface.get_rect.return_value = mock_font_rect
        mock_font.render.return_value = mock_font_surface
        mock_pygame.font.SysFont.return_value = mock_font

        state = State(10, 10)
        viewport = ViewportManager(cell_size=10)

        # Don't pass fps parameter
        renderer.render(state, viewport)

        # Should render with 0.0
        fps_text = mock_font.render.call_args.args[0]
        assert "  0.0" in fps_text

    @patch("pycgol.ui._renderer.pygame")
    def test_render_multiple_alive_cells(self, mock_pygame):
        """Test rendering multiple alive cells."""
        mock_screen = Mock()
        mock_screen.get_width.return_value = 100
        mock_screen.get_height.return_value = 100
        mock_manager = Mock()
        renderer = Renderer(mock_screen, mock_manager)

        state = State(20, 20)
        state[2, 2] = True
        state[3, 3] = True
        state[4, 4] = True

        viewport = ViewportManager(cell_size=10)
        viewport.set_viewport(0, 0)

        renderer.render(state, viewport)

        # Should draw 3 white cells
        white_calls = [
            c
            for c in mock_pygame.draw.rect.call_args_list
            if len(c.args) >= 2 and c.args[1] == "white"
        ]

        assert len(white_calls) == 3
