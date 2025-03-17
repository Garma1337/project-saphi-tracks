# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy


class Sha256FileEncoderStrategyTest(TestCase):

    def setUp(self):
        self.sha256_file_encoder_strategy = Sha256FileEncoderStrategy()
        self.sha256_file_encoder_strategy.get_current_timestamp = Mock(return_value=1742241415)

    def test_encode_file_name(self):
        encoded_resource_target = self.sha256_file_encoder_strategy.encode_file_name('test.txt')

        self.assertEqual('1742241415_test.txt', encoded_resource_target.get_file_name())
        self.assertEqual('cb/e4/61', encoded_resource_target.get_directory_path())
