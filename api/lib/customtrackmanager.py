# coding: utf-8

from datetime import datetime

from werkzeug.datastructures import FileStorage

from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.resource import ResourceType, Resource
from api.resource.resourcemanager import ResourceManager


class CustomTrackNotFoundError(Exception):
    pass


class CustomTrackAlreadyVerifiedError(Exception):
    pass


class CustomTrackManager(object):

    def __init__(self, entity_manager: EntityManager, resource_manager: ResourceManager):
        self.entity_manager = entity_manager
        self.resource_manager = resource_manager

    def verify_custom_track(self, custom_track_id: int) -> CustomTrack:
        custom_track_repository = self.entity_manager.get_repository(CustomTrack)
        custom_track = custom_track_repository.find_one(custom_track_id)

        if not custom_track:
            raise CustomTrackNotFoundError(f'No custom track with id {custom_track_id} exists')

        if custom_track.verified:
            raise CustomTrackAlreadyVerifiedError(f'Custom track with id {custom_track_id} is already verified')

        custom_track_repository.update(id=custom_track_id, verified=True)

        for resource in custom_track.resources:
            self.resource_manager.verify_resource(resource.id)

        return custom_track_repository.find_one(custom_track_id)

    def create_custom_track(
            self,
            author_id: int,
            name: str,
            description: str,
            video: str,
            preview_image: FileStorage,
            lev_file: FileStorage,
            lev_file_version: str,
            vrm_file: FileStorage,
            vrm_file_version: str
    ) -> CustomTrack:
        # we first create the resources to make sure they can be stored on the file system
        # after that we create the custom track and update the resources with the custom track id
        preview_image_resource = self.resource_manager.create_resource_from_uploaded_file(
            author_id,
            ResourceType.PREVIEW.value,
            preview_image,
            '1.0.0'
        )

        lev_resource = self.resource_manager.create_resource_from_uploaded_file(
            author_id,
            ResourceType.LEV.value,
            lev_file,
            lev_file_version
        )

        vrm_resource = self.resource_manager.create_resource_from_uploaded_file(
            author_id,
            ResourceType.VRM.value,
            vrm_file,
            vrm_file_version
        )

        custom_track_repository = self.entity_manager.get_repository(CustomTrack)
        custom_track = custom_track_repository.create(
            author_id=author_id,
            name=name,
            description=description,
            created=datetime.now(),
            highlighted=0,
            verified=0,
            video=video
        )

        resource_repository = self.entity_manager.get_repository(Resource)
        resource_repository.update(id=preview_image_resource.id, custom_track_id=custom_track.id)
        resource_repository.update(id=lev_resource.id, custom_track_id=custom_track.id)
        resource_repository.update(id=vrm_resource.id, custom_track_id=custom_track.id)

        return custom_track
