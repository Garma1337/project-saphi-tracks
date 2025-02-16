# coding: utf-8

from abc import ABC, abstractmethod

from api.database.model.customtrack import CustomTrack
from api.database.model.resource import Resource
from api.database.model.user import User


class PermissionResolver(ABC):

    @abstractmethod
    def can_edit_custom_track(self, user: User, custom_track: CustomTrack) -> bool:
        pass

    @abstractmethod
    def can_delete_custom_track(self, user: User, custom_track: CustomTrack) -> bool:
        pass

    @abstractmethod
    def can_edit_resource(self, user: User, resource: Resource) -> bool:
        pass

    @abstractmethod
    def can_delete_resource(self, user: User, resource: Resource):
        pass

    @abstractmethod
    def can_edit_user(self, user: User, target_user: User) -> bool:
        pass
