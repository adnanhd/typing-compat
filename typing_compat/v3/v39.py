import sys

if sys.version_info >= (3, 9):
    List = list
    Set = set
    Dict = dict
    Tuple = tuple
    Type = type
else:
    from typing import List, Set, Dict, Tuple, Type

__all__ = ["List", "Set", "Dict", "Tuple", "Type"]
