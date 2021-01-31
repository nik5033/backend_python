from marshmallow import Schema, fields, validate

from api.base import ReqDTO


class ReqUpdateMsgDTOSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(max=500))


class ReqUpdateMsgDTO(ReqDTO, ReqUpdateMsgDTOSchema):
    __schema__ = ReqUpdateMsgDTOSchema
