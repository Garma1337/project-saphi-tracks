# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.requesthelper import RequestHelper
from api.http.response import JsonResponse, ErrorJsonResponse, SuccessJsonResponse


class UpdateCustomTrack(RequestHandler):

    def __init__(self, entity_manager: EntityManager, permission_resolver: PermissionResolver):
        self.entity_manager = entity_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        if not 'id' in request.json:
            return ErrorJsonResponse('You need to provide a custom track id')

        current_user = self.get_current_user()

        # if a user can verify custom tracks, he can also edit them
        if not self.permission_resolver.can_verify_custom_track(current_user):
            return ErrorJsonResponse('You are not allowed to update custom tracks', 401)

        custom_track_repository = self.entity_manager.get_repository(CustomTrack)

        custom_track_id = int(request.json.get('id'))
        custom_track = custom_track_repository.find_one(custom_track_id)

        if not custom_track:
            return ErrorJsonResponse(f'No custom track with id {custom_track_id} exists', 404)

        highlighted = RequestHelper.try_parse_boolean_value(request.json, 'highlighted')
        custom_track_repository.update(id=custom_track_id, highlighted=highlighted)

        # reload custom track
        custom_track = custom_track_repository.find_one(custom_track_id)

        return SuccessJsonResponse({'custom_track': custom_track.to_dictionary()})

    def require_authentication(self) -> bool:
        return True
