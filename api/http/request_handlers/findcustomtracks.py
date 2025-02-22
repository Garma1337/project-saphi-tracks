# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse
from api.lib.pagination import Pagination


class FindCustomTracks(RequestHandler):

    def __init__(self, entity_manager: EntityManager, permission_resolver: PermissionResolver):
        self.entity_manager = entity_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        repository = self.entity_manager.get_repository(CustomTrack)

        highlighted = self.get_boolean_query_parameter(request, 'highlighted')
        verified = self.get_boolean_query_parameter(request, 'verified')

        filter_args = {
            'id': request.args.get('id'),
            'author_id': request.args.get('author_id'),
            'name': request.args.get('name'),
            'highlighted': highlighted,
            'verified': verified,
        }

        custom_track_count = repository.count(**filter_args)

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), custom_track_count)
        custom_tracks = repository.find_by(**filter_args, limit=pagination.get_limit(), offset=pagination.get_offset())

        return JsonResponse({
            'pagination': pagination.to_dictionary(),
            'items': [custom_track.to_dictionary() for custom_track in custom_tracks]
        })

    def require_authentication(self) -> bool:
        return False
