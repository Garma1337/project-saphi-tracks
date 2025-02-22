# coding: utf-8

from abc import abstractmethod


class DTOGenerator(object):

    @abstractmethod
    def generate_dtos(self, schemas: dict) -> str:
        pass
