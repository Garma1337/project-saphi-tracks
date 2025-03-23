# coding: utf-8

import os

from api import db
from api.auth.authenticator import Authenticator
from api.auth.password_encoder_strategy.bcryptpasswordencoderstrategy import BcryptPasswordEncoderStrategy
from api.auth.passwordmanager import PasswordManager
from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.auth.user_adapter.localuseradapter import LocalUserAdapter
from api.auth.user_adapter.saphiuseradapter import SaphiUserAdapter
from api.database.databasemanager import DatabaseManager
from api.database.dto_generator.dtogeneratorservicefactory import DTOGeneratorServiceFactory
from api.database.dto_generator.htmlcodeformatter import HtmlCodeFormatter
from api.database.entitymanager import EntityManager
from api.database.repository.modelrepository import ModelRepository
from api.event.eventmanagerfactory import EventManagerFactory
from api.event.subscribers.saphiloginsuccessfuleventsubscriber import SaphiLoginSuccessfulEventSubscriber
from api.faker.fakerservice import FakerService
from api.http.dispatcher import Dispatcher
from api.http.request_handlers.createcustomtrack import CreateCustomTrack
from api.http.request_handlers.downloadresource import DownloadResource
from api.http.request_handlers.findcustomtracks import FindCustomTracks
from api.http.request_handlers.findpermissions import FindPermissions
from api.http.request_handlers.findresources import FindResources
from api.http.request_handlers.findsettings import FindSettings
from api.http.request_handlers.findtags import FindTags
from api.http.request_handlers.findusers import FindUsers
from api.http.request_handlers.generatedtos import GenerateDTOs
from api.http.request_handlers.getsession import GetSession
from api.http.request_handlers.loginuser import LoginUser
from api.http.request_handlers.updatecustomtrack import UpdateCustomTrack
from api.http.request_handlers.verifycustomtrack import VerifyCustomTrack
from api.http.request_handlers.verifyresource import VerifyResource
from api.http.routerfactory import RouterFactory
from api.lib.container import Container
from api.lib.customtrackmanager import CustomTrackManager
from api.lib.saphiclient import SaphiClient
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.file_system_adapter.localfilesystemadapter import LocalFileSystemAdapter
from api.resource.resourcemanager import ResourceManager

container = Container()
current_directory = os.path.abspath(os.path.dirname(__file__))

def init_app(app):
    # Auth
    container.register('auth.user_adapter.local', lambda: LocalUserAdapter(container.get('db.entity_manager'), container.get('auth.password_manager')))
    container.register('auth.user_adapter.saphi', lambda: SaphiUserAdapter(
        container.get('event.event_manager'),
        container.get('db.entity_manager'),
        container.get('auth.password_manager'),
        container.get('saphi_client')
    ))

    container.register('auth.permission.permission_resolver', lambda: LogicalPermissionResolver())
    container.register('auth.password_encoder_strategy.bcrypt', lambda: BcryptPasswordEncoderStrategy())
    container.register('auth.password_manager', lambda: PasswordManager(container.get('auth.password_encoder_strategy.bcrypt')))
    container.register('auth.authenticator', lambda: Authenticator(container.get('auth.user_adapter.saphi')))

    # Database
    container.register('db.database_manager', lambda: DatabaseManager(db, app.config))
    container.register('db.entity_manager', lambda: EntityManager(db, ModelRepository))
    container.register('db.dto_generator.dto_generator_service', lambda: DTOGeneratorServiceFactory.factory())
    container.register('db.dto_generator.html_code_formatter', lambda: HtmlCodeFormatter())

    # Event System
    container.register('event.subscriber.saphi_login_successful', lambda: SaphiLoginSuccessfulEventSubscriber(
        container.get('db.entity_manager'),
        container.get('auth.password_manager')
    ))
    container.register('event.event_manager', lambda: EventManagerFactory.factory(container.get('container')))

    # Faker
    container.register('faker.faker_service', lambda: FakerService(container.get('db.entity_manager'), container.get('resource.resource_manager')))

    # REST API
    container.register('http.router', lambda: RouterFactory.factory(container.get('container')))
    container.register('http.dispatcher', lambda: Dispatcher(container.get('http.router')))

    # HTTP Request Handlers
    container.register('http.request_handler.create_custom_track', lambda: CreateCustomTrack())
    container.register('http.request_handler.download_resource', lambda: DownloadResource(
        container.get('db.entity_manager'),
        container.get('resource.resource_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.find_custom_tracks', lambda: FindCustomTracks(
        container.get('db.entity_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.generate_dtos', lambda: GenerateDTOs(
        container.get('db.dto_generator.dto_generator_service'),
        container.get('db.dto_generator.html_code_formatter')
    ))
    container.register('http.request_handler.get_session', lambda: GetSession())
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
    container.register('http.request_handler.login_user', lambda: LoginUser(
        container.get('auth.authenticator'),
        container.get('db.entity_manager')
    ))
    container.register('http.request_handler.update_custom_track', lambda: UpdateCustomTrack(
        container.get('db.entity_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.verify_custom_track', lambda: VerifyCustomTrack(
        container.get('custom_track_manager'),
        container.get('auth.permission.permission_resolver')
    ))
    container.register('http.request_handler.verify_resource', lambda: VerifyResource(
        container.get('resource.resource_manager'),
        container.get('auth.permission.permission_resolver')
    ))

    # libraries
    container.register('custom_track_manager', lambda: CustomTrackManager(container.get('db.entity_manager'), container.get('resource.resource_manager')))
    container.register('saphi_client', lambda: SaphiClient(app.config['SAPHI_API_URL'], app.config['SAPHI_API_TOKEN']))

    # Resources
    container.register('resource.file_encoder_strategy.sha256', lambda: Sha256FileEncoderStrategy())
    container.register('resource.file_system_adapter.local', lambda: LocalFileSystemAdapter(f'{current_directory}/../resources'))
    container.register('resource.resource_manager', lambda: ResourceManager(
        container.get('db.entity_manager'),
        container.get('resource.file_system_adapter.local'),
        container.get('resource.file_encoder_strategy.sha256')
    ))

    # Container itself
    container.register('container', lambda: container)

    return container
