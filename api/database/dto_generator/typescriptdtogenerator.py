# coding: utf-8

from typing import Optional

from marshmallow import Schema

from api.database.dto_generator.dtogenerator import DTOGenerator


class TypeScriptDTOGenerator(DTOGenerator):

    def generate_dtos(self, schemas: dict) -> str:
        dtos = []

        for model_name, schema in schemas.items():
            dto = self.generate_dto(schemas, model_name, schema)
            dtos.append(dto)

        return '\n\n'.join(dtos)

    def generate_dto(self, schemas: dict, model_name: str, schema: Schema) -> str:
        dto = 'export type {} = {{\n'.format(model_name)

        for field in schema.fields:
            field_type = self.get_type(schemas, schema.fields[field])

            if field_type is None:
                raise ValueError('The field {} has an unsupported type'.format(field))

            dto += '\t{}: {};\n'.format(field, self.get_type(schemas, schema.fields[field]))

        dto += '}'

        return dto

    def get_type(self, schemas: dict, field) -> Optional[str]:
        if field.__class__.__name__ == 'String':
            return 'string'
        elif field.__class__.__name__ == 'Integer':
            return 'number'
        elif field.__class__.__name__ == 'Boolean':
            return 'boolean'
        elif field.__class__.__name__ == 'List':
            return '{}[]'.format(self.get_type(schemas, field.inner))
        elif field.__class__.__name__ == 'DateTime':
            return 'Date'
        elif field.__class__.__name__ == 'Nested':
            if field.schema.many:
                return '{}[]'.format(self.get_type_name(schemas, field.schema.__class__.__name__))
            else:
                return self.get_type_name(schemas, field.schema.__class__.__name__)
        else:
            return None

    def get_type_name(self, schemas: dict, field: str) -> str:
        return next((key for key, value in schemas.items() if value.__class__.__name__ == field), None)
