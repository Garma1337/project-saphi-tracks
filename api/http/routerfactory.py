# coding: utf-8

from api.http.router import Router
from api.lib.container import Container


class RouterFactory(object):

    @staticmethod
    def factory(container: Container) -> Router:
        router = Router()

        # GET Endpoints
        router.add_route('customtracks', 'GET', container.get('http.request_handler.find_custom_tracks'))
        router.add_route('dtos', 'GET', container.get('http.request_handler.generate_dtos'))
        router.add_route('permissions', 'GET', container.get('http.request_handler.find_permissions'))
        router.add_route('resources', 'GET', container.get('http.request_handler.find_resources'))
        router.add_route('session', 'GET', container.get('http.request_handler.get_session'))
        router.add_route('settings', 'GET', container.get('http.request_handler.find_settings'))
        router.add_route('tags', 'GET', container.get('http.request_handler.find_tags'))
        router.add_route('users', 'GET', container.get('http.request_handler.find_users'))

        # POST Endpoints
        router.add_route('customtracks', 'POST', container.get('http.request_handler.create_custom_track'))
        router.add_route('login', 'POST', container.get('http.request_handler.login_user'))

        return router
