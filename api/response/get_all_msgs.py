from datetime import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResDTO


class ResGetAllMsgDTOSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    message = fields.Str()
    recipient_id = fields.Int()
    sender_id = fields.Int()

    @pre_load
    @post_load
    def deserialize(self, data: dict, **kwargs) -> dict:
        deserialized_data = data.copy()

        if 'created_at' in deserialized_data:
            deserialized_data['created_at'] = self.datetime_to_iso(data['created_at'])
        if 'updated_at' in data:
            deserialized_data['updated_at'] = self.datetime_to_iso(data['updated_at'])

        return deserialized_data

    @staticmethod
    def datetime_to_iso(dt) -> dict:
        if isinstance(dt, datetime):
            return dt.isoformat()
        return dt


class ResGetAllMsgDTO(ResDTO, ResGetAllMsgDTOSchema):
    __schema__ = ResGetAllMsgDTOSchema
