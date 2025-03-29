# coding: utf-8

import os
import shutil

from hashlib import md5
from pathlib import Path

from flask import send_from_directory

from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter


class LocalFileSystemAdapter(FileSystemAdapter):

    def __init__(self, root_directory: str):
        self.root_directory = Path(root_directory)

    def create_directory(self, directory_path: str):
        self.get_full_path(directory_path).mkdir(parents=True, exist_ok=True)

    def is_readable(self, file_path: str) -> bool:
        file_path = self.get_full_path(file_path)
        return os.access(file_path, os.R_OK)

    def get_full_path(self, file_path: str) -> Path:
        return self.root_directory.joinpath(file_path)

    def file_exists(self, file_path: str) -> bool:
        file_path = self.get_full_path(file_path)
        return os.path.exists(file_path)

    def is_writable(self, file_path: str) -> bool:
        file_path = self.get_full_path(file_path)
        return os.access(file_path, os.W_OK)

    def read_file(self, file_path: str) -> str:
        file_path = self.get_full_path(file_path)
        with open(file_path, 'r') as file:
            return file.read()

    def write_file(self, file_path: str, content: str) -> bool:
        file_path = self.get_full_path(file_path)
        with open(file_path, 'w') as file:
            file.write(content)

        return True

    def move_uploaded_file(self, file, destination_directory: str, destination_file_name: str) -> None:
        destination_directory = self.get_full_path(destination_directory)
        destination_file_path = destination_directory.joinpath(destination_file_name)

        if not self.file_exists(str(destination_directory)):
            raise FileNotFoundError(f'Destination directory {destination_directory} does not exist')

        file.save(destination_file_path)

    def delete_file(self, file_path: str) -> None:
        if not self.file_exists(file_path):
            return

        file_path = self.get_full_path(file_path)
        os.unlink(file_path)

    def delete_directory_tree(self, directory_path: str) -> None:
        if not self.file_exists(directory_path):
            return

        directory_path = self.get_full_path(directory_path)
        shutil.rmtree(directory_path)

    def generate_checksum(self, file_path: str) -> str:
        file_path = self.get_full_path(file_path)
        checksum = md5()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * checksum.block_size), b''):
                checksum.update(chunk)

        return checksum.hexdigest()

    def offer_file_download(self, directory: str, file_path: str) -> None:
        send_from_directory(directory, file_path, as_attachment=True)
