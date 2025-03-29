# coding: utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.associations import custom_tracks_tags
from api.database.model.model import Model


class CustomTrackSchema(Schema):
    id = fields.Int()
    author_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    highlighted = fields.Bool()
    verified = fields.Bool()
    video = fields.Str()
    author = fields.Nested('UserSchema', exclude=('custom_tracks','resources','permission',))
    resources = fields.Nested('ResourceSchema', exclude=('custom_track','author',), many=True)
    tags = fields.Nested('TagSchema', exclude=('custom_tracks',), many=True)


class CustomTrack(Model):
    __tablename__ = 'custom_tracks'
    __dump_schema__ = CustomTrackSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    author_id: Mapped[int] = Column(ForeignKey('users.id'))
    name: Mapped[str] = Column(String(100), nullable=False)
    description: Mapped[str] = Column(Text(), nullable=False)
    created: Mapped[str] = Column(DateTime(), nullable=False)
    highlighted: Mapped[bool] = Column(Boolean(), nullable=False)
    verified: Mapped[bool] = Column(Boolean(), nullable=False)
    video: Mapped[str] = Column(String(100), nullable=True)
    author: Mapped['User'] = relationship('User', back_populates='custom_tracks')
    resources: Mapped[List['Resource']] = relationship('Resource', back_populates='custom_track')
    tags: Mapped[List['Tag']] = relationship('Tag', secondary=custom_tracks_tags, back_populates='custom_tracks')
