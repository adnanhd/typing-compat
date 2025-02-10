import sys

if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict, Final, get_args, get_origin
else:
    from typing_extensions import Literal, Protocol, TypedDict, Final

    def get_origin(tp):
        """
        Return the origin type of a generic type.

        For example:
          - get_origin(List[int]) returns list.
          - get_origin(Union[int, str]) returns Union.
          - get_origin(int) returns None.
        """
        return getattr(tp, "__origin__", None)

    def get_args(tp):
        """
        Return the type arguments of a generic type.

        For example:
          - get_args(List[int]) returns (int,).
          - get_args(Union[int, str]) returns (int, str).
          - get_args(int) returns ().
        """
        args = getattr(tp, "__args__", None)
        if args is None:
            return ()
        return args


__all__ = ["Literal", "Protocol", "TypedDict", "Final", "get_args", "get_origin"]


# --- Example usage ---
if __name__ == "__main__":
    from typing import List, Dict, Union, Callable

    print("get_origin(List[int]) =", get_origin(List[int]))  # <class 'list'>
    print("get_args(List[int]) =", get_args(List[int]))  # (int,)

    print("get_origin(Dict[str, int]) =", get_origin(Dict[str, int]))  # <class 'dict'>
    print("get_args(Dict[str, int]) =", get_args(Dict[str, int]))  # (str, int)

    print("get_origin(Union[int, str]) =", get_origin(Union[int, str]))  # typing.Union
    print("get_args(Union[int, str]) =", get_args(Union[int, str]))  # (int, str)

    # Callable example (if supported by your version of typing)
    CallableType = Callable[[int], str]
    print("get_origin(Callable[[int], str]) =", get_origin(CallableType))
    print("get_args(Callable[[int], str]) =", get_args(CallableType))

    # For a non-generic type, we get None or empty tuple:
    print("get_origin(int) =", get_origin(int))  # None
    print("get_args(int) =", get_args(int))  # ()
