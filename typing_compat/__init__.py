"""
Enhanced Typing Compatibility Module

Main loader and importer for all typing compatibility features.
This module imports from:
1. typing_compat.py (base/generic utilities)
2. All py3mX.py modules (version-specific features)

Creates a unified interface for all typing needs across Python versions.

Usage:
    from typing_compat import *
    # or
    from typing_compat import List, Dict, Optional, Literal, Protocol, Generator, PathLike, etc.
"""

# Import base/generic utilities from typing_compat.py
from .typing_compat import *

# Import version-specific features from all py3mX.py modules
from .py3m5 import *    # Python 3.5+: Generator, core typing, NamedTuple, NewType
from .py3m6 import *    # Python 3.6+: PathLike, ClassVar, Type improvements  
from .py3m7 import *    # Python 3.7+: ForwardRef, OrderedDict, Counter, etc.
from .py3m8 import *    # Python 3.8+: Literal, Protocol, TypedDict, SupportsIndex
from .py3m9 import *    # Python 3.9+: Built-in generics, collections.abc
from .py3m10 import *   # Python 3.10+: ParamSpec, TypeGuard, union operators
from .py3m11 import *   # Python 3.11+: Self, Never, Required/NotRequired
from .py3m12 import *   # Python 3.12+: override, TypeIs, Buffer

# Explicitly import version from main implementation
from .typing_compat import __version__

# Re-export version info functions for easy access
from .typing_compat import get_version_info, print_version_info

# Re-export utility functions for easy access
from .typing_compat import (
    # Type checking utilities
    is_optional, is_list_like, is_dict_like, is_generator_like, is_pathlike,
    
    # Compatibility helpers
    create_generic_alias, is_generic, is_typing_generic, get_type_hints_compat,
    get_never_type, get_self_type,
    
    # Common utilities
    NoneType,
)

# Master __all__ export - combines everything from all modules
__all__ = [
    # Version info
    "__version__",
    
    # === FROM typing_compat.py (Base/Generic) ===
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
    
    # === FROM py3m5.py (Python 3.5+) ===
    "List", "Dict", "Set", "FrozenSet", "Tuple", "Iterable", "Iterator", 
    "Mapping", "MutableMapping", "Sequence", "MutableSequence",
    "Generator",  # CRITICAL: Now available!
    "NamedTuple", "NewType", "SupportsInt", "SupportsFloat", "SupportsComplex", 
    "SupportsBytes", "SupportsAbs", "SupportsRound", "PY35_PLUS",
    
    # === FROM py3m6.py (Python 3.6+) ===
    "Type", "Container", "Sized", "AbstractSet", "MutableSet",
    "ItemsView", "KeysView", "ValuesView", "ByteString",
    "PathLike",  # CRITICAL: Now available!
    "PY36_PLUS",
    
    # === FROM py3m7.py (Python 3.7+) ===
    "ForwardRef", "OrderedDict", "Counter", "ChainMap", "Deque", "DefaultDict", "PY37_PLUS",
    
    # === FROM py3m8.py (Python 3.8+) ===
    "Literal", "Protocol", "TypedDict", "Final", "runtime_checkable", "get_args", "get_origin",
    "SupportsIndex",  # CRITICAL: Now available!
    "Pattern", "Match", "PY38_PLUS",
    
    # === FROM py3m9.py (Python 3.9+) ===
    "Reversible", "PY39_PLUS",
    
    # === FROM py3m10.py (Python 3.10+) ===
    "ParamSpec", "TypeGuard", "Concatenate", "Annotated", "TypeAlias", 
    "EllipsisType", "UnionType", "UnionOf", "PY310_PLUS",
    
    # === FROM py3m11.py (Python 3.11+) ===
    "Self", "Never", "Required", "NotRequired", "LiteralString", 
    "TypeVarTuple", "Unpack", "PY311_PLUS",
    
    # === FROM py3m12.py (Python 3.12+) ===
    "Hashable", "Buffer", "override", "TypeIs", "PY312_PLUS",
    
    # === Compatibility Helpers (from typing_compat.py) ===
    "create_generic_alias", "is_generic", "is_typing_generic", "get_type_hints_compat",
    "get_never_type", "get_self_type",
    
    # === Type Checking Utilities (from typing_compat.py) ===
    "is_optional", "is_list_like", "is_dict_like", "is_generator_like", "is_pathlike",
    
    # === Extra Utilities ===
    "NoneType",
    
    # === Version Info Utilities ===
    "get_version_info", "print_version_info",
]

# Ensure all version flags are available at package level for utility functions
# These are imported from the py3mX modules above, but we make them explicit
# for users who want to check version capabilities
_VERSION_FLAGS = [
    'PY35_PLUS', 'PY36_PLUS', 'PY37_PLUS', 'PY38_PLUS', 
    'PY39_PLUS', 'PY310_PLUS', 'PY311_PLUS', 'PY312_PLUS'
]

# Add version flags to __all__ (they're already imported via py3mX modules)
__all__.extend(_VERSION_FLAGS)
