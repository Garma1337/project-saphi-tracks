# coding: utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column

from api.database.model.model import Model


class SettingSchema(Schema):
    id = fields.Int()
    category = fields.Str()
    key = fields.Str()
    value = fields.Str()


class Setting(Model):
    __tablename__ = 'settings'
    __dump_schema__ = SettingSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    category: Mapped[str] = Column(String(100), nullable=False)
    key: Mapped[str] = Column(String(100), nullable=False)
    value: Mapped[str] = Column(String(100), nullable=False)
