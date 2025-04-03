# coding=utf-8

import os


class FileSystemHelper(object):

    @staticmethod
    def get_current_directory() -> str:
        return os.path.dirname(os.path.realpath(__file__))
