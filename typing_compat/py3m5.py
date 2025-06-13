"""
Python 3.5+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.5,
primarily the core typing module that was introduced with PEP 484.
"""

import sys

# Version check for this module
PY35_PLUS = sys.version_info >= (3, 5)

# Python 3.5+ features (core typing module)
if PY35_PLUS:
    try:
        from typing import (
            # Core types
            Any, Union, Optional, Tuple, Callable, TypeVar, Generic,
            # Container types  
            List, Dict, Set, FrozenSet,
            # Abstract base classes
            Iterable, Iterator, Mapping, MutableMapping, Sequence, MutableSequence,
            # Generator - IMPORTANT: This was missing!
            Generator,
            # Utility types
            TYPE_CHECKING, cast, overload, NamedTuple, NewType,
            # Text and pattern types
            Text, AnyStr, Pattern, Match,
            # IO types
            IO, TextIO, BinaryIO,
            # Support types
            SupportsInt, SupportsFloat, SupportsComplex, SupportsBytes,
            SupportsAbs, SupportsRound,
        )
    except ImportError:
        # Some features might not be available in early 3.5, provide fallbacks
        from typing import (
            Any, Union, Optional, Tuple, Callable, TypeVar, Generic,
            List, Dict, Set, FrozenSet,
            Iterable, Iterator, Mapping, MutableMapping, Sequence, MutableSequence,
            TYPE_CHECKING, cast, overload,
        )
        
        # Generator fallback - very important!
        try:
            from typing import Generator
        except ImportError:
            # Create a basic Generator fallback
            def Generator(*args):
                """Fallback Generator implementation."""
                if len(args) == 0:
                    return Iterator
                elif len(args) == 1:
                    return Iterator[args[0]]
                else:
                    # Generator[YieldType, SendType, ReturnType]
                    return Iterator[args[0]]  # Return Iterator of yield type
        
        # Fallbacks for potentially missing features
        try:
            from typing import NamedTuple
        except ImportError:
            from collections import namedtuple
            def NamedTuple(typename, fields):
                """Fallback NamedTuple implementation."""
                return namedtuple(typename, fields)
        
        try:
            from typing import NewType
        except ImportError:
            def NewType(name, tp):
                """Fallback NewType implementation."""
                def new_type(x):
                    return x
                new_type.__name__ = name
                new_type.__supertype__ = tp
                return new_type
        
        try:
            from typing import Text, AnyStr, Pattern, Match, IO, TextIO, BinaryIO
        except ImportError:
            # Text type fallbacks
            Text = str
            AnyStr = TypeVar('AnyStr', str, bytes)
            Pattern = type(None)  # Placeholder
            Match = type(None)    # Placeholder
            IO = object           # Placeholder
            TextIO = object       # Placeholder  
            BinaryIO = object     # Placeholder
        
        try:
            from typing import (
                SupportsInt, SupportsFloat, SupportsComplex, SupportsBytes,
                SupportsAbs, SupportsRound
            )
        except ImportError:
            # Support type fallbacks
            class SupportsInt:
                def __int__(self) -> int: ...
            
            class SupportsFloat:
                def __float__(self) -> float: ...
            
            class SupportsComplex:
                def __complex__(self) -> complex: ...
            
            class SupportsBytes:
                def __bytes__(self) -> bytes: ...
            
            class SupportsAbs:
                def __abs__(self): ...
            
            class SupportsRound:
                def __round__(self, ndigits: int = 0): ...

else:
    # Fallback implementations for Python < 3.5 (no typing module)
    
    # Create basic type placeholders
    class Any:
        """Fallback Any type."""
        def __instancecheck__(self, instance):
            return True
    
    Any = Any()
    
    def Union(*args):
        """Fallback Union implementation."""
        if len(args) == 1:
            return args[0]
        return args
    
    def Optional(tp):
        """Fallback Optional implementation."""
        return Union(tp, type(None))
    
    def Tuple(*args):
        """Fallback Tuple implementation."""
        return tuple
    
    def Callable(*args):
        """Fallback Callable implementation."""
        return type(lambda: None)
    
    class TypeVar:
        """Fallback TypeVar implementation."""
        def __init__(self, name, *constraints, **kwargs):
            self.name = name
            self.constraints = constraints
            self.bound = kwargs.get('bound')
    
    class Generic:
        """Fallback Generic implementation."""
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
    
    # Container type fallbacks
    List = list
    Dict = dict
    Set = set
    FrozenSet = frozenset
    
    # Abstract types fallbacks
    try:
        from collections.abc import Iterable, Iterator, Mapping, MutableMapping, Sequence, MutableSequence
    except ImportError:
        from collections import Iterable, Iterator, Mapping, MutableMapping, Sequence, MutableSequence
    
    # Generator fallback for Python < 3.5
    def Generator(*args):
        """Fallback Generator implementation for Python < 3.5."""
        return Iterator
    
    # Utility constants and functions
    TYPE_CHECKING = False
    
    def cast(tp, obj):
        """Fallback cast implementation."""
        return obj
    
    def overload(func):
        """Fallback overload decorator."""
        return func
    
    # NamedTuple fallback
    from collections import namedtuple
    def NamedTuple(typename, fields):
        """Fallback NamedTuple implementation."""
        if isinstance(fields, str):
            fields = fields.split()
        return namedtuple(typename, fields)
    
    def NewType(name, tp):
        """Fallback NewType implementation."""
        def new_type(x):
            return x
        new_type.__name__ = name
        new_type.__supertype__ = tp
        return new_type
    
    # Text and pattern types
    Text = str
    AnyStr = TypeVar('AnyStr', str, bytes)
    Pattern = type(None)
    Match = type(None)
    IO = object
    TextIO = object
    BinaryIO = object
    
    # Support types (minimal implementations)
    class SupportsInt:
        def __int__(self) -> int: ...
    
    class SupportsFloat:
        def __float__(self) -> float: ...
    
    class SupportsComplex:
        def __complex__(self) -> complex: ...
    
    class SupportsBytes:
        def __bytes__(self) -> bytes: ...
    
    class SupportsAbs:
        def __abs__(self): ...
    
    class SupportsRound:
        def __round__(self, ndigits: int = 0): ...

__all__ = [
    # Core types
    "Any", "Union", "Optional", "Tuple", "Callable", "TypeVar", "Generic",
    
    # Container types
    "List", "Dict", "Set", "FrozenSet",
    
    # Abstract base classes
    "Iterable", "Iterator", "Mapping", "MutableMapping", "Sequence", "MutableSequence",
    
    # Generator - ADDED!
    "Generator",
    
    # Utility types
    "TYPE_CHECKING", "cast", "overload", "NamedTuple", "NewType",
    
    # Text and pattern types
    "Text", "AnyStr", "Pattern", "Match",
    
    # IO types
    "IO", "TextIO", "BinaryIO",
    
    # Support types
    "SupportsInt", "SupportsFloat", "SupportsComplex", "SupportsBytes",
    "SupportsAbs", "SupportsRound",
    
    # Version flag
    "PY35_PLUS"
]
