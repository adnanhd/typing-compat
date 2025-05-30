"""
Python 3.10+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.10,
including ParamSpec, TypeGuard, union operator support, and more.
"""

import sys
from typing import Union

# Version check for this module
PY310_PLUS = sys.version_info >= (3, 10)

# Python 3.10+ features
if PY310_PLUS:
    from types import EllipsisType, UnionType
    from typing import ParamSpec, TypeGuard, Concatenate, TypeAlias
    
    # Try to import Annotated from typing, fallback to typing_extensions
    try:
        from typing import Annotated
    except ImportError:
        from typing_extensions import Annotated
    
    # Union syntax support using | operator
    def UnionOf(*types):
        """Create union types using | syntax when available."""
        if len(types) == 0:
            raise ValueError("UnionOf requires at least one type")
        if len(types) == 1:
            return types[0]
        
        # Use the new union operator
        result = types[0]
        for t in types[1:]:
            result = result | t
        return result

else:
    # Fallback implementations for Python < 3.10
    try:
        from typing_extensions import ParamSpec, TypeGuard, Concatenate, Annotated, TypeAlias
    except ImportError:
        # Ultimate fallbacks
        from typing import TypeVar, Callable, Any
        
        class ParamSpec:
            """Fallback ParamSpec implementation."""
            def __init__(self, name):
                self.name = name
                # Create dummy args and kwargs attributes
                self.args = TypeVar(f"{name}_args")
                self.kwargs = TypeVar(f"{name}_kwargs")
                
            def __repr__(self):
                return f"ParamSpec('{self.name}')"
        
        def TypeGuard(tp):
            """Fallback TypeGuard implementation."""
            # Return bool as the base type guard
            return bool
        
        def Concatenate(*args):
            """Fallback Concatenate implementation."""
            if not args:
                return ()
            return args
        
        def Annotated(tp, *metadata):
            """Fallback Annotated implementation."""
            # Just return the base type, ignore metadata
            return tp
        
        def TypeAlias(tp):
            """Fallback TypeAlias implementation."""
            return tp
    
    # Fallback type definitions
    EllipsisType = type(Ellipsis)
    UnionType = type(Union[int, str])
    
    def UnionOf(*types):
        """Create union types using Union for older Python versions."""
        if len(types) == 0:
            raise ValueError("UnionOf requires at least one type")
        if len(types) == 1:
            return types[0]
        return Union[tuple(types)]

__all__ = [
    "ParamSpec",
    "TypeGuard",
    "Concatenate", 
    "Annotated",
    "TypeAlias",
    "EllipsisType",
    "UnionType",
    "UnionOf",
    "PY310_PLUS"
]
