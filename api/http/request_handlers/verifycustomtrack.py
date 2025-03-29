# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.auth.sessionmanager import SessionManager
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse, ErrorJsonResponse, SuccessJsonResponse
from api.lib.customtrackmanager import CustomTrackManager, CustomTrackNotFoundError, CustomTrackAlreadyVerifiedError


class VerifyCustomTrack(RequestHandler):

    def __init__(self, session_manager: SessionManager, custom_track_manager: CustomTrackManager, permission_resolver: PermissionResolver):
        self.session_manager = session_manager
        self.custom_track_manager = custom_track_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        if not 'id' in request.json:
            return ErrorJsonResponse('You need to provide a custom track id')

        current_user = self.session_manager.find_user_by_jwt_identity(self.get_current_identity())

        if not self.permission_resolver.can_verify_custom_track(current_user):
            return ErrorJsonResponse('You are not allowed to verify custom tracks', 401)

        custom_track_id = int(request.json.get('id'))

        try:
            custom_track = self.custom_track_manager.verify_custom_track(custom_track_id)
            return SuccessJsonResponse({'custom_track': custom_track.to_dictionary()})
        except CustomTrackNotFoundError as e:
            return ErrorJsonResponse(str(e), 404)
        except CustomTrackAlreadyVerifiedError as e:
            return ErrorJsonResponse(str(e))

    def require_authentication(self) -> bool:
        return True
