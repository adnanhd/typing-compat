import pytest
import sys
from typing_compat.v3.v38 import Literal, Protocol, TypedDict, Final

def test_literal_module():
    if sys.version_info >= (3, 8):
        assert Literal.__module__ == "typing"
    else:
        assert Literal.__module__ == "typing_extensions"

def test_protocol_module():
    if sys.version_info >= (3, 8):
        assert Protocol.__module__ == "typing"
    else:
        assert Protocol.__module__ == "typing_extensions"

def test_typed_dict_module():
    if sys.version_info >= (3, 8):
        assert TypedDict.__module__ == "typing"
    else:
        assert TypedDict.__module__ == "typing_extensions"

def test_final_module():
    if sys.version_info >= (3, 8):
        assert Final.__module__ == "typing"
    else:
        assert Final.__module__ == "typing_extensions"
