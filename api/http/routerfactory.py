# coding: utf-8

from api.di.transientcontainer import TransientContainer
from api.http.router import Router


class RouterFactory(object):

    @staticmethod
    def factory(container: TransientContainer) -> Router:
        router = Router()

        # GET Endpoints
        router.add_route('customtracks', 'GET', container.get('http.request_handler.find_custom_tracks'))
        router.add_route('discordstatus', 'GET', container.get('http.request_handler.get_discord_status'))
        router.add_route('dtos', 'GET', container.get('http.request_handler.generate_dtos'))
        router.add_route('permissions', 'GET', container.get('http.request_handler.find_permissions'))
        router.add_route('resources', 'GET', container.get('http.request_handler.find_resources'))
        router.add_route('session', 'GET', container.get('http.request_handler.get_session'))
        router.add_route('settings', 'GET', container.get('http.request_handler.find_settings'))
        router.add_route('tags', 'GET', container.get('http.request_handler.find_tags'))
        router.add_route('users', 'GET', container.get('http.request_handler.find_users'))

        # POST Endpoints
        router.add_route('customtracks', 'POST', container.get('http.request_handler.create_custom_track'))
        router.add_route('customtracks/verify', 'POST', container.get('http.request_handler.verify_custom_track'))
        router.add_route('login', 'POST', container.get('http.request_handler.login_user'))
        router.add_route('resources/verify', 'POST', container.get('http.request_handler.verify_resource'))

        # PATCH Endpoints
        router.add_route('customtracks', 'PATCH', container.get('http.request_handler.update_custom_track'))

        # DELETE Endpoints
        router.add_route('customtracks', 'DELETE', container.get('http.request_handler.delete_custom_track'))

        return router
