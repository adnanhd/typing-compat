"""
Test suite for Python 3.11+ features (py3m11.py module).

Tests Self, Never, Required, NotRequired, and other features introduced in Python 3.11.
"""

import sys
import pytest
from typing import TypeVar, Generic, Dict, Any
from typing_compat.py3m11 import *


class TestPy3m11VersionFlag:
    """Test version detection for Python 3.11+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY311_PLUS correctly detects Python 3.11+."""
        expected = sys.version_info >= (3, 11)
        assert PY311_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY311_PLUS is a boolean."""
        assert isinstance(PY311_PLUS, bool)


class TestSelf:
    """Test Self type functionality."""
    
    def test_self_import(self):
        """Test that Self can be imported."""
        assert Self is not None
    
    def test_self_in_method_return(self):
        """Test Self used in method return annotations."""
        class Builder:
            def __init__(self) -> None:
                self.value = 0
            
            def add(self, amount: int) -> Self:
                self.value += amount
                return self
            
            def multiply(self, factor: int) -> Self:
                self.value *= factor
                return self
            
            def get_value(self) -> int:
                return self.value
        
        # Test method chaining
        builder = Builder()
        result = builder.add(5).multiply(2).add(3)
        
        # Should return the same instance
        assert result is builder
        assert result.get_value() == 13  # (0 + 5) * 2 + 3
    
    def test_self_in_class_hierarchy(self):
        """Test Self type with inheritance."""
        class Base:
            def __init__(self, value: int) -> None:
                self.value = value
            
            def copy(self) -> Self:
                return type(self)(self.value)
            
            def reset(self) -> Self:
                self.value = 0
                return self
        
        class Derived(Base):
            def __init__(self, value: int, extra: str = "default") -> None:
                super().__init__(value)
                self.extra = extra
            
            def set_extra(self, extra: str) -> Self:
                self.extra = extra
                return self
        
        # Test with base class
        base = Base(10)
        base_copy = base.copy()
        assert isinstance(base_copy, Base)
        assert base_copy.value == 10
        assert base_copy is not base
        
        # Test with derived class
        derived = Derived(20, "test")
        derived_copy = derived.copy()
        assert isinstance(derived_copy, Derived)
        assert derived_copy.value == 20
        
        # Test method chaining on derived
        result = derived.reset().set_extra("new")
        assert result is derived
        assert result.value == 0
        assert result.extra == "new"
    
    def test_self_with_generics(self):
        """Test Self type with generic classes."""
        T = TypeVar('T')
        
        class Container(Generic[T]):
            def __init__(self) -> None:
                self.items: list[T] = []
            
            def add(self, item: T) -> Self:
                self.items.append(item)
                return self
            
            def clear(self) -> Self:
                self.items.clear()
                return self
            
            def get_items(self) -> list[T]:
                return self.items.copy()
        
        # Test with string container
        str_container = Container[str]()
        result = str_container.add("hello").add("world")
        
        assert result is str_container
        assert result.get_items() == ["hello", "world"]
        
        # Test clear and add
        result.clear().add("new")
        assert result.get_items() == ["new"]


class TestNever:
    """Test Never type functionality."""
    
    def test_never_import(self):
        """Test that Never can be imported."""
        assert Never is not None
    
    def test_never_in_function_annotation(self):
        """Test Never used in function annotations."""
        def always_raises() -> Never:
            raise ValueError("This function always raises")
        
        # Function should be defined
        assert always_raises is not None
        
        # Should raise when called
        with pytest.raises(ValueError):
            always_raises()
    
    def test_never_with_conditionals(self):
        """Test Never in conditional return scenarios."""
        def process_value(value: int) -> str:
            if value < 0:
                raise_error()  # This returns Never
            return f"Value: {value}"
        
        def raise_error() -> Never:
            raise RuntimeError("Negative values not allowed")
        
        # Test normal case
        result = process_value(42)
        assert result == "Value: 42"
        
        # Test error case
        with pytest.raises(RuntimeError):
            process_value(-1)
    
    def test_never_in_type_unions(self):
        """Test Never used in type unions."""
        from typing import Union
        
        def handle_result() -> Union[str, Never]:
            # This is mainly for type checker demonstration
            return "success"
        
        result = handle_result()
        assert result == "success"


class TestRequiredNotRequired:
    """Test Required and NotRequired functionality."""
    
    def test_required_not_required_import(self):
        """Test that Required and NotRequired can be imported."""
        assert Required is not None
        assert NotRequired is not None
    
    def test_required_in_typed_dict(self):
        """Test Required used in TypedDict."""
        from typing_extensions import TypedDict
        
        class UserProfile(TypedDict):
            name: Required[str]
            email: Required[str]
            age: NotRequired[int]
            bio: NotRequired[str]
        
        # Test with required fields only
        minimal_user: UserProfile = {
            "name": "Alice",
            "email": "alice@example.com"
        }
        
        assert minimal_user["name"] == "Alice"
        assert minimal_user["email"] == "alice@example.com"
        
        # Test with all fields
        complete_user: UserProfile = {
            "name": "Bob",
            "email": "bob@example.com", 
            "age": 30,
            "bio": "Software developer"
        }
        
        assert complete_user["age"] == 30
        assert complete_user["bio"] == "Software developer"
    
    def test_required_not_required_nested(self):
        """Test Required/NotRequired with nested structures."""
        from typing_extensions import TypedDict
        from typing import List
        
        class Address(TypedDict):
            street: Required[str]
            city: Required[str]
            country: Required[str]
            zip_code: NotRequired[str]
        
        class Person(TypedDict):
            name: Required[str]
            addresses: Required[List[Address]]
            phone: NotRequired[str]
        
        person: Person = {
            "name": "Charlie",
            "addresses": [
                {
                    "street": "123 Main St",
                    "city": "Anytown", 
                    "country": "USA"
                }
            ]
        }
        
        assert person["name"] == "Charlie"
        assert len(person["addresses"]) == 1
        assert person["addresses"][0]["street"] == "123 Main St"
    
    def test_required_not_required_function_parameters(self):
        """Test Required/NotRequired in function parameters."""
        from typing_extensions import TypedDict
        
        class ConfigDict(TypedDict):
            host: Required[str]
            port: Required[int]
            ssl: NotRequired[bool]
            timeout: NotRequired[int]
        
        def connect_to_server(config: ConfigDict) -> str:
            host = config["host"]
            port = config["port"]
            ssl = config.get("ssl", False)
            timeout = config.get("timeout", 30)
            
            protocol = "https" if ssl else "http"
            return f"{protocol}://{host}:{port} (timeout: {timeout}s)"
        
        # Test minimal config
        minimal_config: ConfigDict = {
            "host": "example.com",
            "port": 8080
        }
        
        result = connect_to_server(minimal_config)
        assert result == "http://example.com:8080 (timeout: 30s)"
        
        # Test full config
        full_config: ConfigDict = {
            "host": "secure.example.com",
            "port": 443,
            "ssl": True,
            "timeout": 60
        }
        
        result = connect_to_server(full_config)
        assert result == "https://secure.example.com:443 (timeout: 60s)"


class TestLiteralString:
    """Test LiteralString functionality."""
    
    def test_literal_string_import(self):
        """Test that LiteralString can be imported."""
        assert LiteralString is not None
    
    def test_literal_string_in_function(self):
        """Test LiteralString used in function annotations."""
        def process_literal_string(value: LiteralString) -> str:
            return f"Literal string: {value}"
        
        # Should work with string literals
        result = process_literal_string("hello")
        assert result == "Literal string: hello"
    
    def test_literal_string_vs_regular_string(self):
        """Test LiteralString vs regular str type."""
        def format_sql_query(table: LiteralString, condition: str) -> str:
            return f"SELECT * FROM {table} WHERE {condition}"
        
        # This demonstrates the intended usage
        query = format_sql_query("users", "age > 18")
        assert query == "SELECT * FROM users WHERE age > 18"


class TestTypeVarTuple:
    """Test TypeVarTuple functionality."""
    
    def test_type_var_tuple_import(self):
        """Test that TypeVarTuple can be imported."""
        assert TypeVarTuple is not None
    
    def test_type_var_tuple_creation(self):
        """Test creating TypeVarTuple instances."""
        Ts = TypeVarTuple('Ts')
        assert Ts is not None
        
        if hasattr(Ts, 'name'):
            assert Ts.name == 'Ts'
    
    def test_type_var_tuple_in_generic(self):
        """Test TypeVarTuple used in generic contexts."""
        # This is mainly for type checker demonstration
        Ts = TypeVarTuple('Ts')
        
        # Simple example that should work
        def process_tuple(items: tuple) -> int:
            return len(items)
        
        result = process_tuple((1, 2, 3))
        assert result == 3


class TestUnpack:
    """Test Unpack functionality."""
    
    def test_unpack_import(self):
        """Test that Unpack can be imported."""
        assert Unpack is not None
    
    def test_unpack_basic_usage(self):
        """Test basic Unpack usage."""
        # Unpack is typically used with TypeVarTuple
        # This is a simplified test for the import
        result = Unpack(tuple[int, str, bool])
        assert result is not None
    
    def test_unpack_in_function(self):
        """Test Unpack used in function context."""
        def process_unpacked(*args) -> int:
            return len(args)
        
        result = process_unpacked(1, "hello", True, 3.14)
        assert result == 4


class TestPy3m11Integration:
    """Test integration of py3m11 features."""
    
    def test_self_with_required_not_required(self):
        """Test Self type with Required/NotRequired TypedDict."""
        from typing_extensions import TypedDict
        
        class ConfigDict(TypedDict):
            name: Required[str]
            debug: NotRequired[bool]
        
        class Configurable:
            def __init__(self, config: ConfigDict) -> None:
                self.config = config
            
            def update_config(self, **updates: Any) -> Self:
                self.config = {**self.config, **updates}
                return self
            
            def get_name(self) -> str:
                return self.config["name"]
            
            def is_debug(self) -> bool:
                return self.config.get("debug", False)
        
        # Test configuration
        initial_config: ConfigDict = {"name": "MyApp"}
        app = Configurable(initial_config)
        
        # Test method chaining with Self
        result = app.update_config(debug=True)
        assert result is app
        assert result.get_name() == "MyApp"
        assert result.is_debug() is True
    
    def test_complex_builder_pattern(self):
        """Test complex builder pattern using multiple py3m11 features."""
        from typing_extensions import TypedDict
        
        class QueryConfig(TypedDict):
            table: Required[str]
            limit: NotRequired[int]
            where_clause: NotRequired[str]
        
        class QueryBuilder:
            def __init__(self) -> None:
                self.config: QueryConfig = {"table": ""}
            
            def table(self, name: LiteralString) -> Self:
                self.config["table"] = name
                return self
            
            def limit(self, count: int) -> Self:
                self.config["limit"] = count
                return self
            
            def where(self, clause: str) -> Self:
                self.config["where_clause"] = clause
                return self
            
            def build(self) -> str:
                if not self.config["table"]:
                    return self._error("Table name is required")
                
                query = f"SELECT * FROM {self.config['table']}"
                
                if "where_clause" in self.config:
                    query += f" WHERE {self.config['where_clause']}"
                
                if "limit" in self.config:
                    query += f" LIMIT {self.config['limit']}"
                
                return query
            
            def _error(self, message: str) -> Never:
                raise ValueError(message)
        
        # Test successful query building
        query = (QueryBuilder()
                .table("users")
                .where("age > 18")
                .limit(10)
                .build())
        
        assert query == "SELECT * FROM users WHERE age > 18 LIMIT 10"
        
        # Test error case
        with pytest.raises(ValueError):
            QueryBuilder().build()


class TestPy3m11Fallbacks:
    """Test fallback behavior for Python 3.11+ features."""
    
    def test_self_fallback(self):
        """Test Self fallback implementation."""
        class TestClass:
            def method(self) -> Self:
                return self
        
        instance = TestClass()
        result = instance.method()
        assert result is instance
    
    def test_never_fallback(self):
        """Test Never fallback implementation."""
        def error_function() -> Never:
            raise RuntimeError("Always fails")
        
        with pytest.raises(RuntimeError):
            error_function()
    
    def test_required_not_required_fallback(self):
        """Test Required/NotRequired fallback behavior."""
        # Should work as pass-through in fallback
        required_str = Required[str]
        not_required_int = NotRequired[int]
        
        assert required_str is not None
        assert not_required_int is not None
    
    def test_literal_string_fallback(self):
        """Test LiteralString fallback behavior."""
        def test_func(value: LiteralString) -> str:
            return str(value)
        
        result = test_func("test")
        assert result == "test"


class TestPy3m11ErrorCases:
    """Test error handling and edge cases."""
    
    def test_self_type_usage_errors(self):
        """Test potential Self type usage errors."""
        # Self should work in method contexts
        class ValidClass:
            def valid_method(self) -> Self:
                return self
        
        # Test that it works
        instance = ValidClass()
        result = instance.valid_method()
        assert result is instance
    
    def test_never_type_behavior(self):
        """Test Never type edge cases."""
        def conditional_never(should_raise: bool) -> str:
            if should_raise:
                return error_func()  # Returns Never
            return "success"
        
        def error_func() -> Never:
            raise Exception("Error occurred")
        
        # Test non-error case
        result = conditional_never(False)
        assert result == "success"
        
        # Test error case
        with pytest.raises(Exception):
            conditional_never(True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
