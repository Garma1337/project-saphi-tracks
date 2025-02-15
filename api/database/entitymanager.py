# coding: utf-8

from copy import copy

from api.database.model.model import Model
from api.database.repository.modelrepository import ModelRepository


class EntityManager(object):

    def __init__(self, model_repository: ModelRepository) -> None:
        self.model_repository = model_repository

    def get_repository(self, model: type[Model]) -> ModelRepository:
        model_repository = copy(self.model_repository)
        model_repository.set_model_class(model)

        return model_repository
