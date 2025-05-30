"""
Python 3.9+ typing features with fallbacks.

This module handles imports for features introduced in Python 3.9,
particularly the built-in generic types that replace typing module equivalents.
"""

import sys

# Version check for this module
PY39_PLUS = sys.version_info >= (3, 9)

# Python 3.9+ features (built-in generic types)
if PY39_PLUS:
    # Use built-in types as generics
    List = list
    Dict = dict
    Set = set
    FrozenSet = frozenset
    Tuple = tuple
    Type = type
    
    # Import from collections.abc for better compatibility
    from collections.abc import (
        Iterable, Iterator, Container, Collection, Sized,
        Mapping, MutableMapping, Sequence, MutableSequence,
        AbstractSet, MutableSet, ItemsView, KeysView, ValuesView
    )
else:
    # Fallback to typing module for Python < 3.9
    from typing import (
        List, Dict, Set, FrozenSet, Tuple, Type,
        Iterable, Iterator, Container, Collection, Sized,
        Mapping, MutableMapping, Sequence, MutableSequence,
        AbstractSet, MutableSet, ItemsView, KeysView, ValuesView
    )

# Additional collections that are version-independent
try:
    from collections.abc import Reversible
except ImportError:
    from typing import Reversible

__all__ = [
    "List",
    "Dict", 
    "Set",
    "FrozenSet",
    "Tuple",
    "Type",
    "Iterable",
    "Iterator", 
    "Container",
    "Collection",
    "Sized",
    "Mapping",
    "MutableMapping",
    "Sequence", 
    "MutableSequence",
    "AbstractSet",
    "MutableSet",
    "ItemsView",
    "KeysView", 
    "ValuesView",
    "Reversible",
    "PY39_PLUS"
]
