# coding: utf-8

import os.path
from unittest import TestCase

from api.resource.file_system_adapter.localfilesystemadapter import LocalFileSystemAdapter


class LocalFileSystemAdapterTest(TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(__file__)
        self.file_system_adapter = LocalFileSystemAdapter(self.current_directory)

    def tearDown(self):
        self.file_system_adapter.delete_file('test.txt')
        self.file_system_adapter.delete_directory_tree('test/')

    def test_can_create_directory(self):
        self.file_system_adapter.create_directory('test/test')
        self.assertTrue(self.file_system_adapter.file_exists('test/test'))

    def test_can_check_if_file_is_readable(self):
        self.file_system_adapter.write_file('test.txt', 'test')

        self.assertTrue(self.file_system_adapter.is_readable(__file__))
        self.assertTrue(self.file_system_adapter.is_readable('test.txt'))

    def test_can_not_check_if_not_existing_file_is_readable(self):
        self.assertFalse(self.file_system_adapter.is_readable('test.txt'))

    def test_can_check_if_file_is_writable(self):
        self.file_system_adapter.write_file('test.txt', 'test')

        self.assertTrue(self.file_system_adapter.is_writable('test.txt'))

    def test_can_not_check_if_not_existing_file_is_writable(self):
        self.assertFalse(self.file_system_adapter.is_writable('test.txt'))

    def test_can_check_if_file_exists(self):
        self.file_system_adapter.write_file('test.txt', 'test')

        self.assertTrue(self.file_system_adapter.file_exists('test.txt'))

    def test_can_check_if_file_does_not_exist(self):
        self.file_system_adapter.delete_file('test.txt')
        self.assertFalse(self.file_system_adapter.file_exists('test.txt'))

    def test_can_read_file(self):
        self.file_system_adapter.write_file('test.txt', 'test')

        self.assertEqual('test', self.file_system_adapter.read_file('test.txt'))

    def test_can_not_read_not_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.file_system_adapter.read_file('test.txt')

    def test_can_write_file(self):
        self.file_system_adapter.write_file('test.txt', 'test2')

        self.assertEqual('test2', self.file_system_adapter.read_file('test.txt'))

    def test_can_delete_file(self):
        self.file_system_adapter.write_file('test.txt', 'test')
        self.file_system_adapter.delete_file('test.txt')

        self.assertFalse(self.file_system_adapter.file_exists('test.txt'))

    def test_can_not_delete_not_existing_file(self):
        self.file_system_adapter.delete_file('test.txt')

    def test_can_delete_directory_tree(self):
        self.file_system_adapter.create_directory('test/test')
        self.file_system_adapter.write_file('test/test/test.txt', 'test')

        self.file_system_adapter.delete_directory_tree('test/')

        self.assertFalse(self.file_system_adapter.file_exists('test/test/test.txt'))
        self.assertFalse(self.file_system_adapter.file_exists('test/test'))
        self.assertFalse(self.file_system_adapter.file_exists('test'))

    def test_can_not_delete_not_existing_directory_tree(self):
        self.file_system_adapter.delete_directory_tree('test/')

        self.assertFalse(self.file_system_adapter.file_exists('test/'))
        self.assertFalse(self.file_system_adapter.file_exists('test'))
