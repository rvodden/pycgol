"""Tests for the EngineRegistry class."""

import pytest

from pycgol.engines import Engine, LoopEngine, NumpyEngine, EngineRegistry
from pycgol.state import State as State, DenseState


class DummyEngine(Engine):
    """Dummy engine for testing purposes."""

    @classmethod
    def next_state(cls, state: State) -> State:
        return state


class AnotherDummyEngine(Engine):
    """Another dummy engine for testing purposes."""

    @classmethod
    def next_state(cls, state: State) -> State:
        return state


class TestEngineRegistry:
    """Test the EngineRegistry class."""

    def test_init_creates_empty_registry(self):
        """Test that a new registry is empty."""
        registry = EngineRegistry()

        assert registry.list_engines() == []
        assert registry.get_default_name() is None

    def test_register_single_engine(self):
        """Test registering a single engine."""
        registry = EngineRegistry()

        registry.register("dummy", DummyEngine)

        assert registry.list_engines() == ["dummy"]
        assert registry.is_registered("dummy")

    def test_register_sets_first_engine_as_default(self):
        """Test that the first registered engine becomes the default."""
        registry = EngineRegistry()

        registry.register("dummy", DummyEngine)

        assert registry.get_default_name() == "dummy"
        assert registry.get_default() == DummyEngine

    def test_register_multiple_engines(self):
        """Test registering multiple engines."""
        registry = EngineRegistry()

        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)

        assert len(registry.list_engines()) == 2
        assert "loop" in registry.list_engines()
        assert "numpy" in registry.list_engines()

    def test_register_with_explicit_default(self):
        """Test registering an engine as default explicitly."""
        registry = EngineRegistry()

        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine, is_default=True)

        # numpy should be default even though loop was registered first
        assert registry.get_default_name() == "numpy"
        assert registry.get_default() == NumpyEngine

    def test_register_duplicate_name_raises_error(self):
        """Test that registering duplicate names raises ValueError."""
        registry = EngineRegistry()
        registry.register("dummy", DummyEngine)

        with pytest.raises(ValueError, match="already registered"):
            registry.register("dummy", AnotherDummyEngine)

    def test_register_non_engine_class_raises_error(self):
        """Test that registering non-Engine class raises ValueError."""
        registry = EngineRegistry()

        class NotAnEngine:
            pass

        with pytest.raises(ValueError, match="must inherit from Engine"):
            registry.register("invalid", NotAnEngine)

    def test_get_retrieves_registered_engine(self):
        """Test that get returns the correct engine class."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)

        assert registry.get("loop") == LoopEngine
        assert registry.get("numpy") == NumpyEngine

    def test_get_nonexistent_engine_raises_error(self):
        """Test that get raises KeyError for unregistered engine."""
        registry = EngineRegistry()

        with pytest.raises(KeyError, match="No engine registered with name 'nonexistent'"):
            registry.get("nonexistent")

    def test_get_default_with_no_engines_raises_error(self):
        """Test that get_default raises RuntimeError when no engines registered."""
        registry = EngineRegistry()

        with pytest.raises(RuntimeError, match="No engines registered"):
            registry.get_default()

    def test_set_default_changes_default_engine(self):
        """Test that set_default changes the default engine."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)

        # loop is default (registered first)
        assert registry.get_default_name() == "loop"

        # Change default to numpy
        registry.set_default("numpy")

        assert registry.get_default_name() == "numpy"
        assert registry.get_default() == NumpyEngine

    def test_set_default_nonexistent_engine_raises_error(self):
        """Test that set_default raises KeyError for unregistered engine."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)

        with pytest.raises(KeyError, match="No engine registered with name 'nonexistent'"):
            registry.set_default("nonexistent")

    def test_list_engines_returns_all_names(self):
        """Test that list_engines returns all registered engine names."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)
        registry.register("dummy", DummyEngine)

        engines = registry.list_engines()

        assert len(engines) == 3
        assert "loop" in engines
        assert "numpy" in engines
        assert "dummy" in engines

    def test_list_engines_preserves_registration_order(self):
        """Test that list_engines returns names in registration order."""
        registry = EngineRegistry()
        registry.register("first", DummyEngine)
        registry.register("second", AnotherDummyEngine)
        registry.register("third", LoopEngine)

        assert registry.list_engines() == ["first", "second", "third"]

    def test_is_registered_returns_true_for_registered_engine(self):
        """Test that is_registered returns True for registered engines."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)

        assert registry.is_registered("loop") is True

    def test_is_registered_returns_false_for_unregistered_engine(self):
        """Test that is_registered returns False for unregistered engines."""
        registry = EngineRegistry()

        assert registry.is_registered("nonexistent") is False

    def test_unregister_removes_engine(self):
        """Test that unregister removes an engine from the registry."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)

        registry.unregister("loop")

        assert registry.is_registered("loop") is False
        assert registry.list_engines() == ["numpy"]

    def test_unregister_nonexistent_engine_raises_error(self):
        """Test that unregister raises KeyError for unregistered engine."""
        registry = EngineRegistry()

        with pytest.raises(KeyError, match="No engine registered with name 'nonexistent'"):
            registry.unregister("nonexistent")

    def test_unregister_only_engine_raises_error(self):
        """Test that unregistering the only engine raises RuntimeError."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)

        with pytest.raises(RuntimeError, match="Cannot unregister the only remaining engine"):
            registry.unregister("loop")

    def test_unregister_default_picks_new_default(self):
        """Test that unregistering the default engine picks a new default."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)

        # loop is default
        assert registry.get_default_name() == "loop"

        # Unregister default
        registry.unregister("loop")

        # numpy should now be default
        assert registry.get_default_name() == "numpy"
        assert registry.get_default() == NumpyEngine

    def test_clear_removes_all_engines(self):
        """Test that clear removes all engines."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)
        registry.register("dummy", DummyEngine)

        registry.clear()

        assert registry.list_engines() == []
        assert registry.get_default_name() is None

    def test_clear_empty_registry(self):
        """Test that clear works on an empty registry."""
        registry = EngineRegistry()

        # Should not raise
        registry.clear()

        assert registry.list_engines() == []

    def test_integration_with_real_engines(self):
        """Test registry with actual LoopEngine and NumpyEngine."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)

        # Both should be retrievable
        assert registry.get("loop") == LoopEngine
        assert registry.get("numpy") == NumpyEngine

        # Both should work with State
        state = DenseState(10, 10)
        state[5, 5] = True

        loop_next = registry.get("loop").next_state(state)
        numpy_next = registry.get("numpy").next_state(state)

        # Both engines should produce valid states
        assert isinstance(loop_next, State)
        assert isinstance(numpy_next, State)

    def test_default_can_be_changed_multiple_times(self):
        """Test that default can be changed multiple times."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.register("numpy", NumpyEngine)
        registry.register("dummy", DummyEngine)

        assert registry.get_default_name() == "loop"

        registry.set_default("numpy")
        assert registry.get_default_name() == "numpy"

        registry.set_default("dummy")
        assert registry.get_default_name() == "dummy"

        registry.set_default("loop")
        assert registry.get_default_name() == "loop"

    def test_register_after_clear(self):
        """Test that engines can be registered after clearing."""
        registry = EngineRegistry()
        registry.register("loop", LoopEngine)
        registry.clear()

        registry.register("numpy", NumpyEngine)

        assert registry.list_engines() == ["numpy"]
        assert registry.get_default_name() == "numpy"
