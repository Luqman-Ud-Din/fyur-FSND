import re

from wtforms import ValidationError


class ValidatePattern:
    def __init__(self, pattern=None, message=None):
        if pattern is None:
            raise ValidationError('Pattern is Required')

        if not message:
            message = 'Not matching with the given pattern'

        self.message = f'{message} \n {pattern}'
        self.pattern = pattern

    def __call__(self, form, field):
        data = (field.data or '').strip()

        if not re.match(self.pattern, data):
            raise ValidationError(self.message)

        return data
