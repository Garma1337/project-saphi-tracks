# coding: utf-8

from flask_sqlalchemy import SQLAlchemy

from api.database.model.model import Model
from api.database.repository.modelrepository import ModelRepository


class EntityManager(object):

    def __init__(self, db: SQLAlchemy, model_repository_type: type[ModelRepository]) -> None:
        self.db = db
        self.model_repository_type = model_repository_type
        self.repository_cache = {}

    def get_repository(self, model_class: type[Model]) -> ModelRepository:
        if model_class not in self.repository_cache:
            self.repository_cache[model_class] = self.model_repository_type(self.db, model_class)

        return self.repository_cache[model_class]
