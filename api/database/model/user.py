# coding: utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.model.model import Model


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    created = fields.DateTime()
    verified = fields.Bool()
    custom_tracks = fields.Nested('CustomTrackSchema', exclude=('author','resources','tags'), many=True)
    permission = fields.Nested('PermissionSchema', exclude=('user',))
    resources = fields.Nested('ResourceSchema', exclude=('author','custom_track',), many=True)


class User(Model):
    __tablename__ = 'users'
    __dump_schema__ = UserSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    username: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(String(100), nullable=False)
    password: Mapped[str] = Column(String(100), nullable=False)
    created: Mapped[str] = Column(DateTime(), nullable=False)
    verified: Mapped[bool] = Column(Boolean(), nullable=False)
    custom_tracks: Mapped[List['CustomTrack']] = relationship('CustomTrack', back_populates='author')
    permission: Mapped['Permission'] = relationship('Permission', back_populates='user')
    resources: Mapped[List['Resource']] = relationship('Resource', back_populates='author')
