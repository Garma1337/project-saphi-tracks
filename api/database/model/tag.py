# coding: utf-8

from typing import List

from marshmallow import fields, Schema
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.associations import custom_tracks_tags
from api.database.model.model import Model


class TagSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    custom_tracks = fields.Nested('CustomTrackSchema', exclude=('tags',), many=True)


class Tag(Model):
    __tablename__ = 'tags'
    __dump_schema__ = TagSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    custom_tracks: Mapped[List['CustomTrack']] = relationship('CustomTrack', secondary=custom_tracks_tags, back_populates='tags')
