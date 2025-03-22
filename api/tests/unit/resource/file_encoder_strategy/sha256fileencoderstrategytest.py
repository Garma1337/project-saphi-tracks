# coding: utf-8

from unittest import TestCase

from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy


class Sha256FileEncoderStrategyTest(TestCase):

    def setUp(self):
        self.sha256_file_encoder_strategy = Sha256FileEncoderStrategy()

    def test_encode_file_name(self):
        encoded_resource_target = self.sha256_file_encoder_strategy.encode_file_name('test.txt')

        self.assertEqual('test.txt', encoded_resource_target.get_file_name())
        self.assertEqual('a6/ed/0c', encoded_resource_target.get_directory_path())
