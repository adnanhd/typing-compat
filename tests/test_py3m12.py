"""
Test suite for Python 3.12+ features (py3m12.py module).

Tests override, TypeIs, Buffer, and other features introduced in Python 3.12.
"""

import sys
import pytest
from typing import Any
from typing_compat.py3m12 import *


class TestPy3m12VersionFlag:
    """Test version detection for Python 3.12+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY312_PLUS correctly detects Python 3.12+."""
        expected = sys.version_info >= (3, 12)
        assert PY312_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY312_PLUS is a boolean."""
        assert isinstance(PY312_PLUS, bool)


class TestHashable:
    """Test Hashable type functionality."""
    
    def test_hashable_import(self):
        """Test that Hashable can be imported."""
        assert Hashable is not None
    
    def test_hashable_in_function_annotation(self):
        """Test Hashable used in function annotations."""
        def process_hashable(item: Hashable) -> int:
            return hash(item)
        
        # Test with hashable types
        assert process_hashable("string") is not None
        assert process_hashable(42) is not None
        assert process_hashable((1, 2, 3)) is not None
    
    def test_hashable_type_checking(self):
        """Test Hashable for type checking purposes."""
        def add_to_set(items: list[Hashable]) -> set[Hashable]:
            return set(items)
        
        result = add_to_set(["a", "b", 1, 2, (3, 4)])
        assert len(result) == 5
        assert "a" in result
        assert 1 in result
        assert (3, 4) in result
    
    def test_hashable_with_dict_keys(self):
        """Test Hashable with dictionary keys."""
        def create_dict(keys: list[Hashable], values: list[Any]) -> dict[Hashable, Any]:
            return dict(zip(keys, values))
        
        keys = ["str_key", 42, (1, 2)]
        values = ["value1", "value2", "value3"]
        
        result = create_dict(keys, values)
        assert result["str_key"] == "value1"
        assert result[42] == "value2"
        assert result[(1, 2)] == "value3"


class TestBuffer:
    """Test Buffer type functionality."""
    
    def test_buffer_import(self):
        """Test that Buffer can be imported."""
        assert Buffer is not None
    
    def test_buffer_in_function_annotation(self):
        """Test Buffer used in function annotations."""
        def process_buffer(data: Buffer) -> int:
            return len(data)
        
        # Test with bytes (should work as Buffer-like)
        result = process_buffer(b"hello world")
        assert result == 11
        
        # Test with bytearray
        result = process_buffer(bytearray(b"test"))
        assert result == 4
    
    def test_buffer_type_behavior(self):
        """Test Buffer type behavior."""
        if PY312_PLUS:
            # On Python 3.12+, Buffer should be from collections.abc
            # Test basic functionality
            def read_buffer(buf: Buffer) -> bytes:
                if hasattr(buf, '__bytes__'):
                    return bytes(buf)
                return buf if isinstance(buf, bytes) else b''
            
            result = read_buffer(b"test data")
            assert result == b"test data"
        else:
            # Fallback behavior - Buffer should be bytes
            assert Buffer is bytes or callable(Buffer)


class TestOverride:
    """Test override decorator functionality."""
    
    def test_override_import(self):
        """Test that override can be imported."""
        assert override is not None
        assert callable(override)
    
    def test_override_basic_usage(self):
        """Test basic override decorator usage."""
        class Animal:
            def make_sound(self) -> str:
                return "Some generic animal sound"
            
            def move(self) -> str:
                return "Moving"
        
        class Dog(Animal):
            @override
            def make_sound(self) -> str:
                return "Woof!"
            
            @override
            def move(self) -> str:
                return "Running"
        
        dog = Dog()
        assert dog.make_sound() == "Woof!"
        assert dog.move() == "Running"
    
    def test_override_with_multiple_inheritance(self):
        """Test override with multiple inheritance."""
        class Flyable:
            def fly(self) -> str:
                return "Flying in the sky"
        
        class Swimable:
            def swim(self) -> str:
                return "Swimming in water"
        
        class Duck(Flyable, Swimable):
            @override
            def fly(self) -> str:
                return "Duck flying"
            
            @override
            def swim(self) -> str:
                return "Duck swimming"
        
        duck = Duck()
        assert duck.fly() == "Duck flying"
        assert duck.swim() == "Duck swimming"
    
    def test_override_with_properties(self):
        """Test override with property methods."""
        class Vehicle:
            @property
            def speed(self) -> int:
                return 0
            
            @speed.setter
            def speed(self, value: int) -> None:
                pass
        
        class Car(Vehicle):
            def __init__(self) -> None:
                self._speed = 0
            
            @property
            @override
            def speed(self) -> int:
                return self._speed
            
            @speed.setter
            @override
            def speed(self, value: int) -> None:
                self._speed = max(0, value)
        
        car = Car()
        car.speed = 60
        assert car.speed == 60
        
        car.speed = -10
        assert car.speed == 0  # Should not allow negative speed
    
    def test_override_in_abstract_context(self):
        """Test override with abstract methods."""
        from abc import ABC, abstractmethod
        
        class Shape(ABC):
            @abstractmethod
            def area(self) -> float:
                pass
            
            @abstractmethod
            def perimeter(self) -> float:
                pass
        
        class Rectangle(Shape):
            def __init__(self, width: float, height: float) -> None:
                self.width = width
                self.height = height
            
            @override
            def area(self) -> float:
                return self.width * self.height
            
            @override
            def perimeter(self) -> float:
                return 2 * (self.width + self.height)
        
        rect = Rectangle(3.0, 4.0)
        assert rect.area() == 12.0
        assert rect.perimeter() == 14.0
    
    def test_override_fallback_behavior(self):
        """Test override decorator fallback behavior."""
        # In fallback mode, override should just return the function unchanged
        class Base:
            def method(self) -> str:
                return "base"
        
        class Derived(Base):
            @override
            def method(self) -> str:
                return "derived"
        
        derived = Derived()
        result = derived.method()
        assert result == "derived"


class TestTypeIs:
    """Test TypeIs functionality."""
    
    def test_type_is_import(self):
        """Test that TypeIs can be imported."""
        assert TypeIs is not None
    
    def test_type_is_basic_usage(self):
        """Test basic TypeIs usage."""
        def is_string(value: Any) -> TypeIs[str]:
            return isinstance(value, str)
        
        # Should work as a type guard
        assert is_string("hello") is True
        assert is_string(42) is False
        assert is_string(None) is False
    
    def test_type_is_with_complex_types(self):
        """Test TypeIs with complex type structures."""
        def is_string_list(value: Any) -> TypeIs[list[str]]:
            return (isinstance(value, list) and 
                   all(isinstance(item, str) for item in value))
        
        # Test valid string list
        assert is_string_list(["a", "b", "c"]) is True
        
        # Test invalid cases
        assert is_string_list(["a", "b", 3]) is False
        assert is_string_list("not a list") is False
        assert is_string_list([]) is True  # Empty list is valid
    
    def test_type_is_with_dict(self):
        """Test TypeIs with dictionary types."""
        def is_str_dict(value: Any) -> TypeIs[dict[str, str]]:
            return (isinstance(value, dict) and
                   all(isinstance(k, str) and isinstance(v, str) 
                       for k, v in value.items()))
        
        # Test valid dict
        assert is_str_dict({"a": "1", "b": "2"}) is True
        
        # Test invalid dicts
        assert is_str_dict({"a": 1, "b": "2"}) is False
        assert is_str_dict({1: "a", 2: "b"}) is False
        assert is_str_dict({}) is True  # Empty dict is valid
    
    def test_type_is_in_conditional_logic(self):
        """Test TypeIs used in conditional logic."""
        def is_positive_int(value: Any) -> TypeIs[int]:
            return isinstance(value, int) and value > 0
        
        def process_value(value: Any) -> str:
            if is_positive_int(value):
                # Type checker should know value is int here
                return f"Positive integer: {value}"
            else:
                return f"Not a positive integer: {type(value).__name__}"
        
        # Test positive int
        result = process_value(42)
        assert result == "Positive integer: 42"
        
        # Test negative int
        result = process_value(-5)
        assert result == "Not a positive integer: int"
        
        # Test non-int
        result = process_value("hello")
        assert result == "Not a positive integer: str"
    
    def test_type_is_vs_type_guard(self):
        """Test TypeIs behavior compared to TypeGuard."""
        # TypeIs is more precise than TypeGuard
        def is_int_with_type_is(value: Any) -> TypeIs[int]:
            return isinstance(value, int)
        
        # Test that it works as expected
        assert is_int_with_type_is(42) is True
        assert is_int_with_type_is(3.14) is False
        assert is_int_with_type_is("42") is False
    
    def test_type_is_fallback_behavior(self):
        """Test TypeIs fallback behavior."""
        # In fallback mode, should behave like a regular function returning bool
        def is_str_fallback(value: Any) -> TypeIs[str]:
            return isinstance(value, str)
        
        assert is_str_fallback("test") is True
        assert is_str_fallback(123) is False


class TestPy3m12Integration:
    """Test integration of py3m12 features."""
    
    def test_override_with_type_is(self):
        """Test override decorator with TypeIs type guards."""
        class Validator:
            def is_valid(self, value: Any) -> TypeIs[str]:
                return isinstance(value, str)
        
        class StrictValidator(Validator):
            @override
            def is_valid(self, value: Any) -> TypeIs[str]:
                return isinstance(value, str) and len(value) > 0
        
        validator = StrictValidator()
        
        assert validator.is_valid("hello") is True
        assert validator.is_valid("") is False
        assert validator.is_valid(42) is False
    
    def test_buffer_with_override(self):
        """Test Buffer type with override methods."""
        class DataProcessor:
            def process_data(self, data: Buffer) -> int:
                return len(data)
        
        class EnhancedProcessor(DataProcessor):
            @override
            def process_data(self, data: Buffer) -> int:
                # Enhanced processing that also validates
                if len(data) == 0:
                    return -1
                return len(data) * 2
        
        processor = EnhancedProcessor()
        
        result = processor.process_data(b"hello")
        assert result == 10  # 5 * 2
        
        result = processor.process_data(b"")
        assert result == -1
    
    def test_hashable_with_type_is(self):
        """Test Hashable type with TypeIs type guards."""
        def is_hashable_string(value: Any) -> TypeIs[str]:
            return isinstance(value, str) and isinstance(value, Hashable)
        
        def process_hashable_strings(items: list[Any]) -> set[str]:
            result = set()
            for item in items:
                if is_hashable_string(item):
                    result.add(item)
            return result
        
        mixed_items = ["hello", "world", 42, ["not", "hashable"], "test"]
        result = process_hashable_strings(mixed_items)
        
        assert result == {"hello", "world", "test"}
    
    def test_complex_inheritance_hierarchy(self):
        """Test complex inheritance with all py3m12 features."""
        class DataContainer:
            def __init__(self, data: Buffer) -> None:
                self.data = data
            
            def get_size(self) -> int:
                return len(self.data)
            
            def is_empty(self) -> bool:
                return self.get_size() == 0
        
        class ValidatedContainer(DataContainer):
            @override
            def __init__(self, data: Buffer) -> None:
                if not self._is_valid_buffer(data):
                    raise ValueError("Invalid buffer data")
                super().__init__(data)
            
            def _is_valid_buffer(self, data: Any) -> TypeIs[Buffer]:
                return hasattr(data, '__len__') and hasattr(data, '__getitem__')
            
            @override
            def get_size(self) -> int:
                # Validated version includes extra checks
                if self.is_empty():
                    return 0
                return super().get_size()
        
        # Test valid buffer
        container = ValidatedContainer(b"test data")
        assert container.get_size() == 9
        assert not container.is_empty()
        
        # Test empty buffer
        empty_container = ValidatedContainer(b"")
        assert empty_container.get_size() == 0
        assert empty_container.is_empty()


class TestPy3m12Fallbacks:
    """Test fallback behavior for Python 3.12+ features."""
    
    def test_hashable_fallback_location(self):
        """Test Hashable fallback from correct location."""
        # Should work regardless of Python version
        assert Hashable is not None
        
        # Should be usable in type annotations
        def test_func(item: Hashable) -> bool:
            try:
                hash(item)
                return True
            except TypeError:
                return False
        
        assert test_func("string") is True
        assert test_func(42) is True
    
    def test_buffer_fallback_behavior(self):
        """Test Buffer fallback behavior."""
        # In fallback mode, Buffer should work with bytes-like objects
        assert Buffer is not None
        
        # Should be usable in annotations
        def process_buffer_fallback(data: Buffer) -> int:
            return len(data)
        
        result = process_buffer_fallback(b"test")
        assert result == 4
    
    def test_override_fallback_decorator(self):
        """Test override fallback decorator behavior."""
        # Should work as a no-op decorator in fallback mode
        class TestClass:
            def method(self) -> str:
                return "original"
        
        class TestSubclass(TestClass):
            @override
            def method(self) -> str:
                return "overridden"
        
        instance = TestSubclass()
        assert instance.method() == "overridden"
    
    def test_type_is_fallback_function(self):
        """Test TypeIs fallback function behavior."""
        # Should work as a regular type guard in fallback mode
        def is_int_fallback(value: Any) -> TypeIs[int]:
            return isinstance(value, int)
        
        assert is_int_fallback(42) is True
        assert is_int_fallback("42") is False


class TestPy3m12ErrorCases:
    """Test error handling and edge cases."""
    
    def test_override_with_incorrect_signature(self):
        """Test override decorator with signature mismatches."""
        # This is mainly for demonstration - type checkers would catch this
        class Base:
            def method(self, x: int) -> str:
                return str(x)
        
        class Derived(Base):
            @override
            def method(self, x: int) -> str:  # Correct signature
                return f"Number: {x}"
        
        # Should work correctly
        derived = Derived()
        result = derived.method(42)
        assert result == "Number: 42"
    
    def test_type_is_edge_cases(self):
        """Test TypeIs with edge cases."""
        def is_non_empty_string(value: Any) -> TypeIs[str]:
            return isinstance(value, str) and len(value) > 0
        
        # Test edge cases
        assert is_non_empty_string("") is False
        assert is_non_empty_string("a") is True
        assert is_non_empty_string(None) is False
        assert is_non_empty_string(0) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
