# coding: utf-8

from flask import Flask
from flask_jwt_extended import JWTManager

from api.container import container
from api.database.model.user import User

jwt = JWTManager()

def init_app(app: Flask):
    jwt.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user: User):
        return user.to_dictionary()

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        entity_manager = container.get('db.entity_manager')
        user_repository = entity_manager.get_repository(User)

        identity = jwt_data['sub']
        return user_repository.find_one(identity['id'])
