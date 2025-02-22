# coding: utf-8

from api.database.repository.modelrepository import ModelRepository


class MockModelRepository(ModelRepository):

    def __init__(self, model_class):
        self.models = []
        self.id = 1
        self.model_class = model_class

    def find_one(self, id):
        models = [model for model in self.models if model.id == id]

        if len(models) > 0:
            return models[0]

        return None

    def find_by(self, **kwargs):
        models = self.models

        for arg in kwargs:
            if kwargs[arg] is not None:
                if arg == 'limit' or arg == 'offset':
                    continue
                else:
                    models = [model for model in models if str(getattr(model, arg)) == str(kwargs[arg])]

        if 'offset' in kwargs:
            models = models[kwargs['offset']:]

        if 'limit' in kwargs:
            models = models[:kwargs['limit']]

        return models

    def count(self, **kwargs) -> int:
        return len(self.find_by(**kwargs))

    def create(self, **kwargs):
        model = self.model_class(**kwargs)
        model.id = self.id
        self.id += 1

        self.models.append(model)

        return model

    def update(self, **kwargs):
        if not 'id' in kwargs:
            raise ValueError('An id is required to update an entity')

        model = self.find_one(kwargs['id'])

        for attribute in kwargs:
            if kwargs[attribute] is not None:
                setattr(model, attribute, kwargs[attribute])

        return model
