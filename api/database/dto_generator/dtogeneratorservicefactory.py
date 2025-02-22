# coding: utf-8

from api.database.dto_generator.dtogeneratorservice import DTOGeneratorService
from api.database.dto_generator.pythondtogenerator import PythonDTOGenerator
from api.database.dto_generator.typescriptdtogenerator import TypeScriptDTOGenerator
from api.database.model.customtrack import CustomTrackSchema
from api.database.model.permission import PermissionSchema
from api.database.model.resource import ResourceSchema
from api.database.model.setting import SettingSchema
from api.database.model.tag import TagSchema
from api.database.model.user import UserSchema


class DTOGeneratorServiceFactory(object):

    @staticmethod
    def factory() -> DTOGeneratorService:
        dto_generator_service = DTOGeneratorService()

        dto_generator_service.register_schema('CustomTrack', CustomTrackSchema())
        dto_generator_service.register_schema('Permission', PermissionSchema())
        dto_generator_service.register_schema('Resource', ResourceSchema())
        dto_generator_service.register_schema('Setting', SettingSchema())
        dto_generator_service.register_schema('Tag', TagSchema())
        dto_generator_service.register_schema('User', UserSchema())

        dto_generator_service.register_generator('python', PythonDTOGenerator())
        dto_generator_service.register_generator('typescript', TypeScriptDTOGenerator())

        return dto_generator_service
