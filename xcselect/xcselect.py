import ctypes
from functools import cached_property
from pathlib import Path
from typing import Callable, Optional, Self

from attrs import define
from packaging.version import Version


@define
class DeveloperDir:
    path: Path
    from_env_var: bool
    from_command_line_tools: bool
    from_default: bool

    def __call__(self) -> Path:
        return self.path


_BPtr = ctypes.POINTER(ctypes.c_bool)
_PATH_MAX = 8 * 1024


class _XCSelect:
    _instance: Optional[Self] = None
    dylib: Optional[ctypes.CDLL] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.dylib = ctypes.CDLL("/usr/lib/libxcselect.dylib")
        return cls._instance

    @cached_property
    def xcselect_version(self) -> Callable[[], Version]:
        assert self.dylib is not None
        func = self.dylib.xcselect_get_version
        func.argtypes = ()
        func.restype = ctypes.c_char_p

        def handle_result(res, func, args) -> Version:
            if not res:
                raise RuntimeError("xcselect_get_version returned NULL")
            return Version(res.decode())

        func.errcheck = handle_result
        return func

    @cached_property
    def xcselect_get_developer_dir_path(
        self,
    ) -> Callable[[ctypes.c_char_p, ctypes.c_int, _BPtr, _BPtr, _BPtr], DeveloperDir]:
        assert self.dylib is not None
        func = self.dylib.xcselect_get_developer_dir_path
        func.argtypes = (ctypes.c_char_p, ctypes.c_int, _BPtr, _BPtr, _BPtr)
        func.restype = ctypes.c_bool

        def handle_result(res, func, args) -> DeveloperDir:
            if not res:
                raise RuntimeError("xcselect_get_developer_dir_path returned false")
            return DeveloperDir(
                Path(args[0].value.decode()),
                args[2].contents.value,
                args[3].contents.value,
                args[4].contents.value,
            )

        func.errcheck = handle_result
        return func


def version() -> Version:
    return _XCSelect().xcselect_version()


def developer_dir() -> DeveloperDir:
    buf = ctypes.create_string_buffer(_PATH_MAX)
    return _XCSelect().xcselect_get_developer_dir_path(
        buf,
        len(buf),
        ctypes.pointer(ctypes.c_bool()),
        ctypes.pointer(ctypes.c_bool()),
        ctypes.pointer(ctypes.c_bool()),
    )


__all__ = ("DeveloperDir", "Version", "version", "developer_dir")
