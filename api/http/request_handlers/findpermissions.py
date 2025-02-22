# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse
from api.lib.pagination import Pagination


class FindPermissions(RequestHandler):

    def __init__(self, entity_manager: EntityManager, permission_resolver: PermissionResolver):
        self.entity_manager = entity_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        repository = self.entity_manager.get_repository(Permission)

        filter_args = {
            'id': request.args.get('id'),
            'user_id': request.args.get('user_id'),
        }

        permission_count = repository.count(**filter_args)

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), permission_count)
        permissions = repository.find_by(**filter_args, limit=pagination.get_limit(), offset=pagination.get_offset())

        return JsonResponse({
            'pagination': pagination.to_dictionary(),
            'items': [permission.to_dictionary() for permission in permissions]
        })

    def require_authentication(self):
        return False
