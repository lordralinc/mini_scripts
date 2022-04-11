import os
import typing
import typing as ty
import uuid
from pathlib import Path


class TempFile:

    def __init__(
            self,
            temp_directory: typing.Union[str, Path],
            name: str = None,
            ext: str = "",
            is_bytes: bool = True,
            **extra
    ):
        self.temp_directory = temp_directory if isinstance(temp_directory, Path) else Path(temp_directory)
        self.name = name or uuid.uuid4().hex
        self.ext = ext
        self.is_bytes = is_bytes
        self.extra = extra
        self.file = None

    def __enter__(self) -> "TempFile":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            os.remove(self.file_path)
        except:
            pass

    def read(self) -> ty.Any:
        with open(self.file_path, 'r' + ('b' if self.is_bytes else ''), **self.extra) as file:
            return file.read()

    def write(self, value: ty.Any):
        with open(self.file_path, 'w' + ('b' if self.is_bytes else ''), **self.extra) as file:
            return file.write(value)

    @property
    def file_name(self) -> str:
        return self.name + "." + self.ext

    @property
    def file_path(self) -> Path:
        return self.temp_directory / self.file_name
