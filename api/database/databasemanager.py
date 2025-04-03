# coding: utf-8

from flask import Config
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from api.util.filesystemhelper import FileSystemHelper


class DatabaseManager(object):

    def __init__(self, db: SQLAlchemy, config: Config):
        self.db = db
        self.config = config

    def reset_database(self):
        self.db.session.execute(text(f'DROP SCHEMA public CASCADE'))
        self.db.session.execute(text(f'CREATE SCHEMA public'))
        self.db.session.execute(text(f'GRANT ALL ON SCHEMA public TO {self.config["DATABASE_USER"]}'))
        self.db.session.commit()
        upgrade(directory=f'{FileSystemHelper.get_current_directory()}/../../migrations')
