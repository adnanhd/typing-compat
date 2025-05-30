"""
Python 3.11+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.11,
including Self, Never, Required, NotRequired, and other advanced features.
"""

import sys

# Version check for this module
PY311_PLUS = sys.version_info >= (3, 11)

# Python 3.11+ features
if PY311_PLUS:
    try:
        from typing import Self, Never, Required, NotRequired, LiteralString, TypeVarTuple, Unpack
    except ImportError:
        # Some features might not be available even in 3.11, fallback to typing_extensions
        from typing_extensions import Self, Never, Required, NotRequired, LiteralString, TypeVarTuple, Unpack
else:
    # Fallback implementations for Python < 3.11
    try:
        from typing_extensions import Self, Never, Required, NotRequired, LiteralString, TypeVarTuple, Unpack
    except ImportError:
        # Ultimate fallbacks when typing_extensions is not available
        from typing import TypeVar, Any, NoReturn
        
        # Self type fallback
        Self = TypeVar('Self')
        
        # Never type fallback (similar to NoReturn)
        Never = NoReturn
        
        def Required(tp):
            """Fallback Required implementation."""
            return tp
        
        def NotRequired(tp):
            """Fallback NotRequired implementation.""" 
            return tp
        
        # LiteralString fallback
        LiteralString = str
        
        class TypeVarTuple:
            """Fallback TypeVarTuple implementation."""
            def __init__(self, name):
                self.name = name
        
        def Unpack(tp):
            """Fallback Unpack implementation."""
            return tp

__all__ = [
    "Self",
    "Never",
    "Required",
    "NotRequired", 
    "LiteralString",
    "TypeVarTuple",
    "Unpack",
    "PY311_PLUS"
]
