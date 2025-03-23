# coding=utf-8

import sys

from cachelib import NullCache
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

sys.dont_write_bytecode = True

db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config.dev.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import container
    container.init_app(app)

    from . import jwt
    jwt.init_app(app)

    from .http.controller.apicontroller import api
    from .http.controller.webcontroller import web
    from .faker.cli import faker
    from .database.cli import db_helper

    app.register_blueprint(api)
    app.register_blueprint(web)
    app.register_blueprint(faker)
    app.register_blueprint(db_helper)

    return app

def create_test_app() -> Flask:
    """
    This app factory is only used for integration testing. It is not used in production.
    :return: The flask test app
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config.dev.py', silent=True)

    app.config.from_mapping({
        'SESSION_TYPE': 'cachelib',
        'SESSION_CACHELIB': NullCache(),
    })

    db.init_app(app)
    migrate.init_app(app, db)

    from . import container
    container.init_app(app)

    from . import jwt
    jwt.init_app(app)

    return app

from api.database.model import (
    customtrack,
    model,
    permission,
    resource,
    setting,
    tag,
    user,
)
