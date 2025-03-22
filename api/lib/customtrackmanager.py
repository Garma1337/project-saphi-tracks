# coding: utf-8

from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
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
