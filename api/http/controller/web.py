# coding: utf-8

import os

from flask import Blueprint

web_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'web')
web = Blueprint('web', __name__, static_folder=web_directory, static_url_path='/')

@web.route('/', defaults={'path': ''})
@web.route('/<path:path>')
def run(path):
    return web.send_static_file('index.html')
