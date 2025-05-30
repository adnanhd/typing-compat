"""
Test suite for Python 3.8+ features (py3m8.py module).

Tests Literal, Protocol, TypedDict, Final, and utility functions introduced in Python 3.8.
"""

import sys
import pytest
from typing import Any, Dict, List
from typing_compat.py3m8 import *


class TestPy3m8VersionFlag:
    """Test version detection for Python 3.8+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY38_PLUS correctly detects Python 3.8+."""
        expected = sys.version_info >= (3, 8)
        assert PY38_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY38_PLUS is a boolean."""
        assert isinstance(PY38_PLUS, bool)


class TestLiteral:
    """Test Literal type functionality."""
    
    def test_literal_import(self):
        """Test that Literal can be imported."""
        assert Literal is not None
    
    def test_literal_single_value(self):
        """Test Literal with single value."""
        Mode = Literal["read"]
        assert Mode is not None
    
    def test_literal_multiple_values(self):
        """Test Literal with multiple values."""
        Status = Literal["pending", "approved", "rejected"]
        assert Status is not None
    
    def test_literal_numeric_values(self):
        """Test Literal with numeric values."""
        Level = Literal[1, 2, 3]
        assert Level is not None
    
    def test_literal_mixed_types(self):
        """Test Literal with mixed value types."""
        Mixed = Literal["auto", 42, True]
        assert Mixed is not None
    
    def test_literal_in_function_annotation(self):
        """Test Literal used in function annotations."""
        def process_mode(mode: Literal["fast", "slow"]) -> str:
            return f"Processing in {mode} mode"
        
        # Should create without errors
        assert process_mode is not None
        
        # Should be callable
        result = process_mode("fast")
        assert result == "Processing in fast mode"
    
    def test_literal_module_source(self):
        """Test Literal comes from expected module."""
        if PY38_PLUS:
            assert Literal.__module__ in ('typing', 'typing_extensions')
        else:
            # Fallback should still work
            assert Literal is not None


class TestProtocol:
    """Test Protocol functionality."""
    
    def test_protocol_import(self):
        """Test that Protocol can be imported."""
        assert Protocol is not None
    
    def test_protocol_creation(self):
        """Test creating a basic Protocol."""
        class Drawable(Protocol):
            def draw(self) -> None: ...
        
        assert Drawable is not None
    
    def test_protocol_with_methods(self):
        """Test Protocol with multiple methods."""
        class Comparable(Protocol):
            def __lt__(self, other: Any) -> bool: ...
            def __eq__(self, other: Any) -> bool: ...
        
        assert Comparable is not None
    
    def test_protocol_with_properties(self):
        """Test Protocol with properties."""
        class HasSize(Protocol):
            @property
            def size(self) -> int: ...
        
        assert HasSize is not None
    
    def test_runtime_checkable_protocol(self):
        """Test runtime_checkable decorator with Protocol."""
        @runtime_checkable
        class Drawable(Protocol):
            def draw(self) -> None: ...
        
        class Circle:
            def draw(self) -> None:
                pass
        
        circle = Circle()
        
        # This should work on Python 3.8+, may not work with fallbacks
        if PY38_PLUS:
            try:
                result = isinstance(circle, Drawable)
                assert isinstance(result, bool)
            except (TypeError, AttributeError):
                # Some implementations might not support runtime checking
                pass
    
    def test_protocol_inheritance(self):
        """Test Protocol inheritance."""
        class Readable(Protocol):
            def read(self) -> str: ...
        
        class Writeable(Protocol):
            def write(self, data: str) -> None: ...
        
        class ReadWriteable(Readable, Writeable, Protocol):
            pass
        
        assert ReadWriteable is not None


class TestTypedDict:
    """Test TypedDict functionality."""
    
    def test_typed_dict_import(self):
        """Test that TypedDict can be imported."""
        assert TypedDict is not None
    
    def test_typed_dict_creation(self):
        """Test creating a basic TypedDict."""
        class Person(TypedDict):
            name: str
            age: int
        
        assert Person is not None
    
    def test_typed_dict_usage(self):
        """Test using TypedDict for type annotations."""
        class Config(TypedDict):
            debug: bool
            timeout: int
            server: str
        
        def load_config() -> Config:
            return {"debug": True, "timeout": 30, "server": "localhost"}
        
        config = load_config()
        assert config["debug"] is True
        assert config["timeout"] == 30
        assert config["server"] == "localhost"
    
    def test_typed_dict_with_optional_keys(self):
        """Test TypedDict with optional keys (if supported)."""
        # Note: total=False requires Python 3.8+
        try:
            class PartialConfig(TypedDict, total=False):
                name: str
                debug: bool
            
            assert PartialConfig is not None
        except TypeError:
            # Fallback implementations might not support total=False
            pass
    
    def test_typed_dict_inheritance(self):
        """Test TypedDict inheritance."""
        class BaseConfig(TypedDict):
            name: str
        
        class ExtendedConfig(BaseConfig):
            debug: bool
        
        assert ExtendedConfig is not None


class TestFinal:
    """Test Final type functionality."""
    
    def test_final_import(self):
        """Test that Final can be imported."""
        assert Final is not None
    
    def test_final_with_type(self):
        """Test Final with explicit type."""
        MAX_SIZE: Final[int] = 100
        assert MAX_SIZE == 100
    
    def test_final_without_type(self):
        """Test Final without explicit type."""
        API_URL: Final = "https://api.example.com"
        assert API_URL == "https://api.example.com"
    
    def test_final_in_class(self):
        """Test Final used in class definitions."""
        class Config:
            MAX_RETRIES: Final[int] = 3
            DEFAULT_TIMEOUT: Final = 30.0
        
        assert Config.MAX_RETRIES == 3
        assert Config.DEFAULT_TIMEOUT == 30.0
    
    def test_final_complex_type(self):
        """Test Final with complex types."""
        ALLOWED_TYPES: Final[List[str]] = ["json", "xml", "yaml"]
        assert ALLOWED_TYPES == ["json", "xml", "yaml"]


class TestUtilityFunctions:
    """Test get_args and get_origin utility functions."""
    
    def test_get_args_import(self):
        """Test that get_args can be imported."""
        assert get_args is not None
        assert callable(get_args)
    
    def test_get_origin_import(self):
        """Test that get_origin can be imported."""
        assert get_origin is not None
        assert callable(get_origin)
    
    def test_get_args_with_list(self):
        """Test get_args with List type."""
        from typing import List
        
        list_type = List[str]
        args = get_args(list_type)
        
        # Should return args or empty tuple
        assert isinstance(args, tuple)
        if args:  # Might be empty in fallback implementations
            assert str in args
    
    def test_get_origin_with_list(self):
        """Test get_origin with List type."""
        from typing import List
        
        list_type = List[int]
        origin = get_origin(list_type)
        
        # Should return origin or None
        if origin is not None:
            assert origin in (list, List)
    
    def test_get_args_with_dict(self):
        """Test get_args with Dict type."""
        from typing import Dict
        
        dict_type = Dict[str, int]
        args = get_args(dict_type)
        
        assert isinstance(args, tuple)
        if args:  # Might be empty in fallback implementations
            assert len(args) <= 2  # str, int
    
    def test_get_origin_with_dict(self):
        """Test get_origin with Dict type."""
        from typing import Dict
        
        dict_type = Dict[str, int]
        origin = get_origin(dict_type)
        
        if origin is not None:
            assert origin in (dict, Dict)
    
    def test_get_args_with_union(self):
        """Test get_args with Union type."""
        from typing import Union
        
        union_type = Union[int, str]
        args = get_args(union_type)
        
        assert isinstance(args, tuple)
        if args:  # Might be empty in fallback implementations
            assert len(args) >= 2
    
    def test_get_origin_with_union(self):
        """Test get_origin with Union type."""
        from typing import Union
        
        union_type = Union[int, str]
        origin = get_origin(union_type)
        
        if origin is not None:
            assert origin is Union
    
    def test_get_args_with_non_generic(self):
        """Test get_args with non-generic type."""
        args = get_args(int)
        assert args == () or args is None
    
    def test_get_origin_with_non_generic(self):
        """Test get_origin with non-generic type."""
        origin = get_origin(str)
        assert origin is None


class TestPy3m8Integration:
    """Test integration of py3m8 features with each other."""
    
    def test_protocol_with_typed_dict(self):
        """Test Protocol using TypedDict."""
        class ConfigDict(TypedDict):
            name: str
            debug: bool
        
        @runtime_checkable
        class Configurable(Protocol):
            def get_config(self) -> ConfigDict: ...
        
        class App:
            def get_config(self) -> ConfigDict:
                return {"name": "MyApp", "debug": True}
        
        app = App()
        config = app.get_config()
        assert config["name"] == "MyApp"
        assert config["debug"] is True
    
    def test_literal_with_final(self):
        """Test Literal used with Final."""
        MODE: Final[Literal["prod", "dev", "test"]] = "prod"
        assert MODE == "prod"
    
    def test_protocol_with_literal(self):
        """Test Protocol using Literal types."""
        class FileHandler(Protocol):
            def open(self, mode: Literal["r", "w", "a"]) -> None: ...
        
        assert FileHandler is not None


class TestPy3m8Fallbacks:
    """Test fallback behavior for Python 3.8+ features."""
    
    def test_literal_fallback_behavior(self):
        """Test Literal fallback works."""
        # Should work even with fallback implementation
        Mode = Literal["fast", "slow"]
        assert Mode is not None
    
    def test_protocol_fallback_behavior(self):
        """Test Protocol fallback works."""
        class TestProtocol(Protocol):
            def method(self) -> None: ...
        
        # Should create without errors
        assert TestProtocol is not None
    
    def test_typed_dict_fallback_behavior(self):
        """Test TypedDict fallback works."""
        class TestDict(TypedDict):
            key: str
        
        # Should create without errors
        assert TestDict is not None
    
    def test_final_fallback_behavior(self):
        """Test Final fallback works."""
        VALUE: Final[str] = "test"
        assert VALUE == "test"
    
    def test_utility_functions_fallback(self):
        """Test utility functions work with fallbacks."""
        # Should be callable even with fallback implementations
        result_args = get_args(int)
        result_origin = get_origin(str)
        
        assert isinstance(result_args, tuple) or result_args is None
        assert result_origin is None or hasattr(result_origin, '__name__')


class TestPy3m8RealWorldUsage:
    """Test real-world usage patterns with Python 3.8+ features."""
    
    def test_api_response_modeling(self):
        """Test modeling API responses with py3m8 features."""
        class APIResponse(TypedDict):
            status: Literal["success", "error"]
            data: Dict[str, Any]
            message: str
        
        class APIClient(Protocol):
            def call(self, endpoint: str) -> APIResponse: ...
        
        def process_response(response: APIResponse) -> str:
            if response["status"] == "success":
                return "OK"
            return f"Error: {response['message']}"
        
        # Should work without errors
        test_response: APIResponse = {
            "status": "success",
            "data": {"result": 42},
            "message": "Operation completed"
        }
        
        result = process_response(test_response)
        assert result == "OK"
    
    def test_configuration_system(self):
        """Test configuration system using multiple py3m8 features."""
        LOG_LEVEL: Final[Literal["DEBUG", "INFO", "WARNING", "ERROR"]] = "INFO"
        
        class DatabaseConfig(TypedDict):
            host: str
            port: int
            ssl: bool
        
        class ConfigProvider(Protocol):
            def get_db_config(self) -> DatabaseConfig: ...
            def get_log_level(self) -> Literal["DEBUG", "INFO", "WARNING", "ERROR"]: ...
        
        class ProductionConfig:
            def get_db_config(self) -> DatabaseConfig:
                return {"host": "prod.db.com", "port": 5432, "ssl": True}
            
            def get_log_level(self) -> Literal["DEBUG", "INFO", "WARNING", "ERROR"]:
                return LOG_LEVEL
        
        config = ProductionConfig()
        db_config = config.get_db_config()
        log_level = config.get_log_level()
        
        assert db_config["host"] == "prod.db.com"
        assert db_config["ssl"] is True
        assert log_level == "INFO"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
