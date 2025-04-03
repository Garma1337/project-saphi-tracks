# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.database.model.resource import Resource
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.requesthelper import RequestHelper
from api.http.response import JsonResponse
from api.util.pagination import Pagination


class FindResources(RequestHandler):

    def __init__(self, entity_manager: EntityManager, session_manager: SessionManager, permission_resolver: PermissionResolver):
        self.entity_manager = entity_manager
        self.session_manager = session_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        repository = self.entity_manager.get_repository(Resource)

        verified = RequestHelper.try_parse_boolean_value(request.args, 'verified')

        current_user = self.session_manager.find_user_by_jwt_identity(self.get_current_identity())
        if not self.permission_resolver.can_see_unverified_resources(current_user):
            verified = True

        filter_args = {
            'id': RequestHelper.try_parse_integer_value(request.args, 'id'),
            'author_id': RequestHelper.try_parse_integer_value(request.args, 'author_id'),
            'custom_track_id': RequestHelper.try_parse_integer_value(request.args, 'custom_track_id'),
            'file_name': request.args.get('file_name'),
            'resource_type': request.args.get('resource_type'),
            'verified': verified,
        }

        resource_count = repository.count(**filter_args)

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), resource_count)
        resources = repository.find_by(**filter_args, limit=pagination.get_limit(), offset=pagination.get_offset())

        return JsonResponse({
            'pagination': pagination.to_dictionary(),
            'items': [resource.to_dictionary() for resource in resources]
        })

    def require_authentication(self) -> bool:
        return False
