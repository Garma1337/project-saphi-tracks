# coding: utf-8

from unittest import TestCase

from marshmallow import Schema, fields

from api.database.dto_generator.pythondtogenerator import PythonDTOGenerator
from api.database.model.customtrack import CustomTrackSchema
from api.database.model.permission import PermissionSchema
from api.database.model.resource import ResourceSchema
from api.database.model.tag import TagSchema
from api.database.model.user import UserSchema


class TestSchema(Schema):
    id = fields.Decimal(1)


class PythonDTOGeneratorTest(TestCase):

    def setUp(self):
        self.dto_generator = PythonDTOGenerator()
        self.schemas = {
            'CustomTrack': CustomTrackSchema(),
            'Permission': PermissionSchema(),
            'Resource': ResourceSchema(),
            'Tag': TagSchema(),
            'User': UserSchema()
        }

    def test_can_generate_dto(self):
        dto = self.dto_generator.generate_dto(self.schemas, 'CustomTrack', self.schemas['CustomTrack'])

        expected = """class CustomTrack(object):
\tid: int
\tauthor_id: int
\tname: str
\tdescription: str
\tcreated: datetime
\thighlighted: bool
\tverified: bool
\tvideo: str
\tauthor: User
\tresources: List[Resource]
\ttags: List[Tag]"""

        self.assertEqual(expected.rstrip(), dto.rstrip())

    def test_cannot_generate_dto_with_unsupported_field_type(self):
        with self.assertRaises(ValueError):
            self.dto_generator.generate_dto(self.schemas, 'Test', TestSchema())

    def test_can_get_integer_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['id'])

        self.assertEqual(field_type, 'int')

    def test_can_get_string_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['name'])

        self.assertEqual(field_type, 'str')

    def test_can_get_boolean_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['highlighted'])

        self.assertEqual(field_type, 'bool')

    def test_can_get_datetime_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['created'])

        self.assertEqual(field_type, 'datetime')

    def test_can_get_nested_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['author'])

        self.assertEqual(field_type, 'User')

    def test_can_get_list_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, self.schemas['CustomTrack'].fields['tags'])

        self.assertEqual(field_type, 'List[Tag]')

    def test_cannot_get_unsupported_field_type(self):
        field_type = self.dto_generator.get_type(self.schemas, TestSchema().fields['id'])

        self.assertIsNone(field_type)

    def test_can_get_type_name(self):
        type_name = self.dto_generator.get_type_name(self.schemas, self.schemas['CustomTrack'].__class__.__name__)

        self.assertEqual(type_name, 'CustomTrack')

    def test_cannot_get_type_name(self):
        type_name = self.dto_generator.get_type_name(self.schemas, 'Test')

        self.assertIsNone(type_name)
