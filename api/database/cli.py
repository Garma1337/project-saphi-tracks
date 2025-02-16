# coding: utf-8

import click
from flask import Blueprint

from api.container import container

db_helper: Blueprint = Blueprint('db_helper', __name__)
database_manager = container.get('db.database_manager')

@db_helper.cli.command('reset_database')
def reset_database():
    database_manager.reset_database()
    click.echo('Database reset successfully.')
