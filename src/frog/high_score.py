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
        kwargs.update('message', 'FROG EXPECTED JSON OF THE FORM: {0}'.format(json))
        return ApiError(**kwargs)
