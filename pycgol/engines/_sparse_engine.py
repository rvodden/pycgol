"""Sparse engine implementation for Game of Life."""

from ._engine import Engine
from ..state import State, SparseState


class SparseEngine(Engine):
    """Sparse implementation - only processes cells near live cells.

    This engine is optimized for sparse patterns where most cells are dead.
    It only examines cells that are alive or adjacent to alive cells,
    making it very efficient for sparse patterns.

    Complexity: O(live cells × 9) instead of O(grid size)
    Best for: Sparse patterns (<10% alive cells)
    """

    # Prefer sparse state for efficient sparse algorithm
    preferred_state_type = SparseState

    @classmethod
    def next_state(cls, state: State) -> State:
        """Calculate next generation using sparse algorithm."""
        # Optimize to sparse state if needed
        state = cls.optimize_state(state)

        # Get all live cells
        live_cells = state.get_live_cells()

        # Build set of cells to check (live cells + their neighbors)
        # This is the key optimization: we only check cells that might change
        cells_to_check = set()
        for x, y in live_cells:
            # Add the cell itself
            cells_to_check.add((x, y))
            # Add all 8 neighbors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    # Only add if within bounds
                    if 0 <= nx < state.width and 0 <= ny < state.height:
                        cells_to_check.add((nx, ny))

        # Create new sparse state
        next_state = SparseState(state.width, state.height)

        # Check each candidate cell
        for x, y in cells_to_check:
            # Count live neighbors
            neighbors = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    # Check if neighbor exists and is alive
                    if (nx, ny) in live_cells:
                        neighbors += 1

            # Apply Conway's Game of Life rules
            is_alive = (x, y) in live_cells

            if is_alive:
                # Live cell survives with 2 or 3 neighbors
                if neighbors == 2 or neighbors == 3:
                    next_state[x, y] = True
            else:
                # Dead cell becomes alive with exactly 3 neighbors
                if neighbors == 3:
                    next_state[x, y] = True

        return next_state
