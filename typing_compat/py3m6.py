"""
Python 3.6+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.6
and provides appropriate fallbacks for older versions.
"""

import sys

# Version check for this module
PY36_PLUS = sys.version_info >= (3, 6)

# Python 3.6+ features
if PY36_PLUS:
    # ClassVar was introduced in Python 3.6
    from typing import ClassVar
    
    # Type was available but improved in 3.6
    from typing import Type
    
    # PathLike was introduced in Python 3.6 - IMPORTANT: This was missing!
    try:
        from os import PathLike
    except ImportError:
        # Fallback for very early 3.6 versions
        class PathLike:
            """Fallback PathLike implementation."""
            def __fspath__(self): ...
    
    # Generic type aliases support improved in 3.6
    from typing import TypeVar, Generic, Union, Optional, Any
    
    # Basic collections that were stabilized in 3.6
    from typing import List, Dict, Set, FrozenSet, Tuple
    from typing import Iterable, Iterator, Container, Sized
    from typing import Mapping, MutableMapping, Sequence, MutableSequence
    from typing import AbstractSet, MutableSet
    
    # Collections views that are available
    try:
        from typing import ItemsView, KeysView, ValuesView
    except ImportError:
        # Fall back to collections.abc if not in typing
        try:
            from collections.abc import ItemsView, KeysView, ValuesView
        except ImportError:
            # Ultimate fallback
            ItemsView = object
            KeysView = object
            ValuesView = object
    
    # Additional support types introduced or improved in 3.6
    try:
        from typing import NoReturn
    except ImportError:
        # NoReturn wasn't available until later, create fallback
        class NoReturn:
            """Fallback NoReturn type."""
            pass
    
    # ByteString (note: deprecated in 3.12 but still useful)
    try:
        from typing import ByteString
    except ImportError:
        # Fallback ByteString
        try:
            from collections.abc import ByteString
        except ImportError:
            ByteString = bytes  # Simple fallback

else:
    # Fallback implementations for Python < 3.6
    try:
        from typing_extensions import ClassVar
    except ImportError:
        # Ultimate fallback - ClassVar as identity function
        def ClassVar(tp):
            """Fallback ClassVar implementation."""
            return tp
    
    # PathLike fallback for Python < 3.6
    class PathLike:
        """Fallback PathLike implementation."""
        def __fspath__(self): ...
    
    # These should be available in older typing modules but include for safety
    try:
        from typing import (
            Type, TypeVar, Generic, Union, Optional, Any,
            List, Dict, Set, FrozenSet, Tuple,
            Iterable, Iterator, Container, Sized,
            Mapping, MutableMapping, Sequence, MutableSequence,
            AbstractSet, MutableSet
        )
    except ImportError:
        # Very basic fallbacks for extremely old Python versions
        TypeVar = None
        Generic = None
        Union = None
        Optional = None
        Any = None
        Type = type
        List = list
        Dict = dict
        Set = set
        FrozenSet = frozenset
        Tuple = tuple
        
        # Create minimal interface
        class _MinimalType:
            pass
        
        Iterable = Iterator = Container = Sized = _MinimalType
        Mapping = MutableMapping = Sequence = MutableSequence = _MinimalType
        AbstractSet = MutableSet = _MinimalType
    
    # Views fallback
    try:
        from collections.abc import ItemsView, KeysView, ValuesView
    except ImportError:
        ItemsView = KeysView = ValuesView = object
    
    # NoReturn fallback
    class NoReturn:
        """Fallback NoReturn type."""
        pass
    
    # ByteString fallback
    ByteString = bytes

__all__ = [
    "ClassVar",
    "Type",
    "PathLike",  # ADDED!
    "TypeVar",
    "Generic", 
    "Union",
    "Optional",
    "Any",
    "List",
    "Dict",
    "Set",
    "FrozenSet", 
    "Tuple",
    "Iterable",
    "Iterator",
    "Container",
    "Sized",
    "Mapping",
    "MutableMapping",
    "Sequence",
    "MutableSequence",
    "AbstractSet",
    "MutableSet",
    "ItemsView",  # ADDED!
    "KeysView",   # ADDED!
    "ValuesView", # ADDED!
    "NoReturn",   # ADDED!
    "ByteString", # ADDED!
    "PY36_PLUS"
]
