# coding=utf-8

from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import verify_jwt_in_request

from api.container import container
from api.http.router import RequestMethod

api: Blueprint = Blueprint('api', __name__)

@api.route('/api/v1/<path:route>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def run(route):
    verify_jwt_in_request(optional=True)

    dispatcher = container.get('http.dispatcher')
    dispatcher.router.add_route('customtracks', RequestMethod.GET.value, container.get(f'http.request_handler.find_custom_tracks'))
    dispatcher.router.add_route('permissions', RequestMethod.GET.value, container.get(f'http.request_handler.find_permissions'))
    dispatcher.router.add_route('resources', RequestMethod.GET.value, container.get(f'http.request_handler.find_resources'))
    dispatcher.router.add_route('settings', RequestMethod.GET.value, container.get(f'http.request_handler.find_settings'))
    dispatcher.router.add_route('tags', RequestMethod.GET.value, container.get(f'http.request_handler.find_tags'))
    dispatcher.router.add_route('users', RequestMethod.GET.value, container.get(f'http.request_handler.find_users'))

    response = dispatcher.dispatch_request(route, request)

    return response.get_data(), response.get_status_code()
