# coding=utf-8

from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import verify_jwt_in_request

from api.container import container

api: Blueprint = Blueprint('api', __name__)

@api.route('/api/v1/<path:route>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@cross_origin()
def run(route):
    verify_jwt_in_request(optional=True)

    dispatcher = container.get('http.dispatcher')
    response = dispatcher.dispatch_request(route, request)

    return response.get_data(), response.get_status_code()
