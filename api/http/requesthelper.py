# coding: utf-8

from typing import Optional


class RequestHelper(object):

    @staticmethod
    def try_parse_boolean_value(request_params: dict, parameter_name: str) -> Optional[bool]:
        parameter = request_params.get(parameter_name)

        if parameter:
            try:
                return bool(int(parameter))
            except ValueError:
                return bool(parameter.lower() == 'true')

        return None

    @staticmethod
    def try_parse_integer_value(request_params: dict, parameter_name: str) -> Optional[int]:
        parameter = request_params.get(parameter_name)

        if parameter:
            try:
                return int(parameter)
            except ValueError:
                return None

        return None
