from marshmallow import Schema, fields, validate

from api.base import ReqDTO


class ReqAuthDTOSchema(Schema):
    username = fields.Str(required=True, allow_none=False, validate=validate.Length(max=100))
    password = fields.Str(required=True, allow_none=False, validate=validate.Length(min=8, max=100))


class ReqAuthDTO(ReqDTO, ReqAuthDTOSchema):
    __schema__ = ReqAuthDTOSchema