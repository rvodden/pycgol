"""Registry for tracking available Game of Life engine implementations."""

from typing import Dict
from ._engine import Engine


class EngineRegistry:
    """
    Registry for managing available Game of Life engine implementations.

    Allows registration, retrieval, and listing of engine implementations
    to support runtime engine switching.
    """

    def __init__(self) -> None:
        """Initialize an empty engine registry."""
        self._engines: Dict[str, type[Engine]] = {}
        self._default_engine: str | None = None

    def register(self, name: str, engine_class: type[Engine], *, is_default: bool = False) -> None:
        """
        Register an engine implementation.

        Args:
            name: Unique identifier for the engine (e.g., "numpy", "loop")
            engine_class: The engine class (must inherit from Engine)
            is_default: If True, sets this engine as the default

        Raises:
            ValueError: If the name is already registered or if engine_class
                       doesn't inherit from Engine
        """
        if name in self._engines:
            raise ValueError(f"Engine '{name}' is already registered")

        if not issubclass(engine_class, Engine):
            raise ValueError(f"Engine class must inherit from Engine, got {engine_class}")

        self._engines[name] = engine_class

        # Set as default if this is the first engine or explicitly marked as default
        if is_default or self._default_engine is None:
            self._default_engine = name

    def get(self, name: str) -> type[Engine]:
        """
        Retrieve an engine by name.

        Args:
            name: The name of the engine to retrieve

        Returns:
            The engine class

        Raises:
            KeyError: If no engine with the given name is registered
        """
        if name not in self._engines:
            raise KeyError(f"No engine registered with name '{name}'")
        return self._engines[name]

    def get_default(self) -> type[Engine]:
        """
        Get the default engine.

        Returns:
            The default engine class

        Raises:
            RuntimeError: If no engines are registered
        """
        if self._default_engine is None:
            raise RuntimeError("No engines registered")
        return self._engines[self._default_engine]

    def set_default(self, name: str) -> None:
        """
        Set the default engine.

        Args:
            name: The name of the engine to set as default

        Raises:
            KeyError: If no engine with the given name is registered
        """
        if name not in self._engines:
            raise KeyError(f"No engine registered with name '{name}'")
        self._default_engine = name

    def list_engines(self) -> list[str]:
        """
        List all registered engine names.

        Returns:
            List of engine names in registration order
        """
        return list(self._engines.keys())

    def get_default_name(self) -> str | None:
        """
        Get the name of the default engine.

        Returns:
            The name of the default engine, or None if no engines are registered
        """
        return self._default_engine

    def is_registered(self, name: str) -> bool:
        """
        Check if an engine is registered.

        Args:
            name: The name to check

        Returns:
            True if an engine with this name is registered, False otherwise
        """
        return name in self._engines

    def unregister(self, name: str) -> None:
        """
        Unregister an engine.

        Args:
            name: The name of the engine to unregister

        Raises:
            KeyError: If no engine with the given name is registered
            RuntimeError: If trying to unregister the only remaining engine
        """
        if name not in self._engines:
            raise KeyError(f"No engine registered with name '{name}'")

        if len(self._engines) == 1:
            raise RuntimeError("Cannot unregister the only remaining engine")

        del self._engines[name]

        # If we unregistered the default, pick a new default
        if self._default_engine == name:
            self._default_engine = next(iter(self._engines.keys()))

    def clear(self) -> None:
        """Remove all registered engines."""
        self._engines.clear()
        self._default_engine = None
