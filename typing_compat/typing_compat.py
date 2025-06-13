"""
Enhanced Typing Compatibility Module - Base Utilities

This module contains base typing utilities and types that don't belong 
to any specific Python version. It provides generic functionality that
works across all Python versions.

This is imported by __init__.py along with all py3mX.py modules.
"""

import sys

# Base typing imports that are generally available across Python versions
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Union,
    Optional,
    TypeVar,
    ClassVar,
    Generic,
    NoReturn,
    cast,
    overload,
    no_type_check,
    no_type_check_decorator,
)

# Async types (generally available in modern Python)
try:
    from typing import (
        Awaitable,
        Coroutine,
        AsyncGenerator,
        AsyncIterator,
        AsyncIterable,
        ContextManager,
        AsyncContextManager,
    )
except ImportError:
    # Fallbacks for very old Python versions
    Awaitable = object
    Coroutine = object
    AsyncGenerator = object
    AsyncIterator = object
    AsyncIterable = object
    ContextManager = object
    AsyncContextManager = object

# Support types with fallbacks
try:
    from typing import (
        SupportsAbs,
        SupportsBytes,
        SupportsComplex,
        SupportsFloat,
        SupportsRound,
        AnyStr,
    )
except ImportError:
    # Basic fallbacks
    class SupportsAbs:
        def __abs__(self): ...
    
    class SupportsBytes:
        def __bytes__(self) -> bytes: ...
    
    class SupportsComplex:
        def __complex__(self) -> complex: ...
    
    class SupportsFloat:
        def __float__(self) -> float: ...
    
    class SupportsRound:
        def __round__(self, ndigits: int = 0): ...
    
    AnyStr = TypeVar('AnyStr', str, bytes)

# Additional base types with fallbacks
try:
    from typing import Text, IO, TextIO, BinaryIO
except ImportError:
    Text = str
    IO = object
    TextIO = object
    BinaryIO = object

# Version information
__version__ = "0.2.0"

# Aliases for common patterns
NoneType = type(None)

# Additional utility types and functions
def create_generic_alias(origin, args):
    """Create a generic alias for older Python versions."""
    if hasattr(origin, '__class_getitem__'):
        return origin[args] if isinstance(args, tuple) else origin[args]
    return origin

def is_generic(tp):
    """Check if a type is a generic type."""
    return hasattr(tp, '__origin__') or hasattr(tp, '__args__')

def is_typing_generic(tp):
    """Check if a type is from the typing module."""
    return hasattr(tp, '__module__') and tp.__module__ == 'typing'

# Type checking utilities (work with any get_origin/get_args implementation)
def is_optional(annotation):
    """Check if a type annotation represents an optional type."""
    # Import get_origin/get_args from wherever they're available
    try:
        # Try to get from main namespace (will be available after __init__.py imports)
        from typing import get_origin, get_args
    except ImportError:
        # Fallback implementations
        def get_origin(tp):
            return getattr(tp, "__origin__", None)
        
        def get_args(tp):
            args = getattr(tp, "__args__", None)
            return args if args is not None else ()
    
    origin = get_origin(annotation)
    if origin is Union:
        args = get_args(annotation)
        return len(args) == 2 and type(None) in args
    return False

def is_list_like(annotation):
    """Check if a type annotation represents a list-like type."""
    try:
        from typing import get_origin
    except ImportError:
        def get_origin(tp):
            return getattr(tp, "__origin__", None)
    
    origin = get_origin(annotation)
    if origin is None:
        return False
    
    # Check for list-like types
    if origin is list:
        return True
    
    # Check against type name
    if hasattr(origin, '__name__') and origin.__name__ == 'list':
        return True
        
    # Check string representation
    origin_str = str(origin)
    return 'list' in origin_str.lower() or 'List' in origin_str

def is_dict_like(annotation):
    """Check if a type annotation represents a dict-like type."""
    try:
        from typing import get_origin
    except ImportError:
        def get_origin(tp):
            return getattr(tp, "__origin__", None)
    
    origin = get_origin(annotation)
    if origin is None:
        return False
    
    # Check for dict-like types
    if origin is dict:
        return True
    
    # Check against type name
    if hasattr(origin, '__name__') and origin.__name__ == 'dict':
        return True
        
    # Check string representation
    origin_str = str(origin)
    return 'dict' in origin_str.lower() or 'Dict' in origin_str

def is_generator_like(annotation):
    """Check if a type annotation represents a generator-like type."""
    try:
        from typing import get_origin
    except ImportError:
        def get_origin(tp):
            return getattr(tp, "__origin__", None)
    
    origin = get_origin(annotation)
    if origin is None:
        return False
        
    # Check string representation for Generator
    origin_str = str(origin)
    return 'generator' in origin_str.lower() or 'Generator' in origin_str

def is_pathlike(annotation):
    """Check if a type annotation represents a path-like type."""
    try:
        from typing import get_origin
    except ImportError:
        def get_origin(tp):
            return getattr(tp, "__origin__", None)
    
    origin = get_origin(annotation)
    if origin is None:
        return False
        
    # Check string representation for PathLike
    origin_str = str(origin)
    return 'pathlike' in origin_str.lower() or 'PathLike' in origin_str

# Compatibility helpers
def get_type_hints_compat(obj, globalns=None, localns=None, include_extras=False):
    """Get type hints with compatibility across Python versions."""
    try:
        from typing import get_type_hints
        # Try to use include_extras if available (Python 3.11+)
        try:
            return get_type_hints(obj, globalns, localns, include_extras=include_extras)
        except TypeError:
            # Fall back to older signature
            return get_type_hints(obj, globalns, localns)
    except ImportError:
        return {}

# Version information functions
def get_version_info():
    """Get detailed version information including Python version compatibility."""
    import sys
    
    info = {
        "typing_compat_version": __version__,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "supported_features": {},
        "available_modules": []
    }
    
    # Version flags will be available after __init__.py imports everything
    # This is safe to call from user code after import
    import typing_compat
    
    # Collect version flags from the main package
    for flag_name in ['PY35_PLUS', 'PY36_PLUS', 'PY37_PLUS', 'PY38_PLUS', 'PY39_PLUS', 'PY310_PLUS', 'PY311_PLUS', 'PY312_PLUS']:
        if hasattr(typing_compat, flag_name):
            feature_name = flag_name.lower().replace('_plus', '_plus').replace('py', 'python_').replace('m', '')
            info["supported_features"][feature_name] = getattr(typing_compat, flag_name)
    
    # List available modules
    for module_name in ['py3m5', 'py3m6', 'py3m7', 'py3m8', 'py3m9', 'py3m10', 'py3m11', 'py3m12']:
        info["available_modules"].append(module_name)
    
    return info

def print_version_info():
    """Print detailed version information."""
    info = get_version_info()
    print(f"Typing Compatibility Library v{info['typing_compat_version']}")
    print(f"Python {info['python_version']}")
    print()
    print("Supported Features:")
    for feature, supported in info['supported_features'].items():
        status = "✅" if supported else "❌"
        print(f"  {status} {feature.replace('_', '.').replace('python.', 'Python ').replace('.plus', '+')}")
    print()
    print("Available Modules:", ", ".join(info['available_modules']))

# Create convenient compatibility helpers
def get_never_type():
    """Get Never type, falling back to NoReturn for older Python versions."""
    # This will work after __init__.py imports everything
    import typing_compat
    if hasattr(typing_compat, 'Never'):
        return typing_compat.Never
    return NoReturn

def get_self_type():
    """Get Self type, falling back to TypeVar for older Python versions."""
    # This will work after __init__.py imports everything
    import typing_compat
    if hasattr(typing_compat, 'Self'):
        return typing_compat.Self
    return TypeVar('Self')

# Backward compatibility
try:
    from typing import _GenericAlias
except ImportError:
    _GenericAlias = type

# Export base utilities (these don't depend on version-specific modules)
__all__ = [
    # Version info
    "__version__",
    
    # Basic types (always available)
    "Any", "NoReturn", "Union", "Optional", "Callable", "TypeVar", "Generic", "ClassVar",
    
    # Support types
    "SupportsAbs", "SupportsBytes", "SupportsComplex", "SupportsFloat", 
    "SupportsRound", "AnyStr", "Text", "IO", "TextIO", "BinaryIO",
    
    # Async types
    "Awaitable", "Coroutine", "AsyncGenerator", "AsyncIterator", "AsyncIterable",
    "ContextManager", "AsyncContextManager",
    
    # Utilities
    "TYPE_CHECKING", "cast", "overload", "no_type_check", "no_type_check_decorator",
    
    # Compatibility helpers
    "create_generic_alias", "is_generic", "is_typing_generic", "get_type_hints_compat",
    "get_never_type", "get_self_type",
    
    # Type checking utilities
    "is_optional", "is_list_like", "is_dict_like", "is_generator_like", "is_pathlike",
    
    # Extra utilities
    "NoneType",
    
    # Version info utilities
    "get_version_info", "print_version_info",
]
