import sys
from types import new_class
from typing import TYPE_CHECKING, Any, Callable

from .v37 import *
from .v38 import *
from .v39 import *
from .v310 import *

from .v312 import *

if TYPE_CHECKING:
    from typing import (
        List,
        Dict,
        Set,
        Tuple,
        Union,
        Type,
        Optional,
        TypeVar,
        ClassVar,
        Generic,
    )

__all__ = [
    "Any",
    "Callable",
    "TYPE_CHECKING",
    "new_class",
    "ForwardRef",
    "Literal",
    "Protocol",
    "TypedDict",
    "Final",
    "List",
    "Set",
    "Dict",
    "Tuple",
    "Type",
    "ParamSpec",
    "EllipsisType",
    "TypeGuard",
    "Concatenate",
    "ParamSpec",
    "Annotated",
    "Union",
    "Optional",
    "TypeVar",
    "ClassVar",
    "Generic",
    "UnionOrNone",
    "Hashable",
    "Iterable",
    "Iterator",
    "get_args","get_origin"
]
