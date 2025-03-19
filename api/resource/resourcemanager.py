# coding: utf-8

from typing import List

from flask import send_from_directory

from api.database.entitymanager import EntityManager
from api.database.model.resource import ResourceType, Resource
from api.resource.file_encoder_strategy.fileencoderstrategy import FileEncoderStrategy
from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter


class ResourceManager(object):

    def __init__(self, entity_manager: EntityManager, file_system_adapter: FileSystemAdapter, file_encoder_strategy: FileEncoderStrategy):
        self.entity_manager = entity_manager
        self.file_system_adapter = file_system_adapter
        self.file_encoder_strategy = file_encoder_strategy

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
        self._send_from_directory(encoder_target.directory_path, encoder_target.file_name)

    def _send_from_directory(self, directory: str, file_path: str) -> None:
        send_from_directory(directory, file_path)

    def create_resource(self, resource_type: str, file_name: str, file_data: bytes) -> str:
        pass
