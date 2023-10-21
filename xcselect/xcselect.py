import ctypes
from pathlib import Path
from typing import Callable

from attrs import define
from packaging.version import Version


@define
class DeveloperDirPath:
    path: Path
    from_env_var: bool
    from_command_line_tools: bool
    from_default: bool


_BPtr = ctypes.POINTER(ctypes.c_bool)


class _XCSelect:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.dylib = ctypes.CDLL("/usr/lib/libxcselect.dylib")
        return cls._instance

    @property
    def xcselect_version(self) -> Callable[[], ctypes.c_char_p]:
        if not hasattr(self, "_xcselect_get_version"):
            func = self.dylib.xcselect_get_version
            func.restype = ctypes.c_char_p
            self._xcselect_get_version = func
        return self._xcselect_get_version

    @property
    def xcselect_get_developer_dir_path(
        self,
    ) -> Callable[[ctypes.c_char_p, ctypes.c_int, _BPtr, _BPtr, _BPtr], ctypes.c_bool]:
        if not hasattr(self, "_xcselect_get_developer_dir_path"):
            func = self.dylib.xcselect_get_developer_dir_path
            func.arg_types = [ctypes.c_char_p, ctypes.c_int, _BPtr, _BPtr, _BPtr]
            func.restype = ctypes.c_bool
            self._xcselect_get_developer_dir_path = func
        return self._xcselect_get_developer_dir_path


def get_version() -> Version:
    return Version(_XCSelect().xcselect_version().decode())


def get_developer_dir_path() -> DeveloperDirPath:
    buf = ctypes.create_string_buffer(8 * 1024)
    from_env_var = ctypes.c_bool()
    from_clt = ctypes.c_bool()
    from_default = ctypes.c_bool()
    if not _XCSelect().xcselect_get_developer_dir_path(
        ctypes.pointer(buf),
        len(buf),
        ctypes.pointer(from_env_var),
        ctypes.pointer(from_clt),
        ctypes.pointer(from_default),
    ):
        raise RuntimeError("xcselect_get_developer_dir_path returned false")
    return DeveloperDirPath(
        Path(buf.value.decode()), from_env_var.value, from_clt.value, from_default.value
    )


__all__ = ("DeveloperDirPath", "Version", "get_version", "get_developer_dir_path")
