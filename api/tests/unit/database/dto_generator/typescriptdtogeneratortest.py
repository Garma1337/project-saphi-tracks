# coding: utf-8

from unittest import TestCase

from marshmallow import fields, Schema

from api.database.dto_generator.typescriptdtogenerator import TypeScriptDTOGenerator
from api.database.model.customtrack import CustomTrackSchema
from api.database.model.permission import PermissionSchema
from api.database.model.resource import ResourceSchema
from api.database.model.tag import TagSchema
from api.database.model.user import UserSchema


class TestSchema(Schema):
    id = fields.Decimal(1)


class TypeScriptDTOGeneratorTest(TestCase):

    def setUp(self):
        self.dto_generator = TypeScriptDTOGenerator()
        self.schemas = {
            'CustomTrack': CustomTrackSchema(),
            'Permission': PermissionSchema(),
            'Resource': ResourceSchema(),
            'Tag': TagSchema(),
            'User': UserSchema()
        }

    def test_can_generate_dto(self):
        dto = self.dto_generator.generate_dto(self.schemas, 'CustomTrack', self.schemas['CustomTrack'])

        expected = """export type CustomTrack = {
\tid: number;
\tauthor_id: number;
\tname: string;
\tdescription: string;
\tcreated: Date;
\thighlighted: boolean;
\tverified: boolean;
\tvideo: string;
\tauthor: User;
\tresources: Resource[];
\ttags: Tag[];
}"""

        self.assertEqual(expected.rstrip(), dto.rstrip())

    def test_cannot_generate_dto_with_unsupported_field_type(self):
        with self.assertRaises(ValueError):
            self.dto_generator.generate_dto(self.schemas, 'Test', TestSchema())

    def test_can_get_integer_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['id'])

        self.assertEqual(field_type, 'number')

    def test_can_get_string_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['name'])

        self.assertEqual(field_type, 'string')

    def test_can_get_boolean_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['highlighted'])

        self.assertEqual(field_type, 'boolean')

    def test_can_get_datetime_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['created'])

        self.assertEqual(field_type, 'Date')

    def test_can_get_nested_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['author'])

        self.assertEqual(field_type, 'User')

    def test_can_get_list_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['tags'])

        self.assertEqual(field_type, 'Tag[]')

    def test_cannot_get_unsupported_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, TestSchema().fields['id'])

        self.assertIsNone(field_type)

    def test_can_get_type_name(self):
        type_name = self.dto_generator.get_type_name(self.schemas, self.schemas['CustomTrack'].__class__.__name__)

        self.assertEqual(type_name, 'CustomTrack')

    def test_cannot_get_type_name(self):
        type_name = self.dto_generator.get_type_name(self.schemas, 'Test')

        self.assertIsNone(type_name)
