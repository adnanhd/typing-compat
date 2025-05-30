"""
Python 3.8+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.8
and provides appropriate fallbacks for older versions.
"""

import sys

# Version check for this module
PY38_PLUS = sys.version_info >= (3, 8)

# Python 3.8+ features
if PY38_PLUS:
    from typing import Literal, Protocol, TypedDict, Final, runtime_checkable, get_args, get_origin
else:
    # Fallback implementations for Python < 3.8
    try:
        from typing_extensions import Literal, Protocol, TypedDict, Final, runtime_checkable
    except ImportError:
        # Ultimate fallbacks for when typing_extensions is not available
        from typing import Union, Any
        
        def Literal(*args):
            """Fallback Literal implementation."""
            if not args:
                return Any
            return Union[tuple(args)] if len(args) > 1 else args[0]
        
        class Protocol:
            """Fallback Protocol base class."""
            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
        
        def TypedDict(typename, fields=None, /, **kwargs):
            """Fallback TypedDict implementation."""
            if fields is None:
                fields = kwargs
            # Return a regular dict class as fallback
            return type(typename, (dict,), {})
        
        def Final(tp=None):
            """Fallback Final implementation."""
            return tp if tp is not None else Any
        
        def runtime_checkable(cls):
            """Fallback runtime_checkable decorator."""
            return cls
    
    # Fallback implementations for get_args and get_origin
    def get_origin(tp):
        """Get the origin type of a generic type."""
        return getattr(tp, "__origin__", None)
    
    def get_args(tp):
        """Get the type arguments of a generic type."""
        args = getattr(tp, "__args__", None)
        return args if args is not None else ()

__all__ = [
    "Literal",
    "Protocol", 
    "TypedDict",
    "Final",
    "runtime_checkable",
    "get_args",
    "get_origin",
    "PY38_PLUS"
]
