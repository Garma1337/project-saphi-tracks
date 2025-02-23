# coding=utf-8

from abc import ABC

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

from api.database.model.model import Model


class ModelRepository(ABC):
    """
    A generic model repository for all kinds of models.
    If a model needs a more complex implementation, a custom repository should be created.
    """

    def __init__(self, db: SQLAlchemy, model_class: type[Model]) -> None:
        self.db = db
        self.model_class = model_class

    def find_one(self, id: int):
        query = self.db.session.query(self.model_class).where(getattr(self.model_class, 'id') == id)
        return query.first()

    def find_by(self, **kwargs):
        query = self.db.session.query(self.model_class)

        for arg in kwargs:
            if kwargs[arg] is not None:
                if arg == 'limit':
                    query = query.limit(kwargs[arg])
                elif arg == 'offset':
                    query = query.offset(kwargs[arg])
                else:
                    if not hasattr(self.model_class, arg):
                        raise ValueError(f'Entity {self.model_class.__name__} has no attribute {arg}')

                    if isinstance(kwargs[arg], str):
                        query = query.where(getattr(self.model_class, arg).ilike(f'%{kwargs[arg]}%'))
                    else:
                        query = query.where(getattr(self.model_class, arg) == kwargs[arg])

        return query.all()

    def count(self, **kwargs) -> int:
        query = self.db.session.query(self.model_class)

        for arg in kwargs:
            if kwargs[arg] is not None:
                if not hasattr(self.model_class, arg):
                    raise ValueError(f'Entity {self.model_class.__name__} has no attribute {arg}')

                if isinstance(kwargs[arg], str):
                    query = query.where(getattr(self.model_class, arg).ilike(f'%{kwargs[arg]}%'))
                else:
                    query = query.where(getattr(self.model_class, arg) == kwargs[arg])

        return query.count()

    def create(self, **kwargs) -> Model:
        model = self.model_class(**kwargs)
        self.db.session.add(model)
        self.db.session.commit()

        return model

    def update(self, **kwargs) -> None:
        if not 'id' in kwargs:
            raise ValueError('An id is required to update an entity')

        for attribute in kwargs:
            if not hasattr(self.model_class, attribute):
                raise ValueError(f'Entity {self.model_class.__name__} has no attribute {attribute}')

        statement = (
            update(self.model_class)
            .where(getattr(self.model_class, 'id').in_([kwargs['id']]))
            .values(**kwargs)
        )

        self.db.session.execute(statement)
        self.db.session.commit()

    def delete_all(self) -> None:
        self.db.session.query(self.model_class).delete()
        self.db.session.commit()

    def set_model_class(self, model: type) -> None:
        self.model_class = model
