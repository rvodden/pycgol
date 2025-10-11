from .._state import State

class Glider:

    _CELLS = [
        (0,0),
        (1,0),
        (2,0),
        (2,1),
        (1,2)
    ]

    @classmethod
    def place(cls, position: tuple[int, int], state: State) -> State:
        x, y = position
        for u, v in cls._CELLS:
            if 0 <= x+u < state.width and 0 <= y+v < state.height:
                state[x+u, y+v] = True
        return state