import pytest
import sys
from typing_compat.v3.v310 import (
    EllipsisType,
    UnionOrNone,
    ParamSpec,
    TypeGuard,
    Concatenate,
    Annotated,
)

def test_ellipsis_type():
    if sys.version_info >= (3, 10):
        assert EllipsisType is type(Ellipsis)
    else:
        assert EllipsisType is type(Ellipsis)

def test_union_or_none():
    if sys.version_info >= (3, 10):
        assert UnionOrNone == (None | str)

def test_param_spec_module():
    if sys.version_info >= (3, 10):
        assert ParamSpec.__module__ == "typing"
    else:
        assert ParamSpec.__module__ == "typing_extensions"

def test_type_guard_module():
    if sys.version_info >= (3, 10):
        assert TypeGuard.__module__ == "typing"
    else:
        assert TypeGuard.__module__ == "typing_extensions"

def test_concatenate_module():
    if sys.version_info >= (3, 10):
        assert Concatenate.__module__ == "typing"
    else:
        assert Concatenate.__module__ == "typing_extensions"

def test_annotated_module():
    if sys.version_info >= (3, 10):
        assert Annotated.__module__ == "typing"
    else:
        assert Annotated.__module__ == "typing_extensions"
