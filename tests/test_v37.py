import pytest
import sys
from typing_compat.v3.v37 import ForwardRef

def test_forward_ref_module():
    if sys.version_info >= (3, 7):
        assert ForwardRef.__module__ == "typing"
    else:
        assert ForwardRef.__module__ == "typing_extensions"
