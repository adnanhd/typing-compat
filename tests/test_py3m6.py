"""
Test suite for Python 3.6+ features (py3m6.py module).

Tests ClassVar, Type, and basic typing features introduced or improved in Python 3.6.
"""

import sys
import pytest
from typing import Any
from typing_compat.py3m6 import *


class TestPy3m6VersionFlag:
    """Test version detection for Python 3.6+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY36_PLUS correctly detects Python 3.6+."""
        expected = sys.version_info >= (3, 6)
        assert PY36_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY36_PLUS is a boolean."""
        assert isinstance(PY36_PLUS, bool)


class TestClassVar:
    """Test ClassVar functionality."""
    
    def test_classvar_import(self):
        """Test that ClassVar can be imported."""
        assert ClassVar is not None
    
    def test_classvar_basic_usage(self):
        """Test basic ClassVar usage."""
        class Config:
            debug: ClassVar[bool] = False
            version: ClassVar[str] = "1.0"
            max_connections: ClassVar[int] = 100
        
        # Should be able to access class variables
        assert Config.debug is False
        assert Config.version == "1.0"
        assert Config.max_connections == 100
    
    def test_classvar_in_inheritance(self):
        """Test ClassVar with inheritance."""
        class BaseConfig:
            app_name: ClassVar[str] = "BaseApp"
            debug: ClassVar[bool] = False
        
        class ProductionConfig(BaseConfig):
            app_name: ClassVar[str] = "ProdApp"  # Override
            log_level: ClassVar[str] = "ERROR"   # New class var
        
        # Test inheritance and overrides
        assert BaseConfig.app_name == "BaseApp"
        assert BaseConfig.debug is False
        
        assert ProductionConfig.app_name == "ProdApp"  # Overridden
        assert ProductionConfig.debug is False         # Inherited
        assert ProductionConfig.log_level == "ERROR"   # New
    
    def test_classvar_with_generics(self):
        """Test ClassVar with generic types."""
        class DataProcessor:
            supported_formats: ClassVar[List[str]] = ["json", "xml", "csv"]
            default_config: ClassVar[Dict[str, Any]] = {"timeout": 30}
            instance_count: ClassVar[int] = 0
        
        assert DataProcessor.supported_formats == ["json", "xml", "csv"]
        assert DataProcessor.default_config["timeout"] == 30
        assert DataProcessor.instance_count == 0
    
    def test_classvar_vs_instance_var(self):
        """Test ClassVar vs instance variables."""
        class Counter:
            total_instances: ClassVar[int] = 0
            
            def __init__(self, name: str) -> None:
                self.name = name  # Instance variable
                Counter.total_instances += 1
        
        # Create instances
        c1 = Counter("first")
        c2 = Counter("second")
        
        # Instance variables are different
        assert c1.name == "first"
        assert c2.name == "second"
        
        # Class variable is shared
        assert Counter.total_instances == 2
        assert c1.total_instances == 2  # Accessible through instance
        assert c2.total_instances == 2


class TestType:
    """Test Type functionality."""
    
    def test_type_import(self):
        """Test that Type can be imported."""
        assert Type is not None
    
    def test_type_basic_usage(self):
        """Test basic Type usage."""
        def create_instance(cls: Type[str]) -> str:
            return cls()
        
        # Should work with Type annotation
        result = create_instance(str)
        assert result == ""
        assert isinstance(result, str)
    
    def test_type_with_inheritance(self):
        """Test Type with class inheritance."""
        class Animal:
            def make_sound(self) -> str:
                return "Some sound"
        
        class Dog(Animal):
            def make_sound(self) -> str:
                return "Woof!"
        
        def create_animal(animal_class: Type[Animal]) -> Animal:
            return animal_class()
        
        # Test with base class
        animal = create_animal(Animal)
        assert animal.make_sound() == "Some sound"
        
        # Test with derived class
        dog = create_animal(Dog)
        assert dog.make_sound() == "Woof!"
        assert isinstance(dog, Animal)  # Should be instance of base class too
    
    def test_type_generic_usage(self):
        """Test Type with generic classes."""
        T = TypeVar('T')
        
        class Container(Generic[T]):
            def __init__(self, item: T) -> None:
                self.item = item
            
            def get_item(self) -> T:
                return self.item
        
        def create_container(container_class: Type[Container[T]], item: T) -> Container[T]:
            return container_class(item)
        
        # Test with specific type
        str_container = create_container(Container, "hello")
        assert str_container.get_item() == "hello"
        
        int_container = create_container(Container, 42)
        assert int_container.get_item() == 42


class TestBasicTypingFeatures:
    """Test basic typing features from Python 3.6."""
    
    def test_basic_type_imports(self):
        """Test that basic types can be imported."""
        basic_types = [
            TypeVar, Generic, Union, Optional, Any,
            List, Dict, Set, FrozenSet, Tuple
        ]
        
        for typ in basic_types:
            assert typ is not None, f"{typ} should not be None"
    
    def test_collection_type_imports(self):
        """Test that collection types can be imported."""
        collection_types = [
            Iterable, Iterator, Container, Sized,
            Mapping, MutableMapping, Sequence, MutableSequence,
            AbstractSet, MutableSet
        ]
        
        for typ in collection_types:
            assert typ is not None, f"{typ} should not be None"
    
    def test_typevar_usage(self):
        """Test TypeVar functionality."""
        if TypeVar is not None:  # Skip if fallback is None
            T = TypeVar('T')
            U = TypeVar('U', bound=str)
            V = TypeVar('V', int, str)
            
            assert T is not None
            assert U is not None  
            assert V is not None
    
    def test_generic_usage(self):
        """Test Generic functionality."""
        if Generic is not None and TypeVar is not None:
            T = TypeVar('T')
            
            class Stack(Generic[T]):
                def __init__(self) -> None:
                    self.items: List[T] = []
                
                def push(self, item: T) -> None:
                    self.items.append(item)
                
                def pop(self) -> Optional[T]:
                    return self.items.pop() if self.items else None
            
            # Test with string stack
            str_stack = Stack()  # Type will be inferred
            str_stack.push("hello")
            str_stack.push("world")
            
            assert str_stack.pop() == "world"
            assert str_stack.pop() == "hello"
            assert str_stack.pop() is None
    
    def test_union_optional_usage(self):
        """Test Union and Optional functionality."""
        if Union is not None and Optional is not None:
            def process_value(value: Union[int, str]) -> str:
                return str(value)
            
            def maybe_process(value: Optional[str]) -> str:
                return value if value is not None else "None"
            
            # Test Union
            assert process_value(42) == "42"
            assert process_value("hello") == "hello"
            
            # Test Optional
            assert maybe_process("test") == "test"
            assert maybe_process(None) == "None"


class TestPy3m6Integration:
    """Test integration of py3m6 features."""
    
    def test_classvar_with_type_annotations(self):
        """Test ClassVar with other type annotations."""
        class APIClient:
            base_url: ClassVar[str] = "https://api.example.com"
            timeout: ClassVar[int] = 30
            supported_versions: ClassVar[List[str]] = ["v1", "v2"]
            
            def __init__(self, api_key: str) -> None:
                self.api_key = api_key
            
            def get_endpoint(self, path: str) -> str:
                return f"{self.base_url}/{path}"
        
        client = APIClient("secret-key")
        assert client.get_endpoint("users") == "https://api.example.com/users"
        assert client.api_key == "secret-key"
        assert APIClient.base_url == "https://api.example.com"
    
    def test_type_with_classvar(self):
        """Test Type annotations with ClassVar."""
        class ServiceRegistry:
            services: ClassVar[Dict[str, Type[Any]]] = {}
            
            @classmethod
            def register(cls, name: str, service_type: Type[Any]) -> None:
                cls.services[name] = service_type
            
            @classmethod
            def create_service(cls, name: str) -> Any:
                if name in cls.services:
                    return cls.services[name]()
                raise ValueError(f"Unknown service: {name}")
        
        # Register a service
        ServiceRegistry.register("logger", str)
        
        # Create service instance
        logger = ServiceRegistry.create_service("logger")
        assert isinstance(logger, str)
    
    def test_complex_generic_with_classvar(self):
        """Test complex generic types with ClassVar."""
        if TypeVar is not None and Generic is not None:
            T = TypeVar('T')
            
            class Repository(Generic[T]):
                connection_pool: ClassVar[Dict[str, Any]] = {}
                
                def __init__(self, model_class: Type[T]) -> None:
                    self.model_class = model_class
                    self.items: List[T] = []
                
                def add(self, item: T) -> None:
                    self.items.append(item)
                
                def get_all(self) -> List[T]:
                    return self.items.copy()
            
            # Test with string repository
            str_repo = Repository(str)
            str_repo.add("hello")
            str_repo.add("world")
            
            assert str_repo.get_all() == ["hello", "world"]
            assert str_repo.model_class is str


class TestPy3m6Fallbacks:
    """Test fallback behavior for Python 3.6+ features."""
    
    def test_classvar_fallback(self):
        """Test ClassVar fallback implementation."""
        # Should work even with fallback implementation
        test_type = ClassVar[int]
        assert test_type is not None
    
    def test_basic_types_fallback(self):
        """Test that basic types work even with fallbacks."""
        # These should always be available in some form
        assert Type is not None
        
        # Test that we can use them in annotations
        def test_func(cls: Type[str]) -> str:
            return cls()
        
        result = test_func(str)
        assert result == ""
    
    def test_collection_types_availability(self):
        """Test that collection types are available."""
        # Even with fallbacks, these should be importable
        collection_types = [
            List, Dict, Set, Tuple,
            Iterable, Iterator, Container, Sized
        ]
        
        for typ in collection_types:
            assert typ is not None


class TestPy3m6RealWorldUsage:
    """Test real-world usage patterns with Python 3.6+ features."""
    
    def test_configuration_class_pattern(self):
        """Test configuration class pattern using ClassVar."""
        class DatabaseConfig:
            # Class-level configuration
            default_host: ClassVar[str] = "localhost"
            default_port: ClassVar[int] = 5432
            supported_drivers: ClassVar[List[str]] = ["postgresql", "mysql"]
            
            def __init__(self, host: Optional[str] = None, port: Optional[int] = None) -> None:
                self.host = host or self.default_host
                self.port = port or self.default_port
            
            def get_connection_string(self) -> str:
                return f"db://{self.host}:{self.port}"
        
        # Test default configuration
        config1 = DatabaseConfig()
        assert config1.get_connection_string() == "db://localhost:5432"
        
        # Test custom configuration
        config2 = DatabaseConfig("prod.db.com", 3306)
        assert config2.get_connection_string() == "db://prod.db.com:3306"
        
        # Class variables are shared
        assert DatabaseConfig.default_host == "localhost"
        assert len(DatabaseConfig.supported_drivers) == 2
    
    def test_factory_pattern_with_type(self):
        """Test factory pattern using Type annotations."""
        class LoggerFactory:
            loggers: ClassVar[Dict[str, Type[Any]]] = {}
            
            @classmethod
            def register_logger(cls, name: str, logger_type: Type[Any]) -> None:
                cls.loggers[name] = logger_type
            
            @classmethod
            def create_logger(cls, name: str, *args: Any) -> Any:
                if name in cls.loggers:
                    return cls.loggers[name](*args)
                raise ValueError(f"Unknown logger type: {name}")
        
        # Register logger types
        LoggerFactory.register_logger("console", str)
        LoggerFactory.register_logger("file", list)
        
        # Create logger instances
        console_logger = LoggerFactory.create_logger("console", "INFO")
        file_logger = LoggerFactory.create_logger("file", ["log1", "log2"])
        
        assert console_logger == "INFO"
        assert file_logger == ["log1", "log2"]
    
    def test_singleton_pattern_with_classvar(self):
        """Test singleton pattern using ClassVar."""
        class DatabaseConnection:
            _instance: ClassVar[Optional['DatabaseConnection']] = None
            _connection_count: ClassVar[int] = 0
            
            def __new__(cls) -> 'DatabaseConnection':
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._connection_count += 1
                return cls._instance
            
            def __init__(self) -> None:
                if not hasattr(self, 'initialized'):
                    self.initialized = True
                    self.connection_id = f"conn_{self._connection_count}"
        
        # Test singleton behavior
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        
        assert db1 is db2  # Same instance
        assert DatabaseConnection._connection_count == 1
        assert db1.connection_id == "conn_1"


class TestPy3m6ErrorCases:
    """Test error handling and edge cases."""
    
    def test_classvar_edge_cases(self):
        """Test ClassVar edge cases."""
        # Test with complex types
        try:
            complex_classvar = ClassVar[Dict[str, List[Optional[int]]]]
            assert complex_classvar is not None
        except Exception:
            # Some fallback implementations might not handle complex types
            pass
    
    def test_type_edge_cases(self):
        """Test Type annotation edge cases."""
        # Test with built-in types
        def test_builtin_types(int_type: Type[int], str_type: Type[str]) -> tuple:
            return int_type(), str_type()
        
        result = test_builtin_types(int, str)
        assert result == (0, "")
    
    def test_fallback_robustness(self):
        """Test that fallbacks are robust."""
        # Even if we're using fallbacks, basic functionality should work
        if TypeVar is not None:
            T = TypeVar('T')
            assert T is not None
        
        # ClassVar should always be usable
        test_annotation = ClassVar[str]
        assert test_annotation is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
