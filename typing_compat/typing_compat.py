"""
Enhanced Typing Compatibility Module

This module provides a unified interface for all typing-related imports,
automatically handling Python version differences by importing from
version-specific modules.

Usage:
    from typing_compat import *
    # or
    from typing_compat import List, Dict, Optional, Literal, Protocol, etc.
"""

import sys
from types import new_class

# Always available from typing
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
    Awaitable,
    Coroutine,
    AsyncGenerator,
    AsyncIterator,
    AsyncIterable,
    ContextManager,
    AsyncContextManager,
    SupportsAbs,
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsIndex,
    SupportsInt,
    SupportsRound,
    ByteString,
    AnyStr,
    Text,
    Pattern,
    Match,
    IO,
    TextIO,
    BinaryIO,
    cast,
    overload,
    no_type_check,
    no_type_check_decorator,
)

# Import from version-specific modules
from .py3m7 import *
from .py3m8 import *
from .py3m9 import *
from .py3m10 import *
from .py3m11 import *
from .py3m12 import *

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

# Compatibility helpers
def get_type_hints_compat(obj, globalns=None, localns=None, include_extras=False):
    """Get type hints with compatibility across Python versions."""
    try:
        from typing import get_type_hints
        if PY311_PLUS:
            return get_type_hints(obj, globalns, localns, include_extras=include_extras)
        else:
            return get_type_hints(obj, globalns, localns)
    except ImportError:
        return {}

# Version info - collected from all modules
__version__ = "0.2.0"

# Aliases for common patterns
NoneType = type(None)

# Backward compatibility
try:
    from typing import _GenericAlias
except ImportError:
    _GenericAlias = type(List[int])

# Extra utilities for convenience
def is_optional(annotation):
    """Check if a type annotation represents an optional type."""
    origin = get_origin(annotation)
    if origin is Union:
        args = get_args(annotation)
        return len(args) == 2 and type(None) in args
    return False

def is_list_like(annotation):
    """Check if a type annotation represents a list-like type."""
    origin = get_origin(annotation)
    return origin in (list, List) if PY39_PLUS else origin is List

def is_dict_like(annotation):
    """Check if a type annotation represents a dict-like type."""
    origin = get_origin(annotation)
    return origin in (dict, Dict) if PY39_PLUS else origin is Dict

# Comprehensive __all__ export
__all__ = [
    # Version info
    "__version__",
    
    # Basic types (always available)
    "Any", "NoReturn", "Union", "Optional", "Callable", "Type", "TypeVar", "Generic", "ClassVar",
    
    # Python 3.7+ (from py3m7)
    "ForwardRef", "OrderedDict", "Counter", "ChainMap", "Deque", "DefaultDict", "PY37_PLUS",
    
    # Python 3.8+ (from py3m8) 
    "Literal", "Protocol", "TypedDict", "Final", "runtime_checkable", "get_args", "get_origin", "PY38_PLUS",
    
    # Python 3.9+ (from py3m9)
    "List", "Dict", "Set", "FrozenSet", "Tuple", "Iterable", "Iterator", "Container", "Collection", "Sized",
    "Mapping", "MutableMapping", "Sequence", "MutableSequence", "AbstractSet", "MutableSet",
    "ItemsView", "KeysView", "ValuesView", "Reversible", "PY39_PLUS",
    
    # Python 3.10+ (from py3m10)
    "ParamSpec", "TypeGuard", "Concatenate", "Annotated", "TypeAlias", "EllipsisType", "UnionType", "UnionOf", "PY310_PLUS",
    
    # Python 3.11+ (from py3m11)
    "Self", "Never", "Required", "NotRequired", "LiteralString", "TypeVarTuple", "Unpack", "PY311_PLUS",
    
    # Python 3.12+ (from py3m12)
    "Hashable", "Buffer", "override", "TypeIs", "PY312_PLUS",
    
    # Support types
    "SupportsAbs", "SupportsBytes", "SupportsComplex", "SupportsFloat", "SupportsIndex",
    "SupportsInt", "SupportsRound", "ByteString", "AnyStr", "Text", "Pattern", "Match",
    "IO", "TextIO", "BinaryIO",
    
    # Async types
    "Awaitable", "Coroutine", "AsyncGenerator", "AsyncIterator", "AsyncIterable",
    "ContextManager", "AsyncContextManager",
    
    # Utilities
    "TYPE_CHECKING", "cast", "overload", "no_type_check", "no_type_check_decorator", "new_class",
    
    # Compatibility helpers
    "create_generic_alias", "is_generic", "is_typing_generic", "get_type_hints_compat",
    
    # Extra utilities
    "NoneType", "is_optional", "is_list_like", "is_dict_like",
]
