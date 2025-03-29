# coding: utf-8

from unittest import TestCase

from api.lib.semvervalidator import SemVerValidator


class SemverValidatorTest(TestCase):

    def setUp(self):
        self.validator = SemVerValidator()

    def test_should_return_true_if_version_is_valid_semver(self):
        self.assertTrue(self.validator.check_is_valid_semver('1.21.0'))
        self.assertTrue(self.validator.check_is_valid_semver('2.1.23'))
        self.assertTrue(self.validator.check_is_valid_semver('31.2.456'))
        self.assertTrue(self.validator.check_is_valid_semver('315.25.456'))

    def test_should_return_false_if_version_is_not_valid_semver(self):
        self.assertFalse(self.validator.check_is_valid_semver('v1'))
        self.assertFalse(self.validator.check_is_valid_semver('1.21'))
        self.assertFalse(self.validator.check_is_valid_semver('test'))
