# coding: utf-8

import os
import shutil
from pathlib import Path

from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter


class LocalFileSystemAdapter(FileSystemAdapter):

    def __init__(self, root_directory: str):
        self.root_directory = Path(root_directory)

    def create_directory(self, directory_path: str):
        self.root_directory.joinpath(directory_path).mkdir(parents=True, exist_ok=True)

    def is_readable(self, file_path: str) -> bool:
        file_path = self.root_directory.joinpath(file_path)
        return os.access(file_path, os.R_OK)

    def get_full_path(self, file_path: str) -> str:
        return str(self.root_directory.joinpath(file_path))

    def file_exists(self, file_path: str) -> bool:
        file_path = self.root_directory.joinpath(file_path)
        return os.path.exists(file_path)

    def is_writable(self, file_path: str) -> bool:
        file_path = self.root_directory.joinpath(file_path)
        return os.access(file_path, os.W_OK)

    def read_file(self, file_path: str) -> str:
        file_path = self.root_directory.joinpath(file_path)
        with open(file_path, 'r') as file:
            return file.read()

    def write_file(self, file_path: str, content: str) -> bool:
        file_path = self.root_directory.joinpath(file_path)
        with open(file_path, 'w') as file:
            file.write(content)

        return True

    def delete_file(self, file_path: str):
        if not self.file_exists(file_path):
            return

        file_path = self.root_directory.joinpath(file_path)
        os.unlink(file_path)

    def delete_directory_tree(self, directory_path: str):
        if not self.file_exists(directory_path):
            return

        directory_path = self.root_directory.joinpath(directory_path)
        shutil.rmtree(directory_path)
