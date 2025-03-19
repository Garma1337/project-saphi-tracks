# coding: utf-8

from unittest import TestCase

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.model.customtrack import CustomTrack
from api.database.model.permission import Permission
from api.database.model.resource import Resource
from api.database.model.user import User


class LogicalPermissionResolverTest(TestCase):

    def setUp(self):
        self.logical_permission_resolver = LogicalPermissionResolver()

    def test_can_see_custom_track_when_custom_track_is_verified(self):
        user = User()

        custom_track = CustomTrack()
        custom_track.verified = True

        self.assertTrue(self.logical_permission_resolver.can_see_custom_track(user, custom_track))

    def test_can_see_custom_track_when_user_can_see_unverified_custom_tracks(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = True

        custom_track = CustomTrack()
        custom_track.verified = False

        self.assertTrue(self.logical_permission_resolver.can_see_custom_track(user, custom_track))

    def test_can_not_see_custom_track_when_custom_track_is_not_verified_and_user_cannot_see_unverified_custom_tracks(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = False

        custom_track = CustomTrack()
        custom_track.verified = False

        self.assertFalse(self.logical_permission_resolver.can_see_custom_track(user, custom_track))

    def test_can_edit_custom_track_when_user_is_author(self):
        user = User()
        user.id = 1
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = False

        custom_track = CustomTrack()
        custom_track.author_id = 1

        self.assertTrue(self.logical_permission_resolver.can_edit_custom_track(user, custom_track))

    def test_can_edit_custom_track_when_user_can_edit_custom_tracks(self):
        user = User()
        user.id = 1
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = True

        custom_track = CustomTrack()
        custom_track.author_id = 2

        self.assertTrue(self.logical_permission_resolver.can_edit_custom_track(user, custom_track))

    def test_can_not_edit_custom_track_when_user_cannot_edit_custom_tracks_and_is_not_author(self):
        user = User()
        user.id = 1
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = False

        custom_track = CustomTrack()
        custom_track.author_id = 2

        self.assertFalse(self.logical_permission_resolver.can_edit_custom_track(user, custom_track))

    def test_can_not_edit_custom_track_when_user_is_not_authenticated(self):
        user = None
        custom_track = CustomTrack()

        self.assertFalse(self.logical_permission_resolver.can_edit_custom_track(user, custom_track))

    def test_can_delete_custom_track_when_user_can_delete_custom_tracks(self):
        user = User()
        user.permission = Permission()
        user.permission.can_delete_custom_tracks = True

        custom_track = CustomTrack()

        self.assertTrue(self.logical_permission_resolver.can_delete_custom_track(user, custom_track))

    def test_can_not_delete_custom_track_when_user_cannot_delete_custom_tracks(self):
        user = User()
        user.permission = Permission()
        user.permission.can_delete_custom_tracks = False

        custom_track = CustomTrack()

        self.assertFalse(self.logical_permission_resolver.can_delete_custom_track(user, custom_track))

    def test_can_not_delete_custom_track_when_user_is_not_authenticated(self):
        user = None
        custom_track = CustomTrack()

        self.assertFalse(self.logical_permission_resolver.can_delete_custom_track(user, custom_track))

    def test_can_see_unverified_custom_tracks_when_user_can_edit_custom_tracks(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = True

        self.assertTrue(self.logical_permission_resolver.can_see_unverified_custom_tracks(user))

    def test_can_not_see_unverified_custom_tracks_when_user_cannot_edit_custom_tracks(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_custom_tracks = False

        self.assertFalse(self.logical_permission_resolver.can_see_unverified_custom_tracks(user))

    def test_can_see_resource_when_resource_is_verified(self):
        user = User()

        resource = Resource()
        resource.verified = True

        self.assertTrue(self.logical_permission_resolver.can_see_resource(user, resource))

    def test_can_see_resource_when_user_can_see_unverified_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_resources = True

        resource = Resource()
        resource.verified = False

        self.assertTrue(self.logical_permission_resolver.can_see_resource(user, resource))

    def test_can_not_see_resource_when_resource_is_not_verified_and_user_cannot_see_unverified_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_resources = False

        resource = Resource()
        resource.verified = False

        self.assertFalse(self.logical_permission_resolver.can_see_resource(user, resource))

    def test_can_edit_resource_when_user_can_edit_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_resources = True

        resource = Resource()

        self.assertTrue(self.logical_permission_resolver.can_edit_resource(user, resource))

    def test_can_not_edit_resource_when_user_cannot_edit_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_resources = False

        resource = Resource()

        self.assertFalse(self.logical_permission_resolver.can_edit_resource(user, resource))

    def test_can_not_edit_resource_when_user_is_not_authenticated(self):
        user = None
        resource = Resource()

        self.assertFalse(self.logical_permission_resolver.can_edit_resource(user, resource))

    def test_can_delete_resource_when_user_can_delete_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_delete_resources = True

        resource = Resource()

        self.assertTrue(self.logical_permission_resolver.can_delete_resource(user, resource))

    def test_can_not_delete_resource_when_user_cannot_delete_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_delete_resources = False

        resource = Resource()

        self.assertFalse(self.logical_permission_resolver.can_delete_resource(user, resource))

    def test_can_not_delete_resource_when_user_is_not_authenticated(self):
        user = None
        resource = Resource()

        self.assertFalse(self.logical_permission_resolver.can_delete_resource(user, resource))

    def test_can_see_unverified_resources_when_user_can_edit_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_resources = True

        self.assertTrue(self.logical_permission_resolver.can_see_unverified_resources(user))

    def test_can_not_see_unverified_resources_when_user_cannot_edit_resources(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_resources = False

        self.assertFalse(self.logical_permission_resolver.can_see_unverified_resources(user))

    def test_can_see_user_when_user_is_verified(self):
        user = User()

        target_user = User()
        target_user.verified = True

        self.assertTrue(self.logical_permission_resolver.can_see_user(user, target_user))

    def test_can_see_user_when_user_can_see_unverified_users(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_users = True

        target_user = User()
        target_user.verified = False

        self.assertTrue(self.logical_permission_resolver.can_see_user(user, target_user))

    def test_can_not_see_user_when_user_is_not_verified_and_user_cannot_see_unverified_users(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_users = False

        target_user = User()
        target_user.verified = False

        self.assertFalse(self.logical_permission_resolver.can_see_user(user, target_user))

    def test_can_edit_user_when_user_is_target_user(self):
        user = User()
        user.id = 1
        user.permission = Permission()
        user.permission.can_edit_users = False

        target_user = User()
        target_user.id = 1

        self.assertTrue(self.logical_permission_resolver.can_edit_user(user, target_user))

    def test_can_edit_user_when_user_can_edit_users(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_users = True

        target_user = User()

        self.assertTrue(self.logical_permission_resolver.can_edit_user(user, target_user))

    def test_can_not_edit_user_when_user_cannot_edit_users_and_is_not_target_user(self):
        user = User()
        user.id = 1
        user.permission = Permission()
        user.permission.can_edit_users = False

        target_user = User()
        target_user.id = 2

        self.assertFalse(self.logical_permission_resolver.can_edit_user(user, target_user))

    def test_can_not_edit_user_when_user_is_not_authenticated(self):
        user = None
        target_user = User()

        self.assertFalse(self.logical_permission_resolver.can_edit_user(user, target_user))

    def test_can_see_unverified_users_when_user_can_edit_users(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_users = True

        self.assertTrue(self.logical_permission_resolver.can_see_unverified_users(user))

    def test_can_not_see_unverified_users_when_user_cannot_edit_users(self):
        user = User()
        user.permission = Permission()
        user.permission.can_edit_users = False

        self.assertFalse(self.logical_permission_resolver.can_see_unverified_users(user))
