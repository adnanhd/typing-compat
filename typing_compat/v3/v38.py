import sys

if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict, Final
else:
    from typing_extensions import Literal, Protocol, TypedDict, Final


__all__ = ["Literal", "Protocol", "TypedDict", "Final"]
