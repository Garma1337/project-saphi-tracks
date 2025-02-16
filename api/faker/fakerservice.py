# coding: utf-8

import hashlib
import random
import uuid
from datetime import datetime
from typing import List

from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.permission import Permission
from api.database.model.resource import Resource, ResourceType
from api.database.model.tag import Tag
from api.database.model.user import User
from api.resource.resourcemanager import ResourceManager


class FakerService(object):

    def __init__(self, entity_manager: EntityManager, resource_manager: ResourceManager):
        self.entity_manager = entity_manager
        self.resource_manager = resource_manager

    def generate_fake_custom_tracks(self, count: int) -> List[CustomTrack]:
        if count < 1:
            raise ValueError('Count must be greater than 0')

        user_repository = self.entity_manager.get_repository(User)

        if user_repository.count() < 1:
            raise ValueError('No users found in the database')

        users = user_repository.find_by()
        custom_track_repository = self.entity_manager.get_repository(CustomTrack)

        fake_custom_tracks = []

        for i in range(1, count + 1):
            random_user = random.choice(users)

            custom_track = custom_track_repository.create(
                author_id=random_user.id,
                name=f'Custom Track {i}',
                description=f'This is a really cool description for Custom Track {i}',
                highlighted=random.randint(0, 1),
                verified=random.randint(0, 1),
                created=datetime.now()
            )

            fake_custom_tracks.append(custom_track)

        return fake_custom_tracks

    def generate_fake_resources(self, count: int, resource_type: str) -> List[CustomTrack]:
        if count < 1:
            raise ValueError('Count must be greater than 0')

        if resource_type not in [ResourceType.PREVIEW.value, ResourceType.XDELTA.value, ResourceType.VRM.value, ResourceType.LEV.value]:
            raise ValueError(f'{resource_type} is not a valid resource type')

        user_repository = self.entity_manager.get_repository(User)

        if user_repository.count() < 1:
            raise ValueError('No users found in the database')

        custom_track_repository = self.entity_manager.get_repository(CustomTrack)

        if custom_track_repository.count() < 1:
            raise ValueError('No custom tracks found in the database')

        expected_extensions = self.resource_manager.get_expected_file_extensions(resource_type)

        users = user_repository.find_by()
        custom_tracks = custom_track_repository.find_by()

        resource_repository = self.entity_manager.get_repository(Resource)
        fake_resources = []

        for i in range(1, count + 1):
            random_custom_track = random.choice(custom_tracks)
            random_extension = random.choice(expected_extensions)

            resource = resource_repository.create(
                author_id=random_custom_track.author_id,
                custom_track_id=random_custom_track.id,
                file_name=f'file{i}.{random_extension}',
                file_size=random.randint(1000000, 5000000),
                resource_type=resource_type,
                checksum=hashlib.md5(f'file{i}.{random_extension}'.encode()).hexdigest(),
                version=f'1.0.0',
                created=datetime.now(),
                verified=random.randint(0, 1)
            )

            fake_resources.append(resource)

        return fake_resources

    def generate_fake_tags(self, count: int) -> List[Tag]:
        if count < 1:
            raise ValueError('Count must be greater than 0')

        tag_repository = self.entity_manager.get_repository(Tag)
        tags = []

        for i in range(1, count + 1):
            tag = tag_repository.create(name=f'Tag {i}')
            tags.append(tag)

        return tags

    def generate_fake_users(self, count: int) -> List[User]:
        if count < 1:
            raise ValueError('Count must be greater than 0')

        user_repository = self.entity_manager.get_repository(User)
        permission_repository = self.entity_manager.get_repository(Permission)

        fake_users = []

        for i in range(1, count + 1):
            user = user_repository.create(
                email=f'{str(uuid.uuid4())}@domain.com',
                username=f'User {i}',
                password=hashlib.sha256(f'password_{i}'.encode()).hexdigest(),
                created=datetime.now(),
                verified=random.randint(0, 1)
            )

            permission_repository.create(
                user_id=user.id,
                can_edit_custom_tracks=False,
                can_delete_custom_tracks=False,
                can_edit_resources=False,
                can_delete_resources=False,
                can_edit_users=False
            )

            fake_users.append(user)

        return fake_users
