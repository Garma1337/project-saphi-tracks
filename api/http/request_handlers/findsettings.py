# coding: utf-8

from flask import Request

from api.database.entitymanager import EntityManager
from api.database.model.setting import Setting
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.requesthelper import RequestHelper
from api.http.response import JsonResponse
from api.lib.pagination import Pagination


class FindSettings(RequestHandler):

    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    def handle_request(self, request: Request) -> JsonResponse:
        repository = self.entity_manager.get_repository(Setting)

        filter_args = {
            'id': RequestHelper.try_parse_integer_value(request.args, 'id'),
            'category': request.args.get('category'),
            'key': request.args.get('key'),
        }

        setting_count = repository.count(**filter_args)

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), setting_count)
        settings = repository.find_by(**filter_args, limit=pagination.get_limit(), offset=pagination.get_offset())

        return JsonResponse({
            'pagination': pagination.to_dictionary(),
            'items': [setting.to_dictionary() for setting in settings]
        })

    def require_authentication(self):
        return False
