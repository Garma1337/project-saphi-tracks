# coding: utf-8

from flask import Request

from api.database.dto_generator.dtogeneratorservice import DTOGeneratorService
from api.database.dto_generator.htmlcodeformatter import HtmlCodeFormatter
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse, ErrorJsonResponse


class GenerateDTOs(RequestHandler):

    def __init__(self, dto_generator_service: DTOGeneratorService, html_code_formatter: HtmlCodeFormatter):
        self.dto_generator_service = dto_generator_service
        self.html_code_formatter = html_code_formatter

    def handle_request(self, request: Request) -> JsonResponse:
        generator_type = request.args.get('generator_type')

        if generator_type is None:
            return ErrorJsonResponse('The generator_type parameter is required.', 400)

        try:
            code = self.dto_generator_service.generate_dtos(generator_type)
            code = self.html_code_formatter.format_code(code)

            return JsonResponse(f'<code>{code}</code>', 200)
        except ValueError as e:
            return ErrorJsonResponse(str(e), 400)

    def require_authentication(self):
        return False
