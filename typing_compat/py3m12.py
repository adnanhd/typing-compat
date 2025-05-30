"""
Python 3.12+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.12,
including Buffer, override decorator, TypeIs, and other latest features.
"""

import sys

# Version check for this module
PY312_PLUS = sys.version_info >= (3, 12)

# Python 3.12+ features
if PY312_PLUS:
    # Hashable moved to collections.abc in 3.12
    from collections.abc import Hashable, Buffer
    
    try:
        from typing import override, TypeIs
    except ImportError:
        # Fallback to typing_extensions if not available in typing
        from typing_extensions import override, TypeIs
else:
    # Fallback implementations for Python < 3.12
    
    # Hashable location handling
    try:
        from collections.abc import Hashable
    except ImportError:
        from typing import Hashable
    
    # Buffer type fallback
    try:
        from collections.abc import Buffer
    except ImportError:
        # Buffer protocol fallback - use bytes as base type
        Buffer = bytes
    
    # Override and TypeIs fallbacks
    try:
        from typing_extensions import override, TypeIs
    except ImportError:
        # Ultimate fallbacks
        def override(func):
            """Fallback override decorator."""
            # Just return the function unchanged
            return func
        
        def TypeIs(tp):
            """Fallback TypeIs implementation."""
            # Return bool as the base type predicate
            return bool

__all__ = [
    "Hashable",
    "Buffer",
    "override", 
    "TypeIs",
    "PY312_PLUS"
]
