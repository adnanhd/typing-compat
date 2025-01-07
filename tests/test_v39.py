import pytest
import sys
from typing_compat.v3.v39 import List, Set, Dict, Tuple, Type

def test_list_type():
    if sys.version_info >= (3, 9):
        assert List == list
    else:
        assert List != list

def test_set_type():
    if sys.version_info >= (3, 9):
        assert Set == set
    else:
        assert Set != set

def test_dict_type():
    if sys.version_info >= (3, 9):
        assert Dict == dict
    else:
        assert Dict != dict

def test_tuple_type():
    if sys.version_info >= (3, 9):
        assert Tuple == tuple
    else:
        assert Tuple != tuple

def test_type_type():
    if sys.version_info >= (3, 9):
        assert Type == type
    else:
        assert Type != type
