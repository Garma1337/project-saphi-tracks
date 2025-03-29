# coding: utf-8

from abc import abstractmethod
from pathlib import Path

from werkzeug.datastructures import FileStorage


class FileNotReadableError(Exception):
    pass


class FileNotWriteableError(Exception):
    pass


class FileSystemAdapter(object):

    @abstractmethod
    def create_directory(self, directory_path: str):
        pass

    @abstractmethod
    def is_readable(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def is_writable(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def get_full_path(self, file_path: str) -> Path:
        pass

    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def write_file(self, file_path: str, content: str) -> bool:
        pass

    @abstractmethod
    def move_uploaded_file(self, file: FileStorage, destination_directory: str, destination_file_name: str) -> None:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass

    @abstractmethod
    def delete_directory_tree(self, directory_path: str) -> None:
        pass

    @abstractmethod
    def generate_checksum(self, file_path: str) -> str:
        pass

    @abstractmethod
    def offer_file_download(self, directory: str, file_path: str) -> None:
        pass
