# coding: utf-8

from unittest import TestCase

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.http.request_handlers.findpermissions import FindPermissions
from api.tests.mockmodelrepository import MockModelRepository


class FindPermissionsTest(TestCase):

    def setUp(self):
        self.permission_repository = MockModelRepository(Permission)

        for i in range(1, 3):
            self.permission_repository.create(
                id=i,
                user_id=i,
                can_edit_custom_tracks=i % 2,
                can_delete_custom_tracks=i % 2,
                can_edit_resources=i % 2,
                can_delete_resources=i % 2,
                can_edit_users=i % 2,
            )

        self.find_permissions = FindPermissions(
            EntityManager(
                SQLAlchemy(),
                MockModelRepository
            ),
            LogicalPermissionResolver()
        )

        self.find_permissions.entity_manager.get_repository = lambda model: self.permission_repository

    def test_can_find_permissions(self):
        response = self.find_permissions.handle_request(Request.from_values())
        data = response.get_data()

        permissions = data['items']
        pagination = data['pagination']

        self.assertEqual(len(permissions), 2)
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['items_per_page'], 20)
        self.assertEqual(pagination['total_item_count'], 2)

        self.assertEqual(permissions[0]['id'], 1)
        self.assertEqual(permissions[0]['user_id'], 1)
        self.assertEqual(permissions[0]['can_edit_custom_tracks'], 1)
        self.assertEqual(permissions[0]['can_delete_custom_tracks'], 1)
        self.assertEqual(permissions[0]['can_edit_resources'], 1)
        self.assertEqual(permissions[0]['can_delete_resources'], 1)
        self.assertEqual(permissions[0]['can_edit_users'], 1)

        self.assertEqual(permissions[1]['id'], 2)
        self.assertEqual(permissions[1]['user_id'], 2)
        self.assertEqual(permissions[1]['can_edit_custom_tracks'], 0)
        self.assertEqual(permissions[1]['can_delete_custom_tracks'], 0)
        self.assertEqual(permissions[1]['can_edit_resources'], 0)
        self.assertEqual(permissions[1]['can_delete_resources'], 0)
        self.assertEqual(permissions[1]['can_edit_users'], 0)

    def test_can_find_permissions_by_id(self):
        response = self.find_permissions.handle_request(Request.from_values(query_string='id=1'))
        data = response.get_data()

        permissions = data['items']
        pagination = data['pagination']

        self.assertEqual(len(permissions), 1)
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['items_per_page'], 20)
        self.assertEqual(pagination['total_item_count'], 1)

        self.assertEqual(permissions[0]['id'], 1)
        self.assertEqual(permissions[0]['user_id'], 1)
        self.assertEqual(permissions[0]['can_edit_custom_tracks'], 1)
        self.assertEqual(permissions[0]['can_delete_custom_tracks'], 1)
        self.assertEqual(permissions[0]['can_edit_resources'], 1)
        self.assertEqual(permissions[0]['can_delete_resources'], 1)
        self.assertEqual(permissions[0]['can_edit_users'], 1)

    def test_can_find_permissions_by_user_id(self):
        response = self.find_permissions.handle_request(Request.from_values(query_string='user_id=1'))
        data = response.get_data()

        permissions = data['items']
        pagination = data['pagination']

        self.assertEqual(len(permissions), 1)
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['items_per_page'], 20)
        self.assertEqual(pagination['total_item_count'], 1)

        self.assertEqual(permissions[0]['id'], 1)
        self.assertEqual(permissions[0]['user_id'], 1)
        self.assertEqual(permissions[0]['can_edit_custom_tracks'], 1)
        self.assertEqual(permissions[0]['can_delete_custom_tracks'], 1)
        self.assertEqual(permissions[0]['can_edit_resources'], 1)
        self.assertEqual(permissions[0]['can_delete_resources'], 1)
        self.assertEqual(permissions[0]['can_edit_users'], 1)
