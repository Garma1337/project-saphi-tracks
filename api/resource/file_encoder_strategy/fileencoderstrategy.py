# coding: utf-8

from abc import ABC, abstractmethod


class EncodedResourceTarget(object):

    def __init__(self, file_name: str, directory_path: str):
        self.file_name = file_name
        self.directory_path = directory_path

    def get_file_name(self) -> str:
        return self.file_name

    def get_directory_path(self) -> str:
        return self.directory_path


class FileEncoderStrategy(ABC):

    @abstractmethod
    def encode_file_name(self, file_name: str) -> EncodedResourceTarget:
        pass
