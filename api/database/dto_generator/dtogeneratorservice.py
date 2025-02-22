# coding: utf-8

from marshmallow import Schema

from api.database.dto_generator.dtogenerator import DTOGenerator


class DTOGeneratorService(object):

    def __init__(self):
        self.schemas = {}
        self.generators = {}

    def generate_dtos(self, generator_type: str) -> str:
        if not self.has_generator(generator_type):
            raise ValueError('No DTO generator of type {} is registered'.format(generator_type))

        return self.generators[generator_type].generate_dtos(self.schemas)

    def register_schema(self, model_name: str, schema: Schema):
        if self.has_schema(model_name):
            raise ValueError('A schema for the model {} is already registered'.format(model_name))

        self.schemas[model_name] = schema

    def register_generator(self, generator_type: str, generator: DTOGenerator):
        if self.has_generator(generator_type):
            raise ValueError('A DTO generator of type {} is already registered'.format(generator_type))

        self.generators[generator_type] = generator

    def has_schema(self, model_name: str) -> bool:
        return model_name in self.schemas

    def has_generator(self, generator_type: str) -> bool:
        return generator_type in self.generators
