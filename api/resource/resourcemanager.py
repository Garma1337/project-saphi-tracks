# coding: utf-8

import os.path
import time
from datetime import datetime
from pathlib import Path
from typing import List

from werkzeug.datastructures import FileStorage

from api.database.entitymanager import EntityManager
from api.database.model.resource import ResourceType, Resource
from api.database.model.user import User
from api.lib.semvervalidator import SemVerValidator
from api.resource.file_encoder_strategy.fileencoderstrategy import FileEncoderStrategy
from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter


class ResourceCreationError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class ResourceAlreadyVerifiedError(Exception):
    pass


class ResourceManager(object):

    def __init__(
            self,
            entity_manager: EntityManager,
            file_system_adapter: FileSystemAdapter,
            file_encoder_strategy: FileEncoderStrategy,
            semver_validator: SemVerValidator
    ):
        self.entity_manager = entity_manager
        self.file_system_adapter = file_system_adapter
        self.file_encoder_strategy = file_encoder_strategy
        self.semver_validator = semver_validator

        self.max_file_size = 1024 * 512 * 10
        self.accepted_file_extensions = ['jpg', 'png', 'lev', 'vrm']
        self.accepted_mime_types = ['image/jpeg', 'image/png', 'model/vrml', 'application/octet-stream']

    def get_expected_file_extensions(self, resource_type: str) -> List[str]:
        extension_mapping = {
            ResourceType.PREVIEW.value: ['jpg', 'png'],
            ResourceType.XDELTA.value: ['xdelta'],
            ResourceType.VRM.value: ['vrm'],
            ResourceType.LEV.value: ['lev']
        }

        if resource_type not in extension_mapping:
            raise KeyError(f'No file extensions defined for resource type {resource_type}')

        return extension_mapping[resource_type]

    def offer_resource_download(self, resource_id: int) -> None:
        resource_repository = self.entity_manager.get_repository(Resource)
        resource = resource_repository.find_one(resource_id)

        if not resource:
            raise ValueError(f'No resource with id {resource_id} exists')

        encoder_target = self.file_encoder_strategy.encode_file_name(resource.file_name)
        target_directory = self.file_system_adapter.get_full_path(encoder_target.directory_path)

        self.file_system_adapter.offer_file_download(str(target_directory), encoder_target.file_name)

    def create_resource_from_uploaded_file(self, author_id: int, resource_type: str, uploaded_file: FileStorage, file_version: str) -> Resource:
        user_repository = self.entity_manager.get_repository(User)
        user = user_repository.find_one(author_id)

        if not user:
            raise ResourceCreationError(f'No user with id {author_id} exists')

        if not self.semver_validator.check_is_valid_semver(file_version):
            raise ResourceCreationError(f'"{file_version}" is not a valid semantic version')

        if uploaded_file.content_length > self.max_file_size:
            raise ResourceCreationError(f'File size exceeds the maximum limit of {self.max_file_size} bytes')

        file_extension = uploaded_file.filename.split('.')[-1]
        if file_extension not in self.get_expected_file_extensions(resource_type):
            raise ResourceCreationError(f'Invalid file extension {file_extension} for resource type {resource_type}')

        mime_type = uploaded_file.content_type
        if mime_type not in self.accepted_mime_types:
            raise ResourceCreationError(f'Invalid MIME type {mime_type} for resource type {resource_type}')

        # custom file name to prevent leaking source file names
        # you never know what people name their files after ...
        destination_file_name = f'{self._get_current_ts()}_{self.generate_file_name_for_resource_type(resource_type)}.{file_extension}'
        destination_file_path = self.move_uploaded_file(uploaded_file, destination_file_name)

        resource_repository = self.entity_manager.get_repository(Resource)
        resource = resource_repository.create(
            author_id=author_id,
            custom_track_id=None,
            file_name=destination_file_name,
            file_size=uploaded_file.content_length,
            resource_type=resource_type,
            checksum=self.file_system_adapter.generate_checksum(str(destination_file_path)),
            version=file_version,
            created=datetime.now(),
            verified=0
        )

        return resource

    def move_uploaded_file(self, uploaded_file: FileStorage, destination_file_name: str) -> Path:
        encoder_target = self.file_encoder_strategy.encode_file_name(destination_file_name)

        self.file_system_adapter.create_directory(encoder_target.get_directory_path())
        self.file_system_adapter.move_uploaded_file(uploaded_file, encoder_target.get_directory_path(), encoder_target.get_file_name())

        return self.file_system_adapter.get_full_path(encoder_target.get_directory_path()).joinpath(encoder_target.get_file_name())

    def verify_resource(self, resource_id: int) -> Resource:
        resource_repository = self.entity_manager.get_repository(Resource)
        resource = resource_repository.find_one(resource_id)

        if not resource:
            raise ResourceNotFoundError(f'No resource with id {resource_id} exists')

        if resource.verified:
            raise ResourceAlreadyVerifiedError(f'Resource with id {resource_id} is already verified')

        resource_repository.update(id=resource_id, verified=1)
        return resource_repository.find_one(resource_id)

    def get_local_path(self, file_name: str) -> str:
        encoder_target = self.file_encoder_strategy.encode_file_name(file_name)
        return os.path.join(encoder_target.get_directory_path(), encoder_target.get_file_name())

    def generate_file_name_for_resource_type(self, resource_type: str) -> str:
        file_name_mapping = {
            ResourceType.PREVIEW.value: 'preview',
            ResourceType.XDELTA.value: 'patch',
            ResourceType.VRM.value: 'texture',
            ResourceType.LEV.value: 'level'
        }

        if resource_type not in file_name_mapping:
            raise KeyError(f'No file name mapping defined for resource type {resource_type}')

        return file_name_mapping[resource_type]

    def _get_current_ts(self):
        return int(time.time())
