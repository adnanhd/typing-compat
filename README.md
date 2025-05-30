# Enhanced Typing Compatibility Library - Modular Edition

A comprehensive typing compatibility library that provides a unified interface for all typing-related imports across different Python versions (3.7+). Now with a **modular architecture** for better maintainability and organization.

## 🏗️ Modular Architecture

The library is now organized into separate modules for each Python version's features:

```
typing_compat/
├── __init__.py          # Main package interface
├── typing_compat.py     # Unified imports from all modules
├── py3m7.py            # Python 3.7+ features (ForwardRef, etc.)
├── py3m8.py            # Python 3.8+ features (Literal, Protocol, TypedDict, etc.)
├── py3m9.py            # Python 3.9+ features (Built-in generics: list[int], etc.)
├── py3m10.py           # Python 3.10+ features (ParamSpec, TypeGuard, | unions, etc.)
├── py3m11.py           # Python 3.11+ features (Self, Never, Required, etc.)
├── py3m12.py           # Python 3.12+ features (Buffer, override, TypeIs, etc.)
└── _version.py         # Version information
```

## 🚀 Key Features

- **Modular Design**: Each Python version's features in separate, focused modules
- **Single Import Source**: Import all typing needs from one place  
- **Automatic Version Detection**: No need to worry about Python version differences
- **Comprehensive Coverage**: Support for Python 3.7+ through 3.12+
- **Intelligent Fallbacks**: Graceful degradation when features aren't available
- **Utility Functions**: Additional helpers for type checking and analysis
- **Zero Configuration**: Works out of the box with sensible defaults

## 📦 Installation

```bash
pip install typing-compat
```

## 🎯 Quick Start

Instead of dealing with version-specific imports:

```python
# ❌ Old way - version-specific imports
import sys
if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict
else:
    from typing_extensions import Literal, Protocol, TypedDict

if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeGuard
else:
    from typing_extensions import ParamSpec, TypeGuard
```

Simply use our modular library:

```python
# ✅ New way - unified imports
from typing_compat import *
# Everything just works across all Python versions! 🎉
```

## 📖 Module-Specific Features

### Python 3.7+ Features (`py3m7.py`)
```python
from typing_compat import ForwardRef, OrderedDict, Counter, ChainMap, Deque, DefaultDict

# ForwardRef works across all versions
UserRef = ForwardRef('User')
```

### Python 3.8+ Features (`py3m8.py`)
```python
from typing_compat import Literal, Protocol, TypedDict, Final, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

class Config(TypedDict):
    mode: Literal["prod", "dev", "test"]
    debug: bool

API_URL: Final[str] = "https://api.example.com"
```

### Python 3.9+ Features (`py3m9.py`)
```python
from typing_compat import List, Dict, Set, Tuple, Type

# Uses built-in types on Python 3.9+, typing module types on older versions
def process_data(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Works with both list[str] (3.9+) and List[str] (older versions)
numbers: List[int] = [1, 2, 3]
```

### Python 3.10+ Features (`py3m10.py`)
```python
from typing_compat import ParamSpec, TypeGuard, Concatenate, TypeAlias, UnionOf

# ParamSpec for preserving function signatures
P = ParamSpec('P')
T = TypeVar('T')

def with_logging(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Type aliases
UserId: TypeAlias = int
UserName: TypeAlias = str

# Union creation helper
StringOrInt = UnionOf(str, int)  # Uses | on 3.10+, Union on older versions
```

### Python 3.11+ Features (`py3m11.py`)
```python
from typing_compat import Self, Never, Required, NotRequired, LiteralString

class Builder:
    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}
    
    def add_field(self, key: str, value: Any) -> Self:  # Returns same type
        self.data[key] = value
        return self
    
    def build(self) -> Dict[str, Any]:
        return self.data

class UserDict(TypedDict):
    name: Required[str]        # Must be present
    email: Required[str]       # Must be present  
    phone: NotRequired[str]    # Optional
```

### Python 3.12+ Features (`py3m12.py`)
```python
from typing_compat import override, TypeIs, Buffer

class Animal:
    def make_sound(self) -> str:
        return "Some sound"

class Dog(Animal):
    @override  # Ensures we're actually overriding a parent method
    def make_sound(self) -> str:
        return "Woof!"

def is_string(value: Any) -> TypeIs[str]:
    """Type guard using TypeIs for more precise type narrowing."""
    return isinstance(value, str)
```

## 🛠️ Cross-Version Compatibility Examples

The beauty of the modular design is that you can use features from any Python version, and the library handles compatibility automatically:

```python
from typing_compat import *

# This works on ALL Python versions (3.7+)
class ModernAPI:
    """API class using features from multiple Python versions."""
    
    # 3.8+ features with fallbacks
    config: TypedDict('Config', {
        'mode': Literal['fast', 'slow'],
        'debug': bool
    })
    
    # 3.9+ built-in generics with fallbacks
    def __init__(self) -> None:
        self.data: List[Dict[str, Any]] = []
        self.cache: Dict[str, Optional[str]] = {}
    
    # 3.11+ Self type with fallbacks
    def add_data(self, item: Dict[str, Any]) -> Self:
        self.data.append(item)
        return self
    
    # 3.10+ ParamSpec with fallbacks
    def with_callback(self, callback: Callable[P, T]) -> Callable[P, T]:
        return callback
    
    # 3.12+ override with fallbacks
    @override
    def __str__(self) -> str:
        return f"ModernAPI({len(self.data)} items)"

# Works perfectly on Python 3.7, 3.8, 3.9, 3.10, 3.11, and 3.12!
api = ModernAPI().add_data({"key": "value"})
```

## 🔍 Version Detection and Utilities

```python
from typing_compat import (
    PY37_PLUS, PY38_PLUS, PY39_PLUS, PY310_PLUS, PY311_PLUS, PY312_PLUS,
    get_version_info, print_version_info
)

# Check what features are available
if PY311_PLUS:
    print("Using latest Self and Never types!")
elif PY310_PLUS:
    print("Using ParamSpec and TypeGuard!")
elif PY39_PLUS:
    print("Using built-in generic types!")

# Get detailed version information
info = get_version_info()
print(f"Library version: {info['typing_compat_version']}")
print(f"Python version: {info['python_version']}")
print(f"Available features: {info['supported_features']}")

# Print comprehensive version info
print_version_info()
# Output:
# Typing Compatibility Library v0.2.0
# Python 3.10.2
# 
# Supported Features:
#   ✅ Python 3.7+
#   ✅ Python 3.8+
#   ✅ Python 3.9+
#   ✅ Python 3.10+
#   ❌ Python 3.11+
#   ❌ Python 3.12+
#
# Available Modules: py3m7, py3m8, py3m9, py3m10, py3m11, py3m12
```

## 🧪 Advanced Usage Examples

### Protocol with Modern Features
```python
from typing_compat import Protocol, runtime_checkable, List, Dict, Self

@runtime_checkable
class DataProcessor(Protocol):
    """Protocol for data processing classes."""
    
    def process(self, data: List[Dict[str, Any]]) -> Self: ...
    def get_results(self) -> Dict[str, Any]: ...

class CSVProcessor:
    def __init__(self):
        self.results = {}
    
    def process(self, data: List[Dict[str, Any]]) -> Self:
        # Process CSV data
        self.results = {"processed": len(data)}
        return self
    
    def get_results(self) -> Dict[str, Any]:
        return self.results

# Works with protocol checking
processor = CSVProcessor()
assert isinstance(processor, DataProcessor)  # True on Python 3.8+
```

### Generic Class with All Features
```python
from typing_compat import *

T = TypeVar('T')
U = TypeVar('U')

class Container(Generic[T]):
    """Container class showcasing multiple typing features."""
    
    def __init__(self) -> None:
        self.items: List[T] = []
        self.metadata: Dict[str, Any] = {}
    
    def add(self, item: T) -> Self:
        """Add an item and return self for chaining."""
        self.items.append(item)
        return self
    
    def transform(self, func: Callable[[T], U]) -> 'Container[U]':
        """Transform items using a function."""
        new_container: Container[U] = Container()
        new_container.items = [func(item) for item in self.items]
        return new_container
    
    def filter_items(self, predicate: Callable[[T], TypeGuard[T]]) -> Self:
        """Filter items using a type guard."""
        self.items = [item for item in self.items if predicate(item)]
        return self
    
    @override
    def __len__(self) -> int:
        return len(self.items)

# Usage works across all Python versions
container: Container[str] = Container()
result = (container
          .add("hello")
          .add("world")
          .transform(str.upper)  # Container[str] -> Container[str]
          .filter_items(lambda x: len(x) > 3))

print(len(result))  # Works with override decorator
```

## 📋 Comprehensive Feature Matrix

| Feature | Module | Python Version | Support | Example |
|---------|--------|----------------|---------|---------|
| **Basic Types** | Core | 3.7+ | ✅ Native | `Any, Union, Optional, Callable` |
| **ForwardRef** | py3m7 | 3.7+ | ✅ Native/Fallback | `ForwardRef('User')` |
| **Literal** | py3m8 | 3.8+ | ✅ Native/Fallback | `Literal["read", "write"]` |
| **Protocol** | py3m8 | 3.8+ | ✅ Native/Fallback | `class Drawable(Protocol): ...` |
| **TypedDict** | py3m8 | 3.8+ | ✅ Native/Fallback | `class User(TypedDict): ...` |
| **Final** | py3m8 | 3.8+ | ✅ Native/Fallback | `MAX_SIZE: Final[int] = 100` |
| **Built-in Generics** | py3m9 | 3.9+ | ✅ Native/Fallback | `list[int]` vs `List[int]` |
| **ParamSpec** | py3m10 | 3.10+ | ✅ Native/Fallback | `P = ParamSpec('P')` |
| **TypeGuard** | py3m10 | 3.10+ | ✅ Native/Fallback | `def is_str(x) -> TypeGuard[str]` |
| **Union Operator** | py3m10 | 3.10+ | ✅ Native/Fallback | `int \| str` via `UnionOf(int, str)` |
| **Self** | py3m11 | 3.11+ | ✅ Native/Fallback | `def method(self) -> Self` |
| **Never** | py3m11 | 3.11+ | ✅ Native/Fallback | `def raise_error() -> Never` |
| **Required/NotRequired** | py3m11 | 3.11+ | ✅ Native/Fallback | `name: Required[str]` |
| **override** | py3m12 | 3.12+ | ✅ Native/Fallback | `@override def method(self)` |
| **TypeIs** | py3m12 | 3.12+ | ✅ Native/Fallback | `def check(x) -> TypeIs[str]` |

## 🧪 Testing

Run the comprehensive test suite that covers all modules:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Test specific modules
pytest tests/test_modular.py::TestPy3m8Module -v
pytest tests/test_modular.py::TestPy3m10Module -v

# Run tests with coverage
pytest tests/ --cov=typing_compat --cov-report=html

# Type checking
mypy typing_compat/
pyright typing_compat/
```

### Running Module-Specific Tests

```bash
# Test individual version modules
python -c "from typing_compat.py3m8 import *; print('Python 3.8+ module works!')"
python -c "from typing_compat.py3m10 import *; print('Python 3.10+ module works!')"
python -c "from typing_compat.py3m11 import *; print('Python 3.11+ module works!')"
```

## 🔧 Development

### Module Development Guidelines

When adding new features:

1. **Identify the Python version** where the feature was introduced
2. **Add to the appropriate module** (`py3m*.py`)  
3. **Provide fallback implementations** for older versions
4. **Update the main module** (`typing_compat.py`) to import the feature
5. **Add comprehensive tests** in the test suite
6. **Update documentation** with usage examples

### Example: Adding a New Feature

```python
# In py3m13.py (hypothetical future version)
import sys

PY313_PLUS = sys.version_info >= (3, 13)

if PY313_PLUS:
    from typing import NewFeature
else:
    # Fallback implementation
    def NewFeature(tp):
        return tp

__all__ = ["NewFeature", "PY313_PLUS"]
```

## 🤝 Contributing

We welcome contributions! The modular structure makes it easy to add new features:

1. Fork the repository
2. Identify which version module needs updates
3. Add your feature with appropriate fallbacks
4. Add tests for the new functionality
5. Update documentation
6. Submit a pull request

### Module-Specific Contributions

- **py3m7.py**: Python 3.7+ features
- **py3m8.py**: Python 3.8+ features (Literal, Protocol, TypedDict, Final)
- **py3m9.py**: Python 3.9+ features (built-in generics)
- **py3m10.py**: Python 3.10+ features (ParamSpec, TypeGuard, union operator)
- **py3m11.py**: Python 3.11+ features (Self, Never, Required/NotRequired)
- **py3m12.py**: Python 3.12+ features (override, TypeIs, Buffer)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the Python typing team for the excellent typing system
- Thanks to the typing_extensions maintainers for backport compatibility
- Inspired by the need for seamless typing across Python versions
- Special thanks to the community for driving the modular architecture

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/adnanhad/typing-compat/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/adnanhad/typing-compat/discussions)  
- 📖 **Documentation**: [README](https://github.com/adnanhad/typing-compat#readme)
- 💬 **Community**: [GitHub Discussions](https://github.com/adnanhad/typing-compat/discussions)

---

**Happy typing with modules!** 🎉 Made with ❤️ for the Python community.

*The modular architecture makes maintaining and extending typing compatibility easier than ever!*
