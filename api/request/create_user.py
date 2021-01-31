from marshmallow import Schema, fields, validate

from api.base import ReqDTO


class ReqCreateUserDTOSchema(Schema):
    username = fields.Str(required=True, allow_none=False, validate=validate.Length(max=100))
    password = fields.Str(required=True, allow_none=False, validate=validate.Length(min=8, max=100))
    first_name = fields.Str(required=True, allow_none=False, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, allow_none=False, validate=validate.Length(max=50))


class ReqCreateUserDTO(ReqDTO, ReqCreateUserDTOSchema):
    __schema__ = ReqCreateUserDTOSchema
