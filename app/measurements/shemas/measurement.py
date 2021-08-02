from marshmallow import Schema, fields, validate, post_load, pre_load, ValidationError
from app.measurements.view import MeasurementsView
from app.measurements.constants import PAGE, PER_PAGE
class MeasurementResponseSchema(Schema):
    id = fields.Integer(required=False)
    temperature = fields.Float()
    pollution = fields.Float()
    humidity = fields.Float()
    created = fields.DateTime()

class MeasurementPostSchema(Schema):
    id = fields.Integer()
    temperature = fields.Float(required=True, validate=validate.Range(min=-70, max=70))
    pollution = fields.Float(required=True, validate=validate.Range(min=-1000, max=1000))
    humidity = fields.Float(required=True, validate=validate.Range(min=-1000, max=1000))
    created = fields.DateTime()

    @post_load()
    def format(self, data, **kwargs):
        return MeasurementsView(**data)

class MeasurementPatchSchema(Schema):
    @pre_load()
    def patch_process(self, data, **kwargs):
        temp = data.get("temperature")
        pol = data.get("pollution")
        hum = data.get("humidity")
        if not temp and not pol and not hum:
            raise ValidationError("Must put some changes into schema")
        return data

    temperature = fields.Float(required=False, validate=validate.Range(min=-70, max=70))
    pollution = fields.Float(required=False, validate=validate.Range(min=-1000, max=1000))
    humidity = fields.Float(required=False, validate=validate.Range(min=-1000, max=1000))
    created = fields.DateTime()

class MeasurementGetLatestSchema(Schema):
    id = fields.Integer(required=False)
    temperature = fields.Float()
    pollution = fields.Float()
    humidity = fields.Float()
    created = fields.DateTime()

    # {"id": measurement.id,
    #  "temperature": measurement.temperature,
    #  "pollution": measurement.pollution,
    #  "humidity": measurement.humidity}

class MeasurementMetaSchema(Schema):
    page = fields.Integer(required=False, default=PAGE, missing=PAGE)
    per_page = fields.Integer(required=False, missing=5, default=PER_PAGE)
    total = fields.Integer(required=False, default=0, missing=0)

class MeasurementPaginationSchema(Schema):

    total = fields.Integer()
    page = fields.Integer()
    per_page = fields.Integer()
    has_next = fields.Boolean()
    # items = fields.List(fields.Nested(MeasurementResponseSchema()))
    meta = fields.Method('get_meta')
    results = fields.Method('get_results')

    @staticmethod
    def get_meta(data):
        response = dict()
        response["total"] = data.total
        response["page"] = data.page
        response["per_page"] = data.per_page
        return MeasurementMetaSchema().dump(response)

    @staticmethod
    def get_results(data):
        return MeasurementResponseSchema(many=True).dump(data.items)


