from marshmallow import Schema, fields

from api.base import ResDTO


class ResAuthDTOSchema(Schema):
    Authorization = fields.Str()


class ResAuthDTO(ResDTO, ResAuthDTOSchema):
    __schema__ = ResAuthDTOSchema
