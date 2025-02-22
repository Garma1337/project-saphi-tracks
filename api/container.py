# coding: utf-8

from api import db
from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.databasemanager import DatabaseManager
from api.database.dto_generator.dtogeneratorservicefactory import DTOGeneratorServiceFactory
from api.database.dto_generator.htmlcodeformatter import HtmlCodeFormatter
from api.database.entitymanager import EntityManager
from api.database.repository.modelrepository import ModelRepository
from api.event.eventmanager import EventManager
from api.faker.fakerservice import FakerService
from api.http.dispatcher import Dispatcher
from api.http.request_handlers.findcustomtracks import FindCustomTracks
from api.http.request_handlers.findpermissions import FindPermissions
from api.http.request_handlers.findresources import FindResources
from api.http.request_handlers.findsettings import FindSettings
from api.http.request_handlers.findtags import FindTags
from api.http.request_handlers.findusers import FindUsers
from api.http.request_handlers.generatedtos import GenerateDTOs
from api.http.routerfactory import RouterFactory
from api.lib.container import Container
from api.resource.resourcemanager import ResourceManager

container = Container()

def init_app(app):
    # Auth
    container.register('auth.permission.permission_resolver', lambda: LogicalPermissionResolver())

    # Database
    container.register('db.database_manager', lambda: DatabaseManager(db, app.config))
    container.register('db.entity_manager', lambda: EntityManager(db, ModelRepository))
    container.register('db.dto_generator.dto_generator_service', lambda: DTOGeneratorServiceFactory.factory())
    container.register('db.dto_generator.html_code_formatter', lambda: HtmlCodeFormatter())

    # Event System
    container.register('event.event_manager', lambda: EventManager())

    # Faker
    container.register('faker.faker_service', lambda: FakerService(container.get('db.entity_manager'), container.get('resources.resource_manager')))

    # REST API
    container.register('http.router', lambda: RouterFactory.factory(container.get('container')))
    container.register('http.dispatcher', lambda: Dispatcher(container.get('http.router')))

    # HTTP Request Handlers
    container.register('http.request_handler.find_custom_tracks', lambda: FindCustomTracks(
        container.get('db.entity_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.generate_dtos', lambda: GenerateDTOs(
        container.get('db.dto_generator.dto_generator_service'),
        container.get('db.dto_generator.html_code_formatter')
    ))
    container.register('http.request_handler.find_permissions', lambda: FindPermissions(
        container.get('db.entity_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.find_resources', lambda: FindResources(
        container.get('db.entity_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.find_settings', lambda: FindSettings(container.get('db.entity_manager')))
    container.register('http.request_handler.find_tags', lambda: FindTags(container.get('db.entity_manager')))
    container.register('http.request_handler.find_users', lambda: FindUsers(
        container.get('db.entity_manager'),
        container.get('auth.permission.permission_resolver')
    ))

    # Resources
    container.register('resources.resource_manager', lambda: ResourceManager())

    # Container itself
    container.register('container', lambda: container)

    return container
