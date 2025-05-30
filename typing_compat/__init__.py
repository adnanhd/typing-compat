"""
Typing Compatibility Library - Modular Version

A comprehensive typing compatibility library that provides a unified interface
for all typing-related imports across different Python versions.

This version uses separate modules for each Python version's features,
providing better organization and maintainability.

Key Features:
- Single import source for all typing needs
- Modular version-specific feature handling
- Automatic version detection and compatibility handling
- Support for Python 3.7+ through 3.12+
- Fallback implementations for missing features
- Additional utility functions for type checking

Usage Examples:
    # Basic usage - import everything
    from typing_compat import *
    
    # Selective imports
    from typing_compat import List, Dict, Optional, Literal, Protocol
    
    # Version-specific features work automatically
    from typing_compat import ParamSpec, TypeGuard, Self, override
    
    # Utility functions
    from typing_compat import is_optional, is_list_like, get_type_hints_compat

Module Structure:
    typing_compat/
    ├── __init__.py          # This file - main package interface
    ├── typing_compat.py     # Main unified module  
    ├── py3m7.py            # Python 3.7+ features
    ├── py3m8.py            # Python 3.8+ features
    ├── py3m9.py            # Python 3.9+ features
    ├── py3m10.py           # Python 3.10+ features
    ├── py3m11.py           # Python 3.11+ features
    ├── py3m12.py           # Python 3.12+ features
    └── _version.py         # Version information

Author: Enhanced Typing Compatibility
Version: 0.2.0
"""

# Import everything from the main unified module
from .typing_compat import *

# Re-export version for convenience
from ._version import __version__ as _version_from_file

# Use the version from the main module, but fall back to file version if needed
try:
    __version__
except NameError:
    __version__ = _version_from_file

# Module metadata
__author__ = "Enhanced Typing Compatibility"
__description__ = "Unified typing imports across Python versions - Modular Edition"
__url__ = "https://github.com/adnanhad/typing-compat"

# Version information for users
def get_version_info():
    """Get detailed version information including Python version compatibility."""
    import sys
    
    info = {
        "typing_compat_version": __version__,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "supported_features": {
            "python_37_plus": PY37_PLUS,
            "python_38_plus": PY38_PLUS, 
            "python_39_plus": PY39_PLUS,
            "python_310_plus": PY310_PLUS,
            "python_311_plus": PY311_PLUS,
            "python_312_plus": PY312_PLUS,
        },
        "available_modules": [
            "py3m7", "py3m8", "py3m9", "py3m10", "py3m11", "py3m12"
        ]
    }
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

# Ensure all exports are available at package level
__all__ = [
    # Re-export everything from the main module
    "Any", "NoReturn", "Union", "Optional", "Callable", "Type", "TypeVar", "Generic", "ClassVar",
    "ForwardRef", "OrderedDict", "Counter", "ChainMap", "Deque", "DefaultDict",
    "Literal", "Protocol", "TypedDict", "Final", "runtime_checkable", "get_args", "get_origin",
    "List", "Dict", "Set", "FrozenSet", "Tuple", "Iterable", "Iterator", "Container", "Collection", "Sized",
    "Mapping", "MutableMapping", "Sequence", "MutableSequence", "AbstractSet", "MutableSet",
    "ItemsView", "KeysView", "ValuesView", "Reversible",
    "ParamSpec", "TypeGuard", "Concatenate", "Annotated", "TypeAlias", "EllipsisType", "UnionType", "UnionOf",
    "Self", "Never", "Required", "NotRequired", "LiteralString", "TypeVarTuple", "Unpack",
    "Hashable", "Buffer", "override", "TypeIs",
    "SupportsAbs", "SupportsBytes", "SupportsComplex", "SupportsFloat", "SupportsIndex",
    "SupportsInt", "SupportsRound", "ByteString", "AnyStr", "Text", "Pattern", "Match",
    "IO", "TextIO", "BinaryIO",
    "Awaitable", "Coroutine", "AsyncGenerator", "AsyncIterator", "AsyncIterable",
    "ContextManager", "AsyncContextManager",
    "TYPE_CHECKING", "cast", "overload", "no_type_check", "no_type_check_decorator", "new_class",
    "create_generic_alias", "is_generic", "is_typing_generic", "get_type_hints_compat",
    "PY37_PLUS", "PY38_PLUS", "PY39_PLUS", "PY310_PLUS", "PY311_PLUS", "PY312_PLUS",
    "NoneType", "is_optional", "is_list_like", "is_dict_like",
    
    # Package metadata and utilities
    "__version__", "__author__", "__description__", "__url__",
    "get_version_info", "print_version_info"
]
