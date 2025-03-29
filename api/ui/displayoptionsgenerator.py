# coding: utf-8

from typing import Optional

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.model.user import User


class DisplayOptionsGenerator(object):

    def __init__(self, permission_resolver: PermissionResolver):
        self.permission_resolver = permission_resolver

    def generate_display_options_for_user(self, user: Optional[User]) -> dict[str, bool]:
        display_options = {
            'show_create_custom_track_button': user is not None,
            'show_admin_button': self.permission_resolver.can_verify_custom_track(user),
            'show_login_button': user is None,
            'show_logout_button': user is not None
        }

        return display_options
