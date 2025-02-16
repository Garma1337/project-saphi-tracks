# coding=utf-8

from marshmallow import Schema
from sqlalchemy.orm import mapped_column, Mapped, declarative_base

from api import db

Base = declarative_base()


class MockSchema(Schema):
    pass


class MockModel(Base):

    __tablename__ = 'mock'
    __dump_schema__ = MockSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    value = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
