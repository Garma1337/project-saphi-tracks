# coding: utf-8

from flask import Request

from api.auth.permission.permissionresolver import PermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.resource import Resource
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse, ErrorJsonResponse, EmptyResponse
from api.resource.resourcemanager import ResourceManager


class DownloadResource(RequestHandler):

    def __init__(self, entity_manager: EntityManager, resource_manager: ResourceManager, permission_resolver: PermissionResolver):
        self.entity_manager = entity_manager
        self.resource_manager = resource_manager
        self.permission_resolver = permission_resolver

    def handle_request(self, request: Request) -> JsonResponse:
        if not 'id' in request.args:
            return ErrorJsonResponse('You need to provide a resource id')

        resource_id = int(request.args.get('id'))
        resource_repository = self.entity_manager.get_repository(Resource)

        resource = resource_repository.find_one(resource_id)

        if not resource:
            return ErrorJsonResponse('No resource with id {} exists', 404)

        if not self.permission_resolver.can_see_resource(self.get_current_user(), resource):
            return ErrorJsonResponse('You are not allowed to access this resource', 401)

        self.resource_manager.offer_resource_download(resource_id)
        return EmptyResponse()

    def require_authentication(self) -> bool:
        return False
