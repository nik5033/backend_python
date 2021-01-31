from datetime import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResDTO


class ResGetUserDTOSchema(Schema):
    id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @pre_load
    @post_load
    def deserialize(self, data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = self.datetime_to_iso(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = self.datetime_to_iso(data['updated_at'])

        return data

    @staticmethod
    def datetime_to_iso(dt) -> dict:
        if isinstance(dt, datetime):
            return dt.isoformat()
        return dt


class ResGetUserDTO(ResDTO, ResGetUserDTOSchema):
    __schema__ = ResGetUserDTOSchema
