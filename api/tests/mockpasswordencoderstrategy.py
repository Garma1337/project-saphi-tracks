# coding=utf-8

from api.auth.password_encoder_strategy.passwordencoderstrategy import PasswordEncoderStrategy


class MockPasswordEncoderStrategy(PasswordEncoderStrategy):

    def generate_salt(self) -> str:
        return '123456'

    def encode_password(self, password: str, salt: str) -> str:
        return password
