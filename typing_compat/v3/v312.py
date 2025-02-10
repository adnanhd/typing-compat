import sys

if sys.version_info >= (3, 12):
    from collections.abc import Hashable
else:
    from typing import Hashable


__all__ = ["Hashable"]
