# coding: utf-8

from typing import List

from api.database.model.resource import ResourceType


class ResourceManager(object):

    def get_expected_file_extensions(self, resource_type: str) -> List[str]:
        extension_mapping = {
            ResourceType.PREVIEW.value: ['jpg', 'png'],
            ResourceType.XDELTA.value: ['xdelta'],
            ResourceType.VRM.value: ['vrm'],
            ResourceType.LEV.value: ['lev']
        }

        return extension_mapping[resource_type]
