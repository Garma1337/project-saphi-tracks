# coding: utf-8

from typing import List

from api.database.model.resource import ResourceType, Resource
from api.resource.file_encoder_strategy.fileencoderstrategy import FileEncoderStrategy
from api.resource.file_system_adapter.filesystemadapter import FileSystemAdapter


class ResourceManager(object):

    def __init__(self, file_system_adapter: FileSystemAdapter, file_encoder_strategy: FileEncoderStrategy):
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
