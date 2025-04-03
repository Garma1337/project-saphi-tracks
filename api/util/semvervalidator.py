# coding: utf-8

import re


class SemVerValidator(object):

    def __init__(self):
        self.version_regex = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')

    def check_is_valid_semver(self, version: str) -> bool:
        return self.version_regex.match(version) is not None
