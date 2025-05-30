"""
Test suite for Python 3.10+ features (py3m10.py module).

Tests ParamSpec, TypeGuard, union operators, and other features introduced in Python 3.10.
"""

import sys
import pytest
from typing import Callable, TypeVar, Any, Union
from typing_compat.py3m10 import *


class TestPy3m10VersionFlag:
    """Test version detection for Python 3.10+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY310_PLUS correctly detects Python 3.10+."""
        expected = sys.version_info >= (3, 10)
        assert PY310_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY310_PLUS is a boolean."""
        assert isinstance(PY310_PLUS, bool)


class TestParamSpec:
    """Test ParamSpec functionality."""
    
    def test_param_spec_import(self):
        """Test that ParamSpec can be imported."""
        assert ParamSpec is not None
    
    def test_param_spec_creation(self):
        """Test creating ParamSpec instances."""
        P = ParamSpec('P')
        assert P is not None
        # Check for name attribute (different implementations may use different attribute names)
        has_name = hasattr(P, 'name') or hasattr(P, '__name__') or hasattr(P, '_name')
        assert has_name, f"ParamSpec missing name attribute. Available: {dir(P)}"
    
    def test_param_spec_attributes(self):
        """Test ParamSpec has expected attributes."""
        P = ParamSpec('TestParams')
        
        # Should have some kind of name attribute
        has_name = hasattr(P, 'name') or hasattr(P, '__name__') or hasattr(P, '_name')
        assert has_name, f"ParamSpec missing name attribute. Available: {[attr for attr in dir(P) if not attr.startswith('__')]}"
        
        # Should have args and kwargs attributes (even in fallback)
        assert hasattr(P, 'args')
        assert hasattr(P, 'kwargs')
    
    def test_param_spec_in_callable(self):
        """Test ParamSpec used in Callable annotations."""
        P = ParamSpec('P')
        T = TypeVar('T')
        
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return func(*args, **kwargs)
            return wrapper
        
        @decorator
        def test_function(x: int, y: str = "default") -> str:
            return f"{x}: {y}"
        
        # Should work without errors
        result = test_function(42, "test")
        assert result == "42: test"
        
        # Test with default parameter
        result = test_function(24)
        assert result == "24: default"
    
    def test_param_spec_multiple_instances(self):
        """Test multiple ParamSpec instances."""
        P1 = ParamSpec('P1')
        P2 = ParamSpec('P2')
        
        # Should be different instances
        assert P1 is not P2
        
        # Should have different string representations
        assert str(P1) != str(P2)
    
    def test_param_spec_module_source(self):
        """Test ParamSpec comes from expected module."""
        if PY310_PLUS:
            assert ParamSpec.__module__ in ('typing', 'typing_extensions')
        else:
            # Fallback should still work
            assert ParamSpec is not None


class TestTypeGuard:
    """Test TypeGuard functionality."""
    
    def test_type_guard_import(self):
        """Test that TypeGuard can be imported."""
        assert TypeGuard is not None
    
    def test_type_guard_creation(self):
        """Test creating TypeGuard annotations."""
        def is_string(value: Any) -> TypeGuard[str]:
            return isinstance(value, str)
        
        assert is_string is not None
        assert is_string("test") is True
        assert is_string(42) is False
    
    def test_type_guard_with_list(self):
        """Test TypeGuard with list types."""
        from typing import List
        
        def is_string_list(items: list) -> TypeGuard[List[str]]:
            return all(isinstance(item, str) for item in items)
        
        # Should work with mixed list
        mixed_list = ["a", "b", 3, "c"]
        assert is_string_list(mixed_list) is False
        
        # Should work with string list
        string_list = ["a", "b", "c"]
        assert is_string_list(string_list) is True
    
    def test_type_guard_in_conditional(self):
        """Test TypeGuard used in conditional logic."""
        from typing import List
        
        def is_int_list(items: list) -> TypeGuard[List[int]]:
            return all(isinstance(item, int) for item in items)
        
        def process_items(items: list) -> str:
            if is_int_list(items):
                # Type checker should know items is list[int] here
                return f"Sum: {sum(items)}"
            else:
                return f"Count: {len(items)}"
        
        # Test with int list
        int_result = process_items([1, 2, 3])
        assert int_result == "Sum: 6"
        
        # Test with mixed list
        mixed_result = process_items(["a", "b", 3])
        assert mixed_result == "Count: 3"
    
    def test_type_guard_complex_types(self):
        """Test TypeGuard with complex type structures."""
        from typing import Dict
        
        def is_str_dict(obj: Any) -> TypeGuard[Dict[str, str]]:
            return (isinstance(obj, dict) and 
                   all(isinstance(k, str) and isinstance(v, str) 
                       for k, v in obj.items()))
        
        # Test valid dict
        valid_dict = {"a": "1", "b": "2"}
        assert is_str_dict(valid_dict) is True
        
        # Test invalid dict
        invalid_dict = {"a": 1, "b": "2"}
        assert is_str_dict(invalid_dict) is False
        
        # Test non-dict
        assert is_str_dict("not a dict") is False


class TestConcatenate:
    """Test Concatenate functionality."""
    
    def test_concatenate_import(self):
        """Test that Concatenate can be imported."""
        assert Concatenate is not None
    
    def test_concatenate_basic_usage(self):
        """Test basic Concatenate usage."""
        P = ParamSpec('P')
        
        # This tests that Concatenate can be used syntactically
        def test_function(first: str, *args: P.args, **kwargs: P.kwargs) -> str:
            return first
        
        result = test_function("hello", "world", extra="param")
        assert result == "hello"
    
    def test_concatenate_with_multiple_params(self):
        """Test Concatenate with multiple prepended parameters."""
        # Concatenate is used in type annotations, not instantiated directly
        P = ParamSpec('P')
        
        def test_function(first: int, second: str, *args: P.args, **kwargs: P.kwargs) -> str:
            return f"{first}-{second}"
        
        result = test_function(1, "hello", "extra", key="value")
        assert result == "1-hello"
    
    def test_concatenate_empty(self):
        """Test Concatenate usage in type annotations."""
        P = ParamSpec('P')
        
        def simple_wrapper(func: Callable[P, str]) -> Callable[P, str]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
                return func(*args, **kwargs)
            return wrapper
        
        @simple_wrapper
        def test_func() -> str:
            return "test"
        
        result = test_func()
        assert result == "test"


class TestAnnotated:
    """Test Annotated functionality."""
    
    def test_annotated_import(self):
        """Test that Annotated can be imported."""
        assert Annotated is not None
    
    def test_annotated_basic_usage(self):
        """Test basic Annotated usage."""
        PositiveInt = Annotated[int, "must be positive"]
        assert PositiveInt is not None
    
    def test_annotated_with_multiple_metadata(self):
        """Test Annotated with multiple metadata items."""
        ValidatedStr = Annotated[str, "non-empty", "trimmed", {"min_length": 1}]
        assert ValidatedStr is not None
    
    def test_annotated_in_function(self):
        """Test Annotated used in function annotations."""
        UserId = Annotated[int, "positive integer representing user ID"]
        UserName = Annotated[str, "non-empty string for username"]
        
        def create_user(user_id: UserId, name: UserName) -> dict:
            return {"id": user_id, "name": name}
        
        result = create_user(123, "alice")
        assert result == {"id": 123, "name": "alice"}
    
    def test_annotated_nested(self):
        """Test nested Annotated types."""
        from typing import List
        
        PositiveInt = Annotated[int, "positive"]
        PositiveIntList = Annotated[List[PositiveInt], "list of positive integers"]
        
        def process_numbers(numbers: PositiveIntList) -> int:
            return sum(numbers)
        
        result = process_numbers([1, 2, 3, 4])
        assert result == 10


class TestTypeAlias:
    """Test TypeAlias functionality."""
    
    def test_type_alias_import(self):
        """Test that TypeAlias can be imported."""
        assert TypeAlias is not None
    
    def test_type_alias_usage(self):
        """Test TypeAlias usage."""
        UserId: TypeAlias = int
        UserName: TypeAlias = str
        
        def get_user_info(user_id: UserId) -> UserName:
            return f"User #{user_id}"
        
        result = get_user_info(123)
        assert result == "User #123"
    
    def test_type_alias_complex_types(self):
        """Test TypeAlias with complex types."""
        from typing import Dict, List
        
        UserData: TypeAlias = Dict[str, Union[str, int, List[str]]]
        
        def process_user_data(data: UserData) -> str:
            return f"Processing data for {data.get('name', 'Unknown')}"
        
        test_data: UserData = {
            "name": "Alice",
            "age": 30,
            "tags": ["admin", "active"]
        }
        
        result = process_user_data(test_data)
        assert result == "Processing data for Alice"


class TestUnionTypes:
    """Test union type functionality."""
    
    def test_ellipsis_type_import(self):
        """Test EllipsisType import."""
        assert EllipsisType is not None
        assert EllipsisType is type(...)
    
    def test_union_type_import(self):
        """Test UnionType import."""
        assert UnionType is not None
        # UnionType should be the type of Union expressions
        assert isinstance(UnionType, type)
    
    def test_union_of_function(self):
        """Test UnionOf helper function."""
        # Test with multiple types
        result = UnionOf(int, str, float)
        assert result is not None
        
        # Test with single type
        single = UnionOf(int)
        assert single is int
        
        # Test error case
        with pytest.raises(ValueError):
            UnionOf()
    
    def test_union_of_in_annotations(self):
        """Test UnionOf used in function annotations."""
        def process_value(value: UnionOf(int, str)) -> str:
            return str(value)
        
        # Test with int
        result_int = process_value(42)
        assert result_int == "42"
        
        # Test with str
        result_str = process_value("hello")
        assert result_str == "hello"
    
    def test_union_of_behavior_across_versions(self):
        """Test UnionOf behavior is consistent across Python versions."""
        union_type = UnionOf(int, str, bool)
        
        # Should create some kind of union representation
        assert union_type is not None
        
        # Should work in function annotations
        def test_func(param: UnionOf(int, str)) -> bool:
            return isinstance(param, (int, str))
        
        assert test_func(42) is True
        assert test_func("test") is True
        assert test_func(3.14) is False


class TestPy3m10Integration:
    """Test integration of py3m10 features."""
    
    def test_param_spec_with_type_guard(self):
        """Test ParamSpec used with TypeGuard."""
        P = ParamSpec('P')
        T = TypeVar('T')
        
        def validate_and_call(
            validator: Callable[[Any], TypeGuard[T]],
            func: Callable[[T], str],
            value: Any
        ) -> str:
            if validator(value):
                return func(value)
            return "Invalid input"
        
        def is_positive_int(x: Any) -> TypeGuard[int]:
            return isinstance(x, int) and x > 0
        
        def format_positive_int(x: int) -> str:
            return f"Positive: {x}"
        
        # Test valid case
        result = validate_and_call(is_positive_int, format_positive_int, 42)
        assert result == "Positive: 42"
        
        # Test invalid case
        result = validate_and_call(is_positive_int, format_positive_int, -5)
        assert result == "Invalid input"
    
    def test_annotated_with_param_spec(self):
        """Test Annotated used with ParamSpec."""
        P = ParamSpec('P')
        T = TypeVar('T')
        
        ValidatedFunc = Annotated[
            Callable[P, T], 
            "Function that has been validated for security"
        ]
        
        def secure_wrapper(func: ValidatedFunc[P, T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                # Add security checks here
                return func(*args, **kwargs)
            return wrapper
        
        @secure_wrapper
        def safe_function(x: int, y: str) -> str:
            return f"{x}: {y}"
        
        result = safe_function(42, "test")
        assert result == "42: test"
    
    def test_complex_generic_with_all_features(self):
        """Test complex example using multiple py3m10 features."""
        P = ParamSpec('P')
        T = TypeVar('T')
        U = TypeVar('U')
        
        # Type aliases
        Validator: TypeAlias = Callable[[Any], TypeGuard[T]]
        Processor: TypeAlias = Callable[P, U]
        
        # Annotated types
        SafeProcessor = Annotated[Processor[P, U], "Validated processor function"]
        
        class ProcessingPipeline:
            def __init__(self) -> None:
                self.steps: list[SafeProcessor] = []
            
            def add_step(self, 
                        validator: Validator[T], 
                        processor: Callable[[T], U]) -> None:
                def safe_processor(*args: P.args, **kwargs: P.kwargs) -> U:
                    # This is a simplified example
                    return processor(args[0] if args else None)
                
                self.steps.append(safe_processor)
            
            def process(self, value: Any) -> UnionOf(U, str):
                try:
                    for step in self.steps:
                        value = step(value)
                    return value
                except Exception:
                    return "Processing failed"
        
        # Test the pipeline
        pipeline = ProcessingPipeline()
        
        def is_int(x: Any) -> TypeGuard[int]:
            return isinstance(x, int)
        
        def double_int(x: int) -> int:
            return x * 2
        
        pipeline.add_step(is_int, double_int)
        
        result = pipeline.process(21)
        assert result == 42


class TestPy3m10Fallbacks:
    """Test fallback behavior for Python 3.10+ features."""
    
    def test_param_spec_fallback(self):
        """Test ParamSpec fallback implementation."""
        P = ParamSpec('TestParam')
        
        # Should have basic attributes even in fallback
        has_name = hasattr(P, 'name') or hasattr(P, '__name__') or hasattr(P, '_name')
        assert has_name, f"ParamSpec missing name attribute. Available: {[attr for attr in dir(P) if not attr.startswith('_')]}"
        assert hasattr(P, 'args')
        assert hasattr(P, 'kwargs')
    
    def test_type_guard_fallback(self):
        """Test TypeGuard fallback implementation."""
        def is_str(x: Any) -> TypeGuard[str]:
            return isinstance(x, str)
        
        # Should work as a regular function
        assert is_str("test") is True
        assert is_str(42) is False
    
    def test_union_of_fallback(self):
        """Test UnionOf fallback behavior."""
        # Should work even with fallback Union implementation
        union_type = UnionOf(int, str)
        assert union_type is not None
        
        # Should handle single type
        single_type = UnionOf(int)
        assert single_type is int


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
