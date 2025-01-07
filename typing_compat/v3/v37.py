import sys

if sys.version_info >= (3, 7):
    from typing import ForwardRef
else:
    from typing_extensions import ForwardRef


__all__ = ["ForwardRef"]
