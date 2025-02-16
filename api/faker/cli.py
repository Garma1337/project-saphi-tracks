# coding=utf-8

import click
from flask import Blueprint

from api.container import container
from api.database.model.resource import ResourceType

faker: Blueprint = Blueprint('faker', __name__)
faker_service = container.get('faker.faker_service')

@faker.cli.command('generate_custom_tracks')
@click.option('--count', default=50, help='The number of fake custom tracks to generate.')
def generate_custom_tracks(count: int):
    faker_service.generate_fake_custom_tracks(count)
    click.echo(f'Successfully created {count} fake custom tracks.')

@faker.cli.command('generate_resources')
@click.option('--count', default=50, help='The number of fake resources to generate.')
@click.option('--resource_type', default='PREVIEW', help='The type of resource to generate.')
def generate_resources(count: int, resource_type: str):
    faker_service.generate_fake_resources(count, resource_type)
    click.echo(f'Successfully created {count} fake resources.')

@faker.cli.command('generate_tags')
@click.option('--count', default=50, help='The number of fake tags to generate.')
def generate_tags(count: int):
    faker_service.generate_fake_tags(count)
    click.echo(f'Successfully created {count} fake tags.')

@faker.cli.command('generate_users')
@click.option('--count', default=50, help='The number of fake users to generate.')
def generate_users(count: int):
    faker_service.generate_fake_users(count)
    click.echo(f'Successfully created {count} fake players.')

@faker.cli.command('generate_all')
@click.option('--count', default=50, help='The number of fake entities to generate.')
def generate_all(count: int):
    faker_service.generate_fake_users(count)
    faker_service.generate_fake_custom_tracks(count)
    faker_service.generate_fake_resources(count, ResourceType.PREVIEW.value)
    faker_service.generate_fake_resources(count, ResourceType.LEV.value)
    faker_service.generate_fake_resources(count, ResourceType.VRM.value)
    faker_service.generate_fake_resources(count, ResourceType.XDELTA.value)
    faker_service.generate_fake_tags(count)

    click.echo(f'Successfully created {count} fake users, custom tracks, resources, and tags.')
