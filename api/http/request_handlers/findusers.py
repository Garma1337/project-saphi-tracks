# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.requesthelper import RequestHelper
from api.http.response import JsonResponse
from api.lib.pagination import Pagination


class FindUsers(RequestHandler):

    def __init__(self, entity_manager: EntityManager, permission_resolver: PermissionResolver):
        self.entity_manager = entity_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        repository = self.entity_manager.get_repository(User)

        verified = RequestHelper.try_parse_boolean_value(request.args, 'verified')

        filter_args = {
            'id': RequestHelper.try_parse_integer_value(request.args, 'id'),
            'username': request.args.get('username'),
            'verified': verified,
        }

        user_count = repository.count(**filter_args)

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), user_count)
        users = repository.find_by(**filter_args, limit=pagination.get_limit(), offset=pagination.get_offset())

        return JsonResponse({
            'pagination': pagination.to_dictionary(),
            'items': [user.to_dictionary() for user in users]
        })

    def require_authentication(self) -> bool:
        return False
