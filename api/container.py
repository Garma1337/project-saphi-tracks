# coding: utf-8

from api import db
from api.database.entitymanager import EntityManager
from api.database.repository.modelrepository import ModelRepository
from api.event.eventmanager import EventManager
from api.http.dispatcher import Dispatcher
from api.http.request_handlers.findcustomtracks import FindCustomTracks
from api.http.router import Router
from api.lib.container import Container

container = Container()

def init_app(app):
    # database
    container.register('db', lambda: db)
    container.register('db.repository.model_repository', lambda: ModelRepository(container.get('db')))
    container.register('db.entity_manager', lambda: EntityManager(container.get('db.model_repository')))

    # event system
    container.register('event.event_manager', lambda: EventManager())

    # api http handlers
    container.register('http.router', lambda: Router())
    container.register('http.dispatcher', lambda: Dispatcher(container.get('http.router')))
    container.register('http.request_handler.find_custom_tracks', lambda: FindCustomTracks(container.get('db.entity_manager')))

    # container itself
    container.register('container', lambda: container)

    return container
