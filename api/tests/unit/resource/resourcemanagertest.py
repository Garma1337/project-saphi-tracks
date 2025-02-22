# coding: utf-8

from unittest import TestCase

from api.resource.resourcemanager import ResourceManager


class ResourceManagerTest(TestCase):


    def setUp(self):
        self.resource_manager = ResourceManager()

    def test_can_get_expected_file_extensions(self):
        self.assertEqual(['jpg', 'png'], self.resource_manager.get_expected_file_extensions('preview'))
        self.assertEqual(['xdelta'], self.resource_manager.get_expected_file_extensions('xdelta'))
        self.assertEqual(['vrm'], self.resource_manager.get_expected_file_extensions('vrm'))
        self.assertEqual(['lev'], self.resource_manager.get_expected_file_extensions('lev'))

    def test_can_not_get_expected_file_extensions_for_non_existent_resource_type(self):
        with self.assertRaises(KeyError):
            self.resource_manager.get_expected_file_extensions('non_existent_resource_type')
