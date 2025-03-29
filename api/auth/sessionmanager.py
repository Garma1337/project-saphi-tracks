# coding: utf-8

from typing import Optional

from api.database.entitymanager import EntityManager
from api.database.model.user import User


class SessionManager(object):

    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    def find_user_by_jwt_identity(self, jwt_identity) -> Optional[User]:
        if jwt_identity is None:
            return None

        user_repository = self.entity_manager.get_repository(User)
        return user_repository.find_one(jwt_identity['id'])
