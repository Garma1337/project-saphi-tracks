# coding: utf-8

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

    def get_full_path(self, file_path: str) -> str:
        return file_path

    def file_exists(self, file_path: str) -> bool:
        return file_path in self.files

    def read_file(self, file_path: str) -> str:
        if not self.file_exists(file_path):
            raise FileNotReadableError('File {} does not exist'.format(file_path))

        return self.files[file_path]

    def write_file(self, file_path: str, content: str) -> bool:
        self.files[file_path] = content
        return True

    def delete_file(self, file_path: str):
        del self.files[file_path]

    def delete_directory_tree(self, directory_path: str):
        del self.directories[directory_path]
