import sys


if sys.version_info >= (3, 10):
    from types import EllipsisType
    from typing import ParamSpec

    from typing import (
        Union,
        TypeGuard,
        Concatenate,
        ParamSpec,
        Optional,
        TypeVar,
        ClassVar,
        Generic,
        Annotated,
    )

    UnionOrNone = Union[None, str]
else:
    from typing_extensions import ParamSpec

    EllipsisType = type(Ellipsis)
    from typing_extensions import TypeGuard, Concatenate, ParamSpec, Annotated
    from typing import Union, Optional, TypeVar, ClassVar, Generic

    UnionOrNone = Union[str, None]


__all__ = [
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
]
