# coding: utf-8

from pathlib import Path

from werkzeug.datastructures import FileStorage

from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter, FileNotReadableError


class MockFileSystemAdapter(FileSystemAdapter):

    def __init__(self):
        self.files = {}

    def create_directory(self, directory_path: str):
        if directory_path in self.files:
            return

        self.files[directory_path] = 1

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

        if not str(destination_directory) in self.files:
            raise FileNotFoundError(f'Destination directory {destination_directory} does not exist')

        self.files[str(destination_directory)] = 1
        self.files[str(destination_file_name)] = file.stream.read()

    def generate_checksum(self, file_path: str) -> str:
        return 'checksum'

    def delete_file(self, file_path: str):
        del self.files[file_path]

    def delete_directory_tree(self, directory_path: str):
        del self.files[directory_path]

    def offer_file_download(self, directory: str, file_path: str) -> None:
        return None
