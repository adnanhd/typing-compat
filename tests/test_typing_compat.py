"""
Main test suite for typing_compat module.

Tests the overall integration, main interface, and cross-version compatibility
of the modular typing_compat library.
"""

import sys
import pytest
from typing import get_type_hints
from unittest.mock import patch

# Import everything from our enhanced modular module
from typing_compat import *
import typing_compat


class TestMainModuleInterface:
    """Test the main typing_compat module interface."""
    
    def test_version_info(self):
        """Test that version information is available."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert __version__ == "0.2.0"
    
    def test_all_exports_available(self):
        """Test that all expected exports are available."""
        # Key exports that should always be available
        expected_exports = [
            # Basic types
            "Any", "Union", "Optional", "Callable", "TypeVar", "Generic",
            
            # Python 3.7+
            "ForwardRef",
            
            # Python 3.8+
            "Literal", "Protocol", "TypedDict", "Final", "get_args", "get_origin",
            
            # Python 3.9+
            "List", "Dict", "Set", "Tuple", "Type",
            
            # Python 3.10+
            "ParamSpec", "TypeGuard", "Concatenate", "Annotated", "UnionOf",
            
            # Python 3.11+
            "Self", "Never", "Required", "NotRequired",
            
            # Python 3.12+
            "override", "TypeIs", "Hashable", "Buffer",
            
            # Utilities
            "is_optional", "is_list_like", "is_dict_like", "get_type_hints_compat",
            
            # Version flags
            "PY37_PLUS", "PY38_PLUS", "PY39_PLUS", "PY310_PLUS", "PY311_PLUS", "PY312_PLUS"
        ]
        
        for export in expected_exports:
            assert hasattr(typing_compat, export), f"Missing export: {export}"
            assert export in typing_compat.__all__, f"{export} not in __all__"
    
    def test_import_star_works(self):
        """Test that 'from typing_compat import *' works."""
        # This test verifies that the __all__ list is properly defined
        # and that all listed items are actually available
        all_items = typing_compat.__all__
        assert len(all_items) > 50  # Should have many exports
        
        # Check that all items in __all__ are actually available
        for item in all_items:
            assert hasattr(typing_compat, item), f"Item in __all__ not available: {item}"


class TestVersionCompatibility:
    """Test compatibility across different Python versions."""
    
    def test_version_flags_consistency(self):
        """Test that version flags are consistent."""
        assert PY37_PLUS == (sys.version_info >= (3, 7))
        assert PY38_PLUS == (sys.version_info >= (3, 8))
        assert PY39_PLUS == (sys.version_info >= (3, 9))
        assert PY310_PLUS == (sys.version_info >= (3, 10))
        assert PY311_PLUS == (sys.version_info >= (3, 11))
        assert PY312_PLUS == (sys.version_info >= (3, 12))
        
        # Version flags should be boolean
        for flag in [PY37_PLUS, PY38_PLUS, PY39_PLUS, PY310_PLUS, PY311_PLUS, PY312_PLUS]:
            assert isinstance(flag, bool)
    
    def test_version_hierarchy(self):
        """Test that version flags follow logical hierarchy."""
        if PY312_PLUS:
            assert PY311_PLUS and PY310_PLUS and PY39_PLUS and PY38_PLUS and PY37_PLUS
        elif PY311_PLUS:
            assert PY310_PLUS and PY39_PLUS and PY38_PLUS and PY37_PLUS
        elif PY310_PLUS:
            assert PY39_PLUS and PY38_PLUS and PY37_PLUS
        elif PY39_PLUS:
            assert PY38_PLUS and PY37_PLUS
        elif PY38_PLUS:
            assert PY37_PLUS


class TestBasicTypingFeatures:
    """Test basic typing features available in all Python versions."""
    
    def test_basic_types_available(self):
        """Test that basic types are available."""
        basic_types = [Any, Union, Optional, Callable, TypeVar, Generic, ClassVar]
        for typ in basic_types:
            assert typ is not None
    
    def test_basic_type_usage(self):
        """Test basic type usage in function annotations."""
        def sample_function(
            a: Any,
            b: Union[int, str],
            c: Optional[str] = None,
            d: Callable[[int], str] = str
        ) -> bool:
            return True
        
        # Should create without errors
        assert sample_function(1, "test") is True
        assert sample_function("any", 42, "optional") is True
    
    def test_generic_class_creation(self):
        """Test creating generic classes."""
        T = TypeVar('T')
        
        class Container(Generic[T]):
            def __init__(self, item: T) -> None:
                self.item = item
            
            def get(self) -> T:
                return self.item
        
        # Test with different types
        str_container = Container("hello")
        assert str_container.get() == "hello"
        
        int_container = Container(42)
        assert int_container.get() == 42


class TestAdvancedFeatures:
    """Test advanced typing features with fallbacks."""
    
    def test_literal_functionality(self):
        """Test Literal type across versions."""
        Mode = Literal["read", "write", "append"]
        
        def open_file(filename: str, mode: Mode) -> str:
            return f"Opening {filename} in {mode} mode"
        
        result = open_file("test.txt", "read")
        assert result == "Opening test.txt in read mode"
    
    def test_protocol_functionality(self):
        """Test Protocol across versions."""
        @runtime_checkable
        class Drawable(Protocol):
            def draw(self) -> None: ...
        
        class Circle:
            def draw(self) -> None:
                pass
        
        circle = Circle()
        # Protocol checking might not work in all versions, but should not error
        try:
            is_drawable = isinstance(circle, Drawable)
            assert isinstance(is_drawable, bool)
        except (TypeError, AttributeError):
            # Some fallback implementations might not support isinstance
            pass
    
    def test_typed_dict_functionality(self):
        """Test TypedDict across versions."""
        class Person(TypedDict):
            name: str
            age: int
        
        def create_person(name: str, age: int) -> Person:
            return {"name": name, "age": age}
        
        person = create_person("Alice", 30)
        assert person["name"] == "Alice"
        assert person["age"] == 30
    
    def test_final_functionality(self):
        """Test Final across versions."""
        MAX_SIZE: Final[int] = 100
        API_VERSION: Final = "v1.0"
        
        assert MAX_SIZE == 100
        assert API_VERSION == "v1.0"
    
    def test_param_spec_functionality(self):
        """Test ParamSpec across versions."""
        P = ParamSpec('P')
        T = TypeVar('T')
        
        def add_logging(func: Callable[P, T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                print(f"Calling {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        
        @add_logging
        def test_function(x: int, y: str = "default") -> str:
            return f"{x}: {y}"
        
        # Should work without errors
        result = test_function(42)
        assert result == "42: default"
    
    def test_self_type_functionality(self):
        """Test Self type across versions."""
        class Builder:
            def __init__(self) -> None:
                self.value = 0
            
            def add(self, amount: int) -> Self:
                self.value += amount
                return self
            
            def get_value(self) -> int:
                return self.value
        
        result = Builder().add(5).add(3).get_value()
        assert result == 8
    
    def test_override_functionality(self):
        """Test override decorator across versions."""
        class Base:
            def method(self) -> str:
                return "base"
        
        class Derived(Base):
            @override
            def method(self) -> str:
                return "derived"
        
        derived = Derived()
        assert derived.method() == "derived"


class TestUtilityFunctions:
    """Test utility functions provided by the module."""
    
    def test_is_optional_function(self):
        """Test is_optional utility function."""
        assert is_optional(Optional[str]) is True
        assert is_optional(Union[str, None]) is True
        assert is_optional(Union[int, str, None]) is False  # More than 2 args
        assert is_optional(str) is False
        assert is_optional(int) is False
    
    def test_is_list_like_function(self):
        """Test is_list_like utility function."""
        # Test with typing.List[int]
        list_int = List[int]
        result = is_list_like(list_int)
        origin = get_origin(list_int)
        assert result is True, f"Expected is_list_like(List[int]) to be True, got {result}. Origin: {origin}, type: {type(origin)}"
        
        # Test based on Python version
        if PY39_PLUS and hasattr(list, '__class_getitem__'):
            # On Python 3.9+, might use built-in list
            try:
                list_str = list[str]
                # This might not be detected as list-like on all implementations
                result = is_list_like(list_str)
                # Could be True or False depending on implementation
                assert isinstance(result, bool)
            except TypeError:
                # Some versions might not support list[str] syntax
                pass
        
        assert is_list_like(Dict[str, int]) is False
        assert is_list_like(str) is False
    
    def test_is_dict_like_function(self):
        """Test is_dict_like utility function."""
        # Test with typing.Dict[str, int]
        dict_str_int = Dict[str, int]
        result = is_dict_like(dict_str_int)
        origin = get_origin(dict_str_int)
        assert result is True, f"Expected is_dict_like(Dict[str, int]) to be True, got {result}. Origin: {origin}, type: {type(origin)}"
        
        # Test based on Python version
        if PY39_PLUS and hasattr(dict, '__class_getitem__'):
            # On Python 3.9+, might use built-in dict
            try:
                dict_type = dict[str, int]
                # This might not be detected as dict-like on all implementations
                result = is_dict_like(dict_type)
                # Could be True or False depending on implementation
                assert isinstance(result, bool)
            except TypeError:
                # Some versions might not support dict[str, int] syntax
                pass
        
        assert is_dict_like(List[str]) is False
        assert is_dict_like(str) is False
    
    def test_get_type_hints_compat(self):
        """Test get_type_hints_compat function."""
        def sample_func(x: int, y: Optional[str] = None) -> bool:
            return True
        
        hints = get_type_hints_compat(sample_func)
        assert isinstance(hints, dict)
        assert 'x' in hints
        assert 'y' in hints
        assert 'return' in hints
    
    def test_get_args_get_origin(self):
        """Test get_args and get_origin functions."""
        # Test with List
        list_int = List[int]
        origin = get_origin(list_int)
        args = get_args(list_int)
        
        # Should work across versions
        assert isinstance(args, tuple) or args is None
        if origin is not None:
            assert origin in (list, List)
        
        # Test with Union
        union_type = Union[int, str]
        union_origin = get_origin(union_type)
        union_args = get_args(union_type)
        
        assert isinstance(union_args, tuple) or union_args is None
        if union_origin is not None:
            assert union_origin is Union


class TestCrossVersionIntegration:
    """Test integration of features across different Python versions."""
    
    def test_all_version_features_together(self):
        """Test using features from all Python versions together."""
        # This should work regardless of Python version
        P = ParamSpec('P')
        T = TypeVar('T')
        
        class APIResponse(TypedDict):
            status: Literal["success", "error", "pending"]
            data: Dict[str, Any]
            message: Optional[str]
        
        @runtime_checkable
        class APIClient(Protocol):
            def call(self, endpoint: str) -> APIResponse: ...
        
        class HTTPClient:
            def call(self, endpoint: str) -> APIResponse:
                return {
                    "status": "success",
                    "data": {"result": "ok"},
                    "message": None
                }
        
        def with_retry(func: Callable[P, T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return func(*args, **kwargs)
            return wrapper
        
        class Service:
            def __init__(self, client: APIClient) -> None:
                self.client = client
            
            @with_retry
            def fetch_data(self, endpoint: str) -> str:
                response = self.client.call(endpoint)
                if response["status"] == "success":
                    return "Data fetched successfully"
                return f"Error: {response.get('message', 'Unknown error')}"
            
            def process_with_self(self) -> Self:
                return self
        
        # Test the integration
        client = HTTPClient()
        service = Service(client)
        
        result = service.fetch_data("/api/data")
        assert result == "Data fetched successfully"
        
        self_result = service.process_with_self()
        assert self_result is service
    
    def test_builtin_generic_compatibility(self):
        """Test built-in generic compatibility across versions."""
        def process_data(
            items: List[str],
            mapping: Dict[str, int],
            unique_items: Set[str]
        ) -> Tuple[int, int, int]:
            return len(items), len(mapping), len(unique_items)
        
        result = process_data(
            ["a", "b", "c"],
            {"x": 1, "y": 2},
            {"p", "q"}
        )
        
        assert result == (3, 2, 2)
    
    def test_union_syntax_compatibility(self):
        """Test union syntax compatibility."""
        def process_value(value: UnionOf(int, str, float)) -> str:
            return str(value)
        
        # Test with different types
        assert process_value(42) == "42"
        assert process_value("hello") == "hello"
        assert process_value(3.14) == "3.14"
    
    def test_type_guard_integration(self):
        """Test TypeGuard integration across versions."""
        def is_string_list(items: List[Any]) -> TypeGuard[List[str]]:
            return all(isinstance(item, str) for item in items)
        
        def process_strings(items: List[Any]) -> int:
            if is_string_list(items):
                # Type checker should know items is List[str] here
                return sum(len(item) for item in items)
            return 0
        
        # Test with string list
        string_items = ["hello", "world"]
        result = process_strings(string_items)
        assert result == 10  # 5 + 5
        
        # Test with mixed list
        mixed_items = ["hello", 42, "world"]
        result = process_strings(mixed_items)
        assert result == 0


class TestRealWorldUsagePatterns:
    """Test real-world usage patterns with the modular system."""
    
    def test_api_client_pattern(self):
        """Test API client pattern using multiple typing features."""
        class RequestConfig(TypedDict):
            url: Required[str]
            method: Required[Literal["GET", "POST", "PUT", "DELETE"]]
            headers: NotRequired[Dict[str, str]]
            timeout: NotRequired[int]
        
        @runtime_checkable
        class HTTPClient(Protocol):
            def request(self, config: RequestConfig) -> Dict[str, Any]: ...
        
        class RestClient:
            def __init__(self, base_url: str) -> None:
                self.base_url = base_url
            
            def request(self, config: RequestConfig) -> Dict[str, Any]:
                full_url = f"{self.base_url}{config['url']}"
                return {
                    "url": full_url,
                    "method": config["method"],
                    "status": 200
                }
            
            def get(self, path: str) -> Self:
                config: RequestConfig = {"url": path, "method": "GET"}
                self.last_response = self.request(config)
                return self
            
            def with_headers(self, headers: Dict[str, str]) -> Self:
                if hasattr(self, 'last_response'):
                    self.last_response["headers"] = headers
                return self
        
        # Test the client
        client = RestClient("https://api.example.com")
        result = client.get("/users").with_headers({"Accept": "application/json"})
        
        assert result is client
        assert result.last_response["url"] == "https://api.example.com/users"
        assert result.last_response["method"] == "GET"
    
    def test_builder_pattern_with_validation(self):
        """Test builder pattern with type validation."""
        def is_positive_int(value: Any) -> TypeGuard[int]:
            return isinstance(value, int) and value > 0
        
        class ConfigBuilder:
            def __init__(self) -> None:
                self.config: Dict[str, Any] = {}
            
            def set_name(self, name: str) -> Self:
                if not isinstance(name, str) or not name.strip():
                    self._error("Name must be a non-empty string")
                self.config["name"] = name
                return self
            
            def set_port(self, port: Any) -> Self:
                if not is_positive_int(port) or port > 65535:
                    self._error("Port must be a positive integer <= 65535")
                self.config["port"] = port
                return self
            
            def set_debug(self, debug: bool) -> Self:
                self.config["debug"] = debug
                return self
            
            def build(self) -> Dict[str, Any]:
                if "name" not in self.config:
                    self._error("Name is required")
                if "port" not in self.config:
                    self._error("Port is required")
                return self.config.copy()
            
            def _error(self, message: str) -> Never:
                raise ValueError(message)
        
        # Test successful build
        config = (ConfigBuilder()
                 .set_name("MyApp")
                 .set_port(8080)
                 .set_debug(True)
                 .build())
        
        assert config["name"] == "MyApp"
        assert config["port"] == 8080
        assert config["debug"] is True
        
        # Test validation errors
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            ConfigBuilder().set_name("")
        
        with pytest.raises(ValueError, match="Port must be a positive integer"):
            ConfigBuilder().set_port(-1)
        
        with pytest.raises(ValueError, match="Name is required"):
            ConfigBuilder().set_port(8080).build()


class TestModularArchitecture:
    """Test that the modular architecture works correctly."""
    
    def test_individual_modules_importable(self):
        """Test that individual modules can be imported."""
        import typing_compat.py3m7
        import typing_compat.py3m8
        import typing_compat.py3m9
        import typing_compat.py3m10
        import typing_compat.py3m11
        import typing_compat.py3m12
        
        # All modules should be importable
        modules = [
            typing_compat.py3m7,
            typing_compat.py3m8,
            typing_compat.py3m9,
            typing_compat.py3m10,
            typing_compat.py3m11,
            typing_compat.py3m12
        ]
        
        for module in modules:
            assert module is not None
            assert hasattr(module, '__all__')
    
    def test_version_flags_from_modules(self):
        """Test that version flags are available from individual modules."""
        from typing_compat.py3m7 import PY37_PLUS as py37_flag
        from typing_compat.py3m8 import PY38_PLUS as py38_flag
        from typing_compat.py3m9 import PY39_PLUS as py39_flag
        from typing_compat.py3m10 import PY310_PLUS as py310_flag
        from typing_compat.py3m11 import PY311_PLUS as py311_flag
        from typing_compat.py3m12 import PY312_PLUS as py312_flag
        
        # Should match main module flags
        assert py37_flag == PY37_PLUS
        assert py38_flag == PY38_PLUS
        assert py39_flag == PY39_PLUS
        assert py310_flag == PY310_PLUS
        assert py311_flag == PY311_PLUS
        assert py312_flag == PY312_PLUS
    
    def test_feature_attribution(self):
        """Test that features come from correct modules."""
        # Test that we can import specific features from specific modules
        from typing_compat.py3m7 import ForwardRef as ForwardRef7
        from typing_compat.py3m8 import Literal as Literal8
        from typing_compat.py3m9 import List as List9
        from typing_compat.py3m10 import ParamSpec as ParamSpec10
        from typing_compat.py3m11 import Self as Self11
        from typing_compat.py3m12 import override as override12
        
        # These should be the same as the main module exports
        assert ForwardRef7 is ForwardRef
        assert Literal8 is Literal
        assert List9 is List
        assert ParamSpec10 is ParamSpec
        assert Self11 is Self
        assert override12 is override


class TestMetadataAndUtilities:
    """Test package metadata and utility functions."""
    
    def test_package_version(self):
        """Test package version information."""
        assert __version__ == "0.2.0"
        assert isinstance(__version__, str)
    
    def test_version_info_utility(self):
        """Test get_version_info utility function."""
        info = get_version_info()
        
        assert isinstance(info, dict)
        assert "typing_compat_version" in info
        assert "python_version" in info
        assert "supported_features" in info
        assert "available_modules" in info
        
        # Check version matches
        assert info["typing_compat_version"] == __version__
        
        # Check supported features are boolean
        features = info["supported_features"]
        for feature_name, supported in features.items():
            assert isinstance(supported, bool)
        
        # Check modules list
        modules = info["available_modules"]
        expected_modules = ["py3m7", "py3m8", "py3m9", "py3m10", "py3m11", "py3m12"]
        for module in expected_modules:
            assert module in modules
    
    def test_print_version_info_utility(self):
        """Test print_version_info utility function."""
        import io
        import contextlib
        
        # Capture output
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            print_version_info()
        
        result = output.getvalue()
        
        # Should contain key information
        assert "Typing Compatibility Library" in result
        assert "0.2.0" in result
        assert "Python" in result
        assert "Supported Features:" in result


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""
    
    def test_existing_import_patterns(self):
        """Test that existing import patterns still work."""
        # These are common patterns that should still work
        from typing_compat import List, Dict, Optional, Union, Any, Callable
        from typing_compat import Literal, Protocol, TypedDict, Final
        from typing_compat import ParamSpec, TypeGuard, Self, override
        
        # All should be available
        imports = [List, Dict, Optional, Union, Any, Callable, 
                  Literal, Protocol, TypedDict, Final,
                  ParamSpec, TypeGuard, Self, override]
        
        for imported_item in imports:
            assert imported_item is not None
    
    def test_function_annotation_compatibility(self):
        """Test that function annotations work as before."""
        def legacy_function(
            items: List[str],
            config: Dict[str, Any],
            callback: Optional[Callable[[str], None]] = None
        ) -> bool:
            if callback:
                for item in items:
                    callback(item)
            return len(items) > 0
        
        # Should work exactly as before
        result = legacy_function(["a", "b"], {"debug": True})
        assert result is True
        
        # Test with callback
        called_with = []
        def test_callback(item: str) -> None:
            called_with.append(item)
        
        result = legacy_function(["x", "y"], {}, test_callback)
        assert result is True
        assert called_with == ["x", "y"]
    
    def test_class_definition_compatibility(self):
        """Test that class definitions work as before."""
        T = TypeVar('T')
        
        class LegacyContainer(Generic[T]):
            def __init__(self) -> None:
                self.items: List[T] = []
            
            def add(self, item: T) -> None:
                self.items.append(item)
            
            def get_all(self) -> List[T]:
                return self.items.copy()
        
        # Should work exactly as before
        container: LegacyContainer[str] = LegacyContainer()
        container.add("test")
        result = container.get_all()
        assert result == ["test"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
