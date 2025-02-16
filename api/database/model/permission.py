# coding: utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.model.model import Model


class PermissionSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    can_edit_custom_tracks = fields.Bool()
    can_delete_custom_tracks = fields.Bool()
    can_edit_resources = fields.Bool()
    can_delete_resources = fields.Bool()
    can_edit_users = fields.Bool()
    user = fields.Nested('UserSchema', exclude=('permission','custom_tracks','resources',))


class Permission(Model):
    __tablename__ = 'permissions'
    __dump_schema__ = PermissionSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = Column(ForeignKey('users.id'), unique=True)
    can_edit_custom_tracks: Mapped[bool] = Column(Boolean(), nullable=False)
    can_delete_custom_tracks: Mapped[bool] = Column(Boolean(), nullable=False)
    can_edit_resources: Mapped[bool] = Column(Boolean(), nullable=False)
    can_delete_resources: Mapped[bool] = Column(Boolean(), nullable=False)
    can_edit_users: Mapped[bool] = Column(Boolean(), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='permission')
