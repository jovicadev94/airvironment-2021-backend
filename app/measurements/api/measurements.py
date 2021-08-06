from app.measurements import measurement_bp
from flask import request
from app.measurements.schemas import PaginationResultSchema, \
    MeasurementResponseSchema, MeasurementPostRequestSchema, \
    MeasurementPatchRequestSchema, SearchRequestSchema
from app.measurements.services.service import MeasurementService


@measurement_bp.get('')
def get_all():
    data = SearchRequestSchema().load(request.args.to_dict())

    measurements = MeasurementService().get_all(data=data)

    if data.get('all'):
        return MeasurementResponseSchema(many=True).dumps(measurements)
    else:
        return PaginationResultSchema().dump(measurements)


@measurement_bp.post('')
def create():
    data = MeasurementPostRequestSchema().load(request.json)

    measurement = MeasurementService().create(post_data=data)

    return MeasurementResponseSchema().dumps(measurement)


@measurement_bp.get('/<int:id>')
def get_id(id):
    measurement = MeasurementService().get_by_id(id=id)

    return MeasurementResponseSchema().dumps(measurement)


@measurement_bp.patch('/<int:id>')
def patch_id(id):
    patch_data = MeasurementPatchRequestSchema().load(request.json)

    measurement = MeasurementService().patch(id=id, patch_data=patch_data)

    return MeasurementResponseSchema().dumps(measurement)


@measurement_bp.get('/latest')
def get_latest():
    measurement = MeasurementService().get_latest()

    return MeasurementResponseSchema().dumps(measurement)
