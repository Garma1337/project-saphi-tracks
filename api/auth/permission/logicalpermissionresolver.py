# coding: utf-8

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.model.customtrack import CustomTrack
from api.database.model.resource import Resource
from api.database.model.user import User


class LogicalPermissionResolver(PermissionResolver):

    def can_see_custom_track(self, user: User, custom_track: CustomTrack) -> bool:
        return custom_track.verified or self.can_see_unverified_custom_tracks(user)

    def can_edit_custom_track(self, user: User, custom_track: CustomTrack) -> bool:
        if not user:
            return False

        return custom_track.author_id == user.id or user.permission.can_edit_custom_tracks

    def can_delete_custom_track(self, user: User, custom_track: CustomTrack) -> bool:
        if not user:
            return False

        return user.permission.can_delete_custom_tracks

    def can_see_unverified_custom_tracks(self, user: User) -> bool:
        if not user:
            return False

        return user.permission.can_edit_custom_tracks

    def can_see_resource(self, user: User, resource: Resource) -> bool:
        return resource.verified or self.can_see_unverified_resources(user)

    def can_edit_resource(self, user: User, resource: Resource) -> bool:
        if not user:
            return False

        return user.permission.can_edit_resources

    def can_delete_resource(self, user: User, resource: Resource) -> bool:
        if not user:
            return False

        return user.permission.can_delete_resources

    def can_see_unverified_resources(self, user: User) -> bool:
        if not user:
            return False

        return user.permission.can_edit_resources

    def can_see_user(self, user: User, target_user: User) -> bool:
        return target_user.verified or self.can_see_unverified_users(user)

    def can_edit_user(self, user: User, target_user: User) -> bool:
        if not user:
            return False

        return user.id == target_user.id or user.permission.can_edit_users

    def can_see_unverified_users(self, user: User) -> bool:
        if not user:
            return False

        return user.permission.can_edit_users
