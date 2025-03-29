# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.model.user import User
from api.ui.displayoptionsgenerator import DisplayOptionsGenerator


class DisplayOptionsGeneratorTest(TestCase):

    def setUp(self):
        self.permission_resolver = LogicalPermissionResolver()
        self.display_options_generator = DisplayOptionsGenerator(self.permission_resolver)

    def test_generate_display_options_for_logged_in_user(self):
        user = User()
        self.permission_resolver.can_verify_custom_track = Mock(return_value=False)

        display_options = self.display_options_generator.generate_display_options_for_user(user)

        self.assertTrue(display_options['show_create_custom_track_button'])
        self.assertFalse(display_options['show_admin_button'])
        self.assertFalse(display_options['show_login_button'])
        self.assertTrue(display_options['show_logout_button'])

    def test_generate_display_options_for_logged_out_user(self):
        display_options = self.display_options_generator.generate_display_options_for_user(None)

        self.assertFalse(display_options['show_create_custom_track_button'])
        self.assertFalse(display_options['show_admin_button'])
        self.assertTrue(display_options['show_login_button'])
        self.assertFalse(display_options['show_logout_button'])

    def test_generate_display_options_for_admin_user(self):
        user = User()
        self.permission_resolver.can_verify_custom_track = Mock(return_value=True)

        display_options = self.display_options_generator.generate_display_options_for_user(user)

        self.assertTrue(display_options['show_create_custom_track_button'])
        self.assertTrue(display_options['show_admin_button'])
        self.assertFalse(display_options['show_login_button'])
        self.assertTrue(display_options['show_logout_button'])
