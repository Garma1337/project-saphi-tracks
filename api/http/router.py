# coding: utf-8

from enum import Enum
from typing import Optional

from api.http.request_handlers.requesthandler import RequestHandler


class RequestMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Router(object):

    def __init__(self):
        self.routes = {}

    def add_route(self, path: str, method: str, handler: RequestHandler):
        if not path in self.routes:
            self.routes[path] = {}

        if self.has_request_handler(path, method):
            raise ValueError(f'Route {path} already has a handler for method {method}')

        self.routes[path][method] = handler

    def get_request_handler_for_route(self, path: str, method: str) -> Optional[RequestHandler]:
        if not path in self.routes:
            return None

        if not method in self.routes[path]:
            return None

        return self.routes[path][method]

    def has_request_handler(self, path: str, method: str) -> bool:
        return self.get_request_handler_for_route(path, method) is not None

    def remove_route(self, path: str, method: str):
        if not path in self.routes:
            return

        if not method in self.routes[path]:
            return

        del self.routes[path][method]
