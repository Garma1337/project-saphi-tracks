# coding: utf-8

from pathlib import Path

from werkzeug.datastructures import FileStorage

from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter, FileNotReadableError


class MockFileSystemAdapter(FileSystemAdapter):

    def __init__(self):
        self.files = {}
        self.directories = {}

    def create_directory(self, directory_path: str):
        if directory_path in self.directories:
            return

        self.directories[directory_path] = {}

    def is_readable(self, file_path: str) -> bool:
        return True

    def is_writable(self, file_path: str) -> bool:
        return True

    def get_full_path(self, file_path: str) -> Path:
        return Path(file_path)

    def file_exists(self, file_path: str) -> bool:
        return file_path in self.files

    def read_file(self, file_path: str) -> str:
        if not self.file_exists(file_path):
            raise FileNotReadableError('File {} does not exist'.format(file_path))

        return self.files[file_path]

    def write_file(self, file_path: str, content: str) -> bool:
        self.files[file_path] = content
        return True

    def move_uploaded_file(self, file: FileStorage, destination_directory: str, destination_file_name: str) -> None:
        destination_directory = self.get_full_path(destination_directory)
        destination_file_path = destination_directory.joinpath(destination_file_name)

        if not self.file_exists(str(destination_directory)):
            raise FileNotFoundError(f'Destination directory {destination_directory} does not exist')

        self.files[str(destination_file_path)] = file

    def generate_checksum(self, file_path: str) -> str:
        return 'checksum'

    def delete_file(self, file_path: str):
        del self.files[file_path]

    def delete_directory_tree(self, directory_path: str):
        del self.directories[directory_path]

    def offer_file_download(self, directory: str, file_path: str) -> None:
        return None
