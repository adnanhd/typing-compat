"""
Test suite for Python 3.5+ features (py3m5.py module).

Tests core typing module features introduced in Python 3.5 (PEP 484).
"""

import sys
import pytest
from typing_compat.py3m5 import *


class TestPy3m5VersionFlag:
    """Test version detection for Python 3.5+ features."""

    def test_version_flag_accuracy(self):
        """Test that PY35_PLUS correctly detects Python 3.5+."""
        expected = sys.version_info >= (3, 5)
        assert PY35_PLUS == expected

    def test_version_flag_type(self):
        """Test that PY35_PLUS is a boolean."""
        assert isinstance(PY35_PLUS, bool)


class TestCoreTypes:
    """Test core typing types introduced in Python 3.5."""

    def test_any_import(self):
        """Test that Any can be imported."""
        assert Any is not None

    def test_union_import(self):
        """Test that Union can be imported."""
        assert Union is not None

    def test_union_usage(self):
        """Test Union type usage."""
        def process_value(value: Union[int, str]) -> str:
            return str(value)

        assert process_value(42) == "42"
        assert process_value("hello") == "hello"

    def test_optional_import(self):
        """Test that Optional can be imported."""
        assert Optional is not None

    def test_optional_usage(self):
        """Test Optional type usage."""
        def maybe_process(value: Optional[str]) -> int:
            return len(value) if value is not None else 0

        assert maybe_process("hello") == 5
        assert maybe_process(None) == 0

    def test_tuple_import(self):
        """Test that Tuple can be imported."""
        assert Tuple is not None

    def test_callable_import(self):
        """Test that Callable can be imported."""
        assert Callable is not None

    def test_callable_usage(self):
        """Test Callable type usage."""
        def apply_function(func: Callable[[int], str], value: int) -> str:
            return func(value)

        result = apply_function(str, 42)
        assert result == "42"

    def test_typevar_import(self):
        """Test that TypeVar can be imported."""
        assert TypeVar is not None

    def test_typevar_usage(self):
        """Test TypeVar usage."""
        T = TypeVar('T')

        def identity(value: T) -> T:
            return value

        assert identity(42) == 42
        assert identity("hello") == "hello"

    def test_generic_import(self):
        """Test that Generic can be imported."""
        assert Generic is not None

    def test_generic_usage(self):
        """Test Generic class usage."""
        T = TypeVar('T')

        class Container(Generic[T]):
            def __init__(self, value: T) -> None:
                self.value = value

            def get(self) -> T:
                return self.value

        container = Container("test")
        assert container.get() == "test"


class TestContainerTypes:
    """Test container types from Python 3.5 typing."""

    def test_list_import(self):
        """Test that List can be imported."""
        assert List is not None

    def test_list_usage(self):
        """Test List type usage."""
        def process_strings(items: List[str]) -> int:
            return len(items)

        result = process_strings(["a", "b", "c"])
        assert result == 3

    def test_dict_import(self):
        """Test that Dict can be imported."""
        assert Dict is not None

    def test_dict_usage(self):
        """Test Dict type usage."""
        def get_keys(mapping: Dict[str, int]) -> List[str]:
            return list(mapping.keys())

        result = get_keys({"a": 1, "b": 2})
        assert result == ["a", "b"]

    def test_set_import(self):
        """Test that Set can be imported."""
        assert Set is not None

    def test_set_usage(self):
        """Test Set type usage."""
        def unique_items(items: Set[str]) -> int:
            return len(items)

        result = unique_items({"a", "b", "c"})
        assert result == 3

    def test_frozenset_import(self):
        """Test that FrozenSet can be imported."""
        assert FrozenSet is not None

    def test_frozenset_usage(self):
        """Test FrozenSet type usage."""
        def process_frozen(items: FrozenSet[int]) -> List[int]:
            return sorted(list(items))

        result = process_frozen(frozenset([3, 1, 2]))
        assert result == [1, 2, 3]


class TestAbstractTypes:
    """Test abstract base class types."""

    def test_iterable_import(self):
        """Test that Iterable can be imported."""
        assert Iterable is not None

    def test_iterable_usage(self):
        """Test Iterable type usage."""
        def sum_items(items: Iterable[int]) -> int:
            return sum(items)

        assert sum_items([1, 2, 3]) == 6
        assert sum_items((1, 2, 3)) == 6

    def test_iterator_import(self):
        """Test that Iterator can be imported."""
        assert Iterator is not None

    def test_iterator_usage(self):
        """Test Iterator type usage."""
        def consume_iterator(it: Iterator[str]) -> List[str]:
            return list(it)

        result = consume_iterator(iter(["a", "b", "c"]))
        assert result == ["a", "b", "c"]

    def test_mapping_import(self):
        """Test that Mapping can be imported."""
        assert Mapping is not None

    def test_mapping_usage(self):
        """Test Mapping type usage."""
        def get_value(mapping: Mapping[str, int], key: str) -> Optional[int]:
            return mapping.get(key)

        result = get_value({"a": 1, "b": 2}, "a")
        assert result == 1

    def test_mutable_mapping_import(self):
        """Test that MutableMapping can be imported."""
        assert MutableMapping is not None

    def test_sequence_import(self):
        """Test that Sequence can be imported."""
        assert Sequence is not None

    def test_sequence_usage(self):
        """Test Sequence type usage."""
        def get_first(seq: Sequence[str]) -> Optional[str]:
            return seq[0] if seq else None

        assert get_first(["a", "b", "c"]) == "a"
        assert get_first("hello") == "h"

    def test_mutable_sequence_import(self):
        """Test that MutableSequence can be imported."""
        assert MutableSequence is not None


class TestUtilityTypes:
    """Test utility types and functions."""

    def test_type_checking_flag(self):
        """Test TYPE_CHECKING flag."""
        assert isinstance(TYPE_CHECKING, bool)
        # Should be False at runtime
        assert TYPE_CHECKING is False

    def test_cast_function(self):
        """Test cast function."""
        assert cast is not None
        assert callable(cast)

        # Cast should return the object unchanged at runtime
        result = cast(str, 42)
        assert result == 42

    def test_overload_decorator(self):
        """Test overload decorator."""
        assert overload is not None
        assert callable(overload)

        @overload
        def process(value: int) -> str: ...

        @overload
        def process(value: str) -> int: ...

        def process(value):
            if isinstance(value, int):
                return str(value)
            else:
                return len(value)

        assert process(42) == "42"
        assert process("hello") == 5

    def test_named_tuple_import(self):
        """Test that NamedTuple can be imported."""
        assert NamedTuple is not None

    def test_named_tuple_usage(self):
        """Test NamedTuple usage."""
        Point = NamedTuple('Point', [('x', int), ('y', int)])

        p = Point(1, 2)
        assert p.x == 1
        assert p.y == 2
        assert p[0] == 1
        assert p[1] == 2

    def test_new_type_import(self):
        """Test that NewType can be imported."""
        assert NewType is not None

    def test_new_type_usage(self):
        """Test NewType usage."""
        UserId = NewType('UserId', int)

        def get_user_name(user_id: UserId) -> str:
            return f"User {user_id}"

        user_id = UserId(12345)
        result = get_user_name(user_id)
        assert result == "User 12345"

        # Should have proper attributes
        assert hasattr(UserId, '__name__')
        assert hasattr(UserId, '__supertype__')


class TestTextAndPatternTypes:
    """Test text and pattern types."""

    def test_text_import(self):
        """Test that Text can be imported."""
        assert Text is not None

    def test_text_usage(self):
        """Test Text type usage."""
        def process_text(value: Text) -> int:
            return len(value)

        result = process_text("hello")
        assert result == 5

    def test_anystr_import(self):
        """Test that AnyStr can be imported."""
        assert AnyStr is not None

    def test_anystr_usage(self):
        """Test AnyStr usage."""
        def concat(a: AnyStr, b: AnyStr) -> AnyStr:
            return a + b

        # Should work with strings
        result_str = concat("hello", "world")
        assert result_str == "helloworld"

        # Should work with bytes
        result_bytes = concat(b"hello", b"world")
        assert result_bytes == b"helloworld"

    def test_pattern_import(self):
        """Test that Pattern can be imported."""
        assert Pattern is not None

    def test_match_import(self):
        """Test that Match can be imported."""
        assert Match is not None


class TestIOTypes:
    """Test IO types."""

    def test_io_import(self):
        """Test that IO can be imported."""
        assert IO is not None

    def test_text_io_import(self):
        """Test that TextIO can be imported."""
        assert TextIO is not None

    def test_binary_io_import(self):
        """Test that BinaryIO can be imported."""
        assert BinaryIO is not None


class TestSupportTypes:
    """Test support protocol types."""

    def test_supports_int_import(self):
        """Test that SupportsInt can be imported."""
        assert SupportsInt is not None

    def test_supports_float_import(self):
        """Test that SupportsFloat can be imported."""
        assert SupportsFloat is not None

    def test_supports_complex_import(self):
        """Test that SupportsComplex can be imported."""
        assert SupportsComplex is not None

    def test_supports_bytes_import(self):
        """Test that SupportsBytes can be imported."""
        assert SupportsBytes is not None

    def test_supports_abs_import(self):
        """Test that SupportsAbs can be imported."""
        assert SupportsAbs is not None

    def test_supports_round_import(self):
        """Test that SupportsRound can be imported."""
        assert SupportsRound is not None


class TestPy3m5Integration:
    """Test integration of py3m5 features."""

    def test_complex_type_annotations(self):
        """Test complex type annotations using py3m5 features."""
        def complex_function(
            data: Dict[str, List[Union[int, str]]],
            processor: Callable[[Any], str],
            optional_config: Optional[Dict[str, Any]] = None
        ) -> Tuple[List[str], int]:
            results = []
            count = 0

            for key, values in data.items():
                for value in values:
                    processed = processor(value)
                    results.append(f"{key}: {processed}")
                    count += 1

            return results, count

        # Test the function
        test_data = {
            "numbers": [1, 2, 3],
            "texts": ["a", "b"]
        }

        results, count = complex_function(test_data, str)
        assert count == 5
        assert len(results) == 5

    def test_generic_class_with_multiple_types(self):
        """Test generic class with multiple type parameters."""
        K = TypeVar('K')
        V = TypeVar('V')

        class KeyValueStore(Generic[K, V]):
            def __init__(self) -> None:
                self.store: Dict[K, V] = {}

            def put(self, key: K, value: V) -> None:
                self.store[key] = value

            def get(self, key: K) -> Optional[V]:
                return self.store.get(key)

            def keys(self) -> List[K]:
                return list(self.store.keys())

        # Test with string keys and int values
        store = KeyValueStore()  # Type will be inferred
        store.put("count", 42)
        store.put("total", 100)

        assert store.get("count") == 42
        assert store.get("total") == 100
        assert len(store.keys()) == 2


class TestPy3m5Fallbacks:
    """Test fallback behavior for Python 3.5+ features."""

    def test_fallback_imports_work(self):
        """Test that fallback implementations work."""
        # All imports should work regardless of Python version
        types_to_test = [
            Any, Union, Optional, Tuple, Callable, TypeVar, Generic,
            List, Dict, Set, FrozenSet,
            Iterable, Iterator, Mapping, MutableMapping, Sequence, MutableSequence,
            TYPE_CHECKING, cast, overload, NamedTuple, NewType,
            Text, AnyStr, Pattern, Match, IO, TextIO, BinaryIO,
            SupportsInt, SupportsFloat, SupportsComplex, SupportsBytes, SupportsAbs, SupportsRound
        ]

        for type_obj in types_to_test:
            assert type_obj is not None

    def test_fallback_functionality(self):
        """Test that fallback implementations provide basic functionality."""
        # Test Union fallback
        union_type = Union[int, str]
        assert union_type is not None

        # Test Optional fallback
        optional_type = Optional[str]
        assert optional_type is not None

        # Test cast fallback
        result = cast(str, 42)
        assert result == 42

        # Test overload fallback
        @overload
        def test_func(x: int) -> str: ...

        def test_func(x):
            return str(x)

        assert test_func(42) == "42"


class TestPy3m5RealWorldUsage:
    """Test real-world usage patterns with Python 3.5+ features."""

    def test_data_processing_pipeline(self):
        """Test data processing pipeline using py3m5 features."""
        T = TypeVar('T')
        U = TypeVar('U')

        def map_items(items: Iterable[T], func: Callable[[T], U]) -> List[U]:
            return [func(item) for item in items]

        def filter_items(items: Iterable[T], predicate: Callable[[T], bool]) -> List[T]:
            return [item for item in items if predicate(item)]

        def reduce_items(items: Iterable[T], func: Callable[[T, T], T]) -> Optional[T]:
            iterator = iter(items)
            try:
                result = next(iterator)
                for item in iterator:
                    result = func(result, item)
                return result
            except StopIteration:
                return None

        # Test the pipeline
        numbers = [1, 2, 3, 4, 5]

        # Map: square each number
        squared = map_items(numbers, lambda x: x * x)
        assert squared == [1, 4, 9, 16, 25]

        # Filter: only even numbers
        even_squared = filter_items(squared, lambda x: x % 2 == 0)
        assert even_squared == [4, 16]

        # Reduce: sum all numbers
        total = reduce_items(even_squared, lambda a, b: a + b)
        assert total == 20

    def test_configuration_system(self):
        """Test configuration system using py3m5 typing features."""
        ConfigValue = Union[str, int, bool, List[str]]

        class Configuration:
            def __init__(self) -> None:
                self.settings: Dict[str, ConfigValue] = {}

            def set(self, key: str, value: ConfigValue) -> None:
                self.settings[key] = value

            def get(self, key: str, default: Optional[ConfigValue] = None) -> Optional[ConfigValue]:
                return self.settings.get(key, default)

            def get_str(self, key: str, default: str = "") -> str:
                value = self.get(key, default)
                return str(value) if value is not None else default

            def get_int(self, key: str, default: int = 0) -> int:
                value = self.get(key, default)
                return int(value) if isinstance(value, (int, str)) else default

            def get_bool(self, key: str, default: bool = False) -> bool:
                value = self.get(key, default)
                if isinstance(value, bool):
                    return value
                elif isinstance(value, str):
                    return value.lower() in ("true", "yes", "1", "on")
                else:
                    return default

        # Test the configuration system
        config = Configuration()
        config.set("app_name", "MyApp")
        config.set("port", 8080)
        config.set("debug", True)
        config.set("features", ["auth", "logging", "metrics"])

        assert config.get_str("app_name") == "MyApp"
        assert config.get_int("port") == 8080
        assert config.get_bool("debug") is True
        assert config.get("features") == ["auth", "logging", "metrics"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
