# coding: utf-8

from abc import abstractmethod


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
    def file_exists(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def write_file(self, file_path: str, content: str) -> bool:
        pass

    @abstractmethod
    def delete_file(self, file_path: str):
        pass

    @abstractmethod
    def delete_directory_tree(self, directory_path: str):
        pass
