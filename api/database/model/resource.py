# coding: utf-8

from enum import Enum

from marshmallow import Schema, fields
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.model.model import Model


class ResourceType(Enum):
    PREVIEW = 'preview'
    XDELTA = 'xdelta'
    VRM = 'vrm'
    LEV = 'lev'


class ResourceSchema(Schema):
    id = fields.Int()
    author_id = fields.Int()
    custom_track_id = fields.Int()
    file_name = fields.Str()
    file_size = fields.Int()
    resource_type = fields.Str()
    checksum = fields.Str()
    version = fields.Str()
    created = fields.DateTime()
    verified = fields.Bool()
    author = fields.Nested('UserSchema', exclude=('resources','custom_tracks','permission',))
    custom_track = fields.Nested('CustomTrackSchema', exclude=('resources','author','tags',))


class Resource(Model):
    __tablename__ = 'resources'
    __dump_schema__ = ResourceSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    author_id: Mapped[int] = Column(ForeignKey('users.id'))
    custom_track_id: Mapped[int] = Column(ForeignKey('custom_tracks.id'))
    file_name: Mapped[str] = Column(String(100), nullable=False)
    file_size: Mapped[int] = Column(Integer(), nullable=False)
    resource_type: Mapped[str] = Column(String(100), nullable=False)
    checksum: Mapped[str] = Column(String(100), nullable=False)
    version: Mapped[str] = Column(String(100), nullable=False)
    created: Mapped[str] = Column(DateTime(), nullable=False)
    verified: Mapped[bool] = Column(Integer(), nullable=False, default=False)
    author: Mapped['User'] = relationship('User', back_populates='resources')
    custom_track: Mapped['CustomTrack'] = relationship('CustomTrack', back_populates='resources')
