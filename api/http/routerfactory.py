# coding: utf-8

from api.http.router import Router, RequestMethod
from api.lib.container import Container


class RouterFactory(object):

    @staticmethod
    def factory(container: Container) -> Router:
        router = Router()
        router.add_route(
            'customtracks',
            RequestMethod.GET.value,
            container.get('http.request_handler.find_custom_tracks')
        )
        router.add_route(
            'dtos',
            RequestMethod.GET.value,
            container.get('http.request_handler.generate_dtos')
        )
        router.add_route(
            'permissions',
            RequestMethod.GET.value,
            container.get('http.request_handler.find_permissions')
        )
        router.add_route(
            'resources',
            RequestMethod.GET.value,
            container.get('http.request_handler.find_resources')
        )
        router.add_route(
            'settings',
            RequestMethod.GET.value,
            container.get('http.request_handler.find_settings')
        )
        router.add_route(
            'tags',
            RequestMethod.GET.value,
            container.get('http.request_handler.find_tags')
        )
        router.add_route(
            'users',
            RequestMethod.GET.value,
            container.get('http.request_handler.find_users')
        )

        return router
