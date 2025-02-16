# coding: utf-8

from flask import Request

from api.database.entitymanager import EntityManager
from api.database.model.tag import Tag
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import Response
from api.lib.pagination import Pagination


class FindTags(RequestHandler):

    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    def handle_request(self, request: Request) -> Response:
        repository = self.entity_manager.get_repository(Tag)

        filter_args = {
            'id': request.args.get('id'),
            'name': request.args.get('name'),
        }

        tag_count = repository.count(**filter_args)

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), tag_count)
        tags = repository.find_by(**filter_args, limit=pagination.get_limit(), offset=pagination.get_offset())

        return Response({
            'pagination': pagination.to_dictionary(),
            'items': [tag.to_dictionary() for tag in tags]
        })

    def require_authentication(self):
        return False
