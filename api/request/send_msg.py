from marshmallow import Schema, fields, validate

from api.base import ReqDTO


class ReqCreateMsgDTOSchema(Schema):
    message = fields.Str(required=True, allow_none=False, validate=validate.Length(max=500))
    recipient = fields.Str(required=True, allow_none=False, validate=validate.Length(max=100))


class ReqCreateMsgDTO(ReqDTO, ReqCreateMsgDTOSchema):
    __schema__ = ReqCreateMsgDTOSchema
