# coding: utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.model.model import Model


class ResourceSchema(Schema):
    id = fields.Int()
    custom_track_id = fields.Int()
    file_name = fields.Str()
    file_size = fields.Int()
    resource_type = fields.Str()
    checksum = fields.Str()
    version = fields.Str()
    created = fields.DateTime()
    custom_track = fields.Nested('CustomTrackSchema', exclude=('resources',))


class Resource(Model):
    __tablename__ = 'resources'
    __dump_schema__ = ResourceSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    custom_track_id: Mapped[int] = Column(ForeignKey('custom_tracks.id'))
    file_name: Mapped[str] = Column(String(100), nullable=False)
    file_size: Mapped[int] = Column(Integer(), nullable=False)
    resource_type: Mapped[str] = Column(String(100), nullable=False)
    checksum: Mapped[str] = Column(String(100), nullable=False)
    version: Mapped[str] = Column(String(100), nullable=False)
    created: Mapped[str] = Column(DateTime(), nullable=False)
    custom_track: Mapped['CustomTrack'] = relationship('CustomTrack', back_populates='resources')
