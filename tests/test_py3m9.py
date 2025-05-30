"""
Test suite for Python 3.9+ features (py3m9.py module).

Tests built-in generic types and collections.abc imports introduced in Python 3.9.
"""

import sys
import pytest
from typing_compat.py3m9 import *


class TestPy3m9VersionFlag:
    """Test version detection for Python 3.9+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY39_PLUS correctly detects Python 3.9+."""
        expected = sys.version_info >= (3, 9)
        assert PY39_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY39_PLUS is a boolean."""
        assert isinstance(PY39_PLUS, bool)


class TestBuiltinGenerics:
    """Test built-in generic types (list, dict, set, etc.)."""
    
    def test_list_type(self):
        """Test List type import and behavior."""
        assert List is not None
        
        if PY39_PLUS:
            # Should be the built-in list type
            assert List is list
        else:
            # Should be from typing module
            from typing import List as TypingList
            assert List is TypingList
    
    def test_dict_type(self):
        """Test Dict type import and behavior."""
        assert Dict is not None
        
        if PY39_PLUS:
            # Should be the built-in dict type
            assert Dict is dict
        else:
            # Should be from typing module
            from typing import Dict as TypingDict
            assert Dict is TypingDict
    
    def test_set_type(self):
        """Test Set type import and behavior."""
        assert Set is not None
        
        if PY39_PLUS:
            # Should be the built-in set type
            assert Set is set
        else:
            # Should be from typing module
            from typing import Set as TypingSet
            assert Set is TypingSet
    
    def test_frozenset_type(self):
        """Test FrozenSet type import and behavior."""
        assert FrozenSet is not None
        
        if PY39_PLUS:
            # Should be the built-in frozenset type
            assert FrozenSet is frozenset
        else:
            # Should be from typing module
            from typing import FrozenSet as TypingFrozenSet
            assert FrozenSet is TypingFrozenSet
    
    def test_tuple_type(self):
        """Test Tuple type import and behavior."""
        assert Tuple is not None
        
        if PY39_PLUS:
            # Should be the built-in tuple type
            assert Tuple is tuple
        else:
            # Should be from typing module
            from typing import Tuple as TypingTuple
            assert Tuple is TypingTuple
    
    def test_type_type(self):
        """Test Type type import and behavior."""
        assert Type is not None
        
        if PY39_PLUS:
            # Should be the built-in type type
            assert Type is type
        else:
            # Should be from typing module
            from typing import Type as TypingType
            assert Type is TypingType


class TestGenericTypeUsage:
    """Test using generic types in annotations."""
    
    def test_list_annotation(self):
        """Test List type in function annotations."""
        def process_strings(items: List[str]) -> int:
            return len(items)
        
        # Should work with both built-in and typing versions
        result = process_strings(["a", "b", "c"])
        assert result == 3
        
        # Check annotation
        annotation = process_strings.__annotations__['items']
        if PY39_PLUS:
            # Might be list[str] or List[str] depending on how it's used
            assert annotation is not None
        else:
            assert annotation is not None
    
    def test_dict_annotation(self):
        """Test Dict type in function annotations."""
        def process_mapping(data: Dict[str, int]) -> List[str]:
            return list(data.keys())
        
        result = process_mapping({"a": 1, "b": 2})
        assert result == ["a", "b"]
    
    def test_set_annotation(self):
        """Test Set type in function annotations."""
        def get_unique_items(items: List[str]) -> Set[str]:
            return set(items)
        
        result = get_unique_items(["a", "b", "a", "c"])
        assert len(result) == 3
        assert "a" in result
        assert "b" in result
        assert "c" in result
    
    def test_tuple_annotation(self):
        """Test Tuple type in function annotations."""
        def create_pair(a: str, b: int) -> Tuple[str, int]:
            return (a, b)
        
        result = create_pair("test", 42)
        assert result == ("test", 42)
    
    def test_nested_generics(self):
        """Test nested generic types."""
        def process_nested(data: Dict[str, List[int]]) -> Set[str]:
            return set(data.keys())
        
        test_data = {"numbers": [1, 2, 3], "values": [4, 5, 6]}
        result = process_nested(test_data)
        assert result == {"numbers", "values"}


class TestCollectionsABC:
    """Test collections.abc types."""
    
    def test_iterable_import(self):
        """Test Iterable import."""
        assert Iterable is not None
        
        def process_iterable(items: Iterable[str]) -> int:
            return sum(1 for _ in items)
        
        result = process_iterable(["a", "b", "c"])
        assert result == 3
    
    def test_iterator_import(self):
        """Test Iterator import."""
        assert Iterator is not None
        
        def create_iterator() -> Iterator[int]:
            yield 1
            yield 2
            yield 3
        
        result = list(create_iterator())
        assert result == [1, 2, 3]
    
    def test_container_import(self):
        """Test Container import."""
        assert Container is not None
        
        def check_membership(container: Container[str], item: str) -> bool:
            return item in container
        
        result = check_membership(["a", "b", "c"], "b")
        assert result is True
    
    def test_collection_import(self):
        """Test Collection import."""
        assert Collection is not None
        
        def get_collection_size(coll: Collection[str]) -> int:
            return len(coll)
        
        result = get_collection_size(["a", "b", "c"])
        assert result == 3
    
    def test_sized_import(self):
        """Test Sized import."""
        assert Sized is not None
        
        def check_size(obj: Sized) -> int:
            return len(obj)
        
        result = check_size([1, 2, 3, 4])
        assert result == 4
    
    def test_mapping_types(self):
        """Test Mapping and MutableMapping imports."""
        assert Mapping is not None
        assert MutableMapping is not None
        
        def process_mapping(data: Mapping[str, int]) -> List[int]:
            return list(data.values())
        
        def modify_mapping(data: MutableMapping[str, int]) -> None:
            data["new"] = 42
        
        # Test with regular dict
        test_dict = {"a": 1, "b": 2}
        values = process_mapping(test_dict)
        assert set(values) == {1, 2}
        
        modify_mapping(test_dict)
        assert test_dict["new"] == 42
    
    def test_sequence_types(self):
        """Test Sequence and MutableSequence imports."""
        assert Sequence is not None
        assert MutableSequence is not None
        
        def process_sequence(seq: Sequence[str]) -> str:
            return seq[0] if seq else ""
        
        def modify_sequence(seq: MutableSequence[str]) -> None:
            seq.append("new")
        
        # Test with list
        test_list = ["a", "b", "c"]
        first = process_sequence(test_list)
        assert first == "a"
        
        modify_sequence(test_list)
        assert "new" in test_list
    
    def test_set_types(self):
        """Test AbstractSet and MutableSet imports."""
        assert AbstractSet is not None
        assert MutableSet is not None
        
        def process_set(s: AbstractSet[str]) -> int:
            return len(s)
        
        def modify_set(s: MutableSet[str]) -> None:
            s.add("new")
        
        test_set = {"a", "b", "c"}
        size = process_set(test_set)
        assert size == 3
        
        modify_set(test_set)
        assert "new" in test_set
    
    def test_view_types(self):
        """Test ItemsView, KeysView, ValuesView imports."""
        assert ItemsView is not None
        assert KeysView is not None
        assert ValuesView is not None
        
        def process_keys(keys: KeysView[str]) -> List[str]:
            return list(keys)
        
        def process_values(values: ValuesView[int]) -> List[int]:
            return list(values)
        
        def process_items(items: ItemsView[str, int]) -> Dict[str, int]:
            return dict(items)
        
        test_dict = {"a": 1, "b": 2, "c": 3}
        
        keys = process_keys(test_dict.keys())
        assert set(keys) == {"a", "b", "c"}
        
        values = process_values(test_dict.values())
        assert set(values) == {1, 2, 3}
        
        items = process_items(test_dict.items())
        assert items == test_dict
    
    def test_reversible_import(self):
        """Test Reversible import."""
        assert Reversible is not None
        
        def process_reversible(rev: Reversible[str]) -> List[str]:
            return list(reversed(rev))
        
        result = process_reversible(["a", "b", "c"])
        assert result == ["c", "b", "a"]


class TestPy3m9Integration:
    """Test integration of py3m9 features."""
    
    def test_complex_type_annotations(self):
        """Test complex type annotations using py3m9 features."""
        def complex_function(
            data: Dict[str, List[int]],
            lookup: Mapping[str, Set[str]],
            results: MutableSequence[Tuple[str, int]]
        ) -> Iterator[Dict[str, Any]]:
            for key, values in data.items():
                for value in values:
                    yield {"key": key, "value": value}
        
        # Should create without errors
        assert complex_function is not None
        
        # Test execution
        test_data = {"numbers": [1, 2], "values": [3, 4]}
        test_lookup = {"a": {"x", "y"}}
        test_results = []
        
        results = list(complex_function(test_data, test_lookup, test_results))
        assert len(results) == 4
        assert all("key" in r and "value" in r for r in results)
    
    def test_generic_class_with_builtin_types(self):
        """Test generic class using built-in types."""
        from typing import TypeVar, Generic
        
        T = TypeVar('T')
        
        class Container(Generic[T]):
            def __init__(self) -> None:
                self.items: List[T] = []
                self.metadata: Dict[str, str] = {}
            
            def add(self, item: T) -> None:
                self.items.append(item)
            
            def get_all(self) -> Tuple[List[T], Dict[str, str]]:
                return (self.items.copy(), self.metadata.copy())
        
        # Test with string container
        container: Container[str] = Container()
        container.add("test")
        container.metadata["version"] = "1.0"
        
        items, meta = container.get_all()
        assert items == ["test"]
        assert meta["version"] == "1.0"


class TestPy3m9Compatibility:
    """Test compatibility across Python versions."""
    
    def test_type_equivalence(self):
        """Test that types work equivalently across versions."""
        # These should work the same regardless of Python version
        def test_function(
            a: List[str],
            b: Dict[str, int], 
            c: Set[str],
            d: Tuple[str, ...],
            e: Type[str]
        ) -> bool:
            return True
        
        # Should create and call without errors
        assert test_function([], {}, set(), (), str) is True
    
    def test_runtime_behavior_consistency(self):
        """Test that runtime behavior is consistent."""
        # Collections should behave the same
        test_list: List[int] = [1, 2, 3]
        test_dict: Dict[str, int] = {"a": 1}
        test_set: Set[str] = {"x", "y"}
        
        assert len(test_list) == 3
        assert test_dict["a"] == 1
        assert "x" in test_set
        
        # Should be able to use all collection methods
        test_list.append(4)
        test_dict["b"] = 2
        test_set.add("z")
        
        assert 4 in test_list
        assert test_dict["b"] == 2
        assert "z" in test_set


class TestPy3m9ErrorCases:
    """Test error handling and edge cases."""
    
    def test_invalid_generic_usage(self):
        """Test error cases with generic types."""
        # These should either work or raise appropriate exceptions
        try:
            # Some type checkers might catch this
            invalid_list: List = []  # Missing type parameter
            assert invalid_list is not None
        except (TypeError, NameError):
            pass
    
    def test_type_checking_behavior(self):
        """Test behavior with type checking tools."""
        # These annotations should be valid for type checkers
        def type_heavy_function(
            sequences: Sequence[MutableSequence[str]],
            mappings: Mapping[str, MutableMapping[str, int]],
            containers: Container[AbstractSet[str]]
        ) -> Collection[Iterable[str]]:
            return []
        
        # Should create without errors
        assert type_heavy_function is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
