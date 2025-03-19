# coding: utf-8

class JsonResponse(object):

    def __init__(self, data, status_code: int = 200) -> None:
        self.data = data
        self.status_code = status_code

    def get_data(self):
        return self.data

    def get_status_code(self) -> int:
        return self.status_code

    def to_dictionary(self) -> dict:
        return {
            'data': self.data,
            'status_code': self.status_code
        }


class EmptyResponse(JsonResponse):

    def __init__(self) -> None:
        super().__init__('', 204)


class ErrorJsonResponse(JsonResponse):

    def __init__(self, error: str, status_code: int = 400) -> None:
        super().__init__({'success': False, 'error': error }, status_code)


class SuccessJsonResponse(JsonResponse):

    def __init__(self, data, status_code: int = 200) -> None:
        data['success'] = True
        super().__init__(data, status_code)
