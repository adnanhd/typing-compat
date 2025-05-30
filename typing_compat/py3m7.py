"""
Python 3.7+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.7
and provides appropriate fallbacks for older versions.
"""

import sys

# Version check for this module
PY37_PLUS = sys.version_info >= (3, 7)

# Python 3.7+ features
if PY37_PLUS:
    from typing import ForwardRef, OrderedDict, Counter, ChainMap, Deque, DefaultDict
else:
    # Fallback implementations for Python < 3.7
    try:
        from typing_extensions import ForwardRef
    except ImportError:
        # Ultimate fallback - try to get from typing with alternate name
        try:
            from typing import _ForwardRef as ForwardRef
        except ImportError:
            # Create a minimal fallback
            class ForwardRef:
                def __init__(self, arg, is_argument=True):
                    self.arg = arg
                    self.is_argument = is_argument
    
    # These were available in earlier versions but are included for completeness
    from typing import OrderedDict, Counter, ChainMap, Deque, DefaultDict

__all__ = [
    "ForwardRef",
    "OrderedDict", 
    "Counter",
    "ChainMap", 
    "Deque",
    "DefaultDict",
    "PY37_PLUS"
]
