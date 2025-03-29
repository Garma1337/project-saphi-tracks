# coding: utf-8

from api.auth.permission.permissionresolver import PermissionResolver
from api.auth.sessionmanager import SessionManager
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import ErrorJsonResponse, SuccessJsonResponse, JsonResponse
from api.resource.resourcemanager import ResourceManager, ResourceNotFoundError, ResourceAlreadyVerifiedError


class VerifyResource(RequestHandler):

    def __init__(self, session_manager: SessionManager, resource_manager: ResourceManager, permission_resolver: PermissionResolver):
        self.session_manager = session_manager
        self.resource_manager = resource_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request) -> JsonResponse:
        if not 'id' in request.json:
            return ErrorJsonResponse('You need to provide a resource id')

        current_user = self.session_manager.find_user_by_jwt_identity(self.get_current_identity())

        if not self.permission_resolver.can_verify_resource(current_user):
            return ErrorJsonResponse('You are not allowed to verify resources', 401)

        resource_id = int(request.json.get('id'))

        try:
            resource = self.resource_manager.verify_resource(resource_id)
            return SuccessJsonResponse({'resource': resource.to_dictionary()})
        except ResourceNotFoundError as e:
            return ErrorJsonResponse(str(e), 404)
        except ResourceAlreadyVerifiedError as e:
            return ErrorJsonResponse(str(e))

    def require_authentication(self) -> bool:
        return True
