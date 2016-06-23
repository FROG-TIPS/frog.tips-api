import inspect
import re

from flask import Response, request
import flask.json


class ApiError(Exception):
    status_code = 400
    default_message = 'FROG CAN SWALLOW ERROR CONDITIONS UP TO THE SIZE OF ITS HEAD (3 CM).'

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', self.default_message)
        self.status_code = kwargs.get('status_code', self.status_code)
        self.payload = kwargs.get('payload')

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    @staticmethod
    def as_json_hint(json, **kwargs):
        kwargs.update({'message': 'FROG EXPECTED JSON OF THE FORM: {0}'.format(json)})
        return ApiError(**kwargs)


class BaseApiResponse(Response):
    def __init__(self, data=None, status=200, content_type=None, converters=None):
        default_content_type = 'application/json;charset=utf-8'
        converters = dict(converters or [])
        converters[default_content_type] = self.convert_application_json

        if content_type is None:
            # If the content type is not explicitly given, detect it
            content_type = request.accept_mimetypes.best_match([default_content_type] + list(converters.keys()))

        try:
            converter = converters[content_type]
        except KeyError:
            converter = converters[default_content_type]

        final_data = converter(data, status, content_type)
        super(BaseApiResponse, self).__init__(final_data, content_type=content_type, status=status)

    def convert_application_json(self, data, status, content_type):
        if data is None:
            return

        return flask.json.dumps(obj=data, indent=None, ensure_ascii=False, encoding='utf-8')
