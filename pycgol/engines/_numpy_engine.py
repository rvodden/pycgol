import numpy as np
from scipy import signal

from ._engine import Engine
from ..state import StateInterface, DenseState


class NumpyEngine(Engine):
    """Numpy-optimized implementation.

    This engine requires dense state for efficient numpy array operations.
    It will convert sparse states to dense on first use.
    """

    # Prefer dense state for numpy array operations
    preferred_state_type = DenseState

    # Convolution kernel to count neighbors
    _KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)

    @classmethod
    def next_state(cls, state: StateInterface) -> StateInterface:
        # Optimize to dense state if needed
        state = cls.optimize_state(state)

        # Now we can safely assume it's a DenseState with _cells attribute
        # Convert state to numpy array for fast computation
        grid = np.array(
            [[state[x, y] for x in range(state.width)] for y in range(state.height)],
            dtype=np.int8,
        )

        # Count neighbors using convolution (much faster than loops)
        neighbor_count = signal.convolve2d(
            grid, cls._KERNEL, mode="same", boundary="fill"
        )

        # Apply Game of Life rules vectorized
        # Live cells with 2 or 3 neighbors survive
        # Dead cells with exactly 3 neighbors become alive
        next_grid = ((grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))) | (
            (grid == 0) & (neighbor_count == 3)
        )

        # Create new dense state and copy results
        next_state = DenseState(state.width, state.height)
        for y in range(state.height):
            for x in range(state.width):
                next_state[x, y] = bool(next_grid[y, x])

        return next_state
