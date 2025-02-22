# coding: utf-8


class HtmlCodeFormatter(object):

    def __init__(self):
        self.replace_map = {
            '\n': '<br>',
            '\t': '&nbsp;&nbsp;&nbsp;&nbsp;'
        }

    def format_code(self, code) -> str:
        for key, value in self.replace_map.items():
            code = code.replace(key, value)

        return code
