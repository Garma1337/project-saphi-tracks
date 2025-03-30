# coding: utf-8

import os

from flask import Blueprint

from api.container import container
from api.resource.resourcemanager import ResourceManager

resource_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'resources')
rproxy = Blueprint('resource', __name__, static_folder=resource_directory, static_url_path='/')

@rproxy.route('/rproxy/', defaults={'file_name': ''})
@rproxy.route('/rproxy/<path:file_name>')
def run(file_name):
    resource_manager = container.get('resource.resource_manager') # type: ResourceManager
    local_path = resource_manager.get_local_path(file_name)

    return rproxy.send_static_file(local_path)
