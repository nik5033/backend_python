from marshmallow import Schema, fields, validate

from api.base import ReqDTO


class ReqUpdateUserDTOSchema(Schema):
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))


class ReqUpdateUserDTO(ReqDTO, ReqUpdateUserDTOSchema):
    __schema__ = ReqUpdateUserDTOSchema

    fields: list

    def __init__(self, *args, **kwargs):
        self.fields = []
        super(ReqUpdateUserDTO, self).__init__(*args, **kwargs)

    def set(self, key, value):
        self.fields.append(key)
        super(ReqUpdateUserDTO, self).set(key, value)
