# coding: utf-8

from marshmallow import fields, Schema
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column

from api.database.model.model import Model


class TagSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Tag(Model):
    __tablename__ = 'tags'
    __dump_schema__ = TagSchema

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
