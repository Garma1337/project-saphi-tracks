# coding: utf-8

from flask import Request

from api.auth.sessionmanager import SessionManager
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse, SuccessJsonResponse, ErrorJsonResponse
from api.services.customtrackmanager import CustomTrackManager
from api.resource.resourcemanager import ResourceCreationError


class CreateCustomTrack(RequestHandler):

    def __init__(self, session_manager: SessionManager, custom_track_manager: CustomTrackManager):
        self.session_manager = session_manager
        self.custom_track_manager = custom_track_manager

    def handle_request(self, request: Request) -> JsonResponse:
        required_form_fields = [
            'name',
            'description',
            'video',
            'lev_file_version',
            'vrm_file_version'
        ]

        for field in required_form_fields:
            if not field in request.form:
                return ErrorJsonResponse(f'Required form field "{field}" is missing')

            if not request.form[field]:
                return ErrorJsonResponse(f'Required form field "{field}" is empty')

        required_file_fields = [
            'preview_image',
            'lev_file',
            'vrm_file'
        ]

        for field in required_file_fields:
            if not field in request.files:
                return ErrorJsonResponse(f'Required file "{field}" is missing')

            if not request.files[field]:
                return ErrorJsonResponse(f'Required file "{field}" is missing')

        current_user = self.session_manager.find_user_by_jwt_identity(self.get_current_identity())
        user_dict = current_user.to_dictionary()

        try:
            custom_track = self.custom_track_manager.create_custom_track(
                author_id=user_dict['id'],
                name=request.form.get('name'),
                description=request.form.get('description'),
                video=request.form.get('video'),
                preview_image=request.files.get('preview_image'),
                lev_file=request.files.get('lev_file'),
                lev_file_version=request.form.get('lev_file_version'),
                vrm_file=request.files.get('vrm_file'),
                vrm_file_version=request.form.get('vrm_file_version')
            )

            return SuccessJsonResponse({'custom_track': custom_track.to_dictionary()})
        except ResourceCreationError as e:
            return ErrorJsonResponse(str(e))

    def require_authentication(self) -> bool:
        return True
