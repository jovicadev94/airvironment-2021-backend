from werkzeug.exceptions import NotFound
from app import db
from app.measurements import measurement_bp
from app.measurements.models import Measurement
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE
from app.measurements.shemas import MeasurementResponseSchema, MeasurementPostSchema, MeasurementPatchSchema,\
    MeasurementGetLatestSchema, MeasurementMetaSchema, MeasurementPaginationSchema

measurement_response_schema = MeasurementResponseSchema()
measurement_collection_response_schema = MeasurementResponseSchema(many=True)
measurement_post_schema = MeasurementPostSchema()
measurement_patch_schema = MeasurementPatchSchema()
measurement_getlatest_schema= MeasurementGetLatestSchema()
measurement_meta_schema = MeasurementMetaSchema()
measurement_pagination_schema = MeasurementPaginationSchema()


@measurement_bp.get('')
def get_all():
    # page = int(request.args.get("page", PAGE))
    # per_page = int(request.args.get("per_page", PER_PAGE))
    schema_load = measurement_meta_schema.load(request.args.to_dict())
    measurements = db.session.query(Measurement).paginate(page=schema_load.get('page'),
                                                          per_page=schema_load.get('per_page'))
    # measurements = db.session.query(Measurement).paginate(page=page, per_page=per_page)

    # response = {"meta": {"total": measurements.total,
    #                      "page": measurements.page,
    #                      "per_page": measurements.per_page},
    #             "results": []}
    # a = 1
    # all = request.args.get('all')
    # if all:
    #     return {"asdf": 1}
    # measurements = db.session.query(Measurement).all()
    # list_of_measurements = []
    #
    # for measurement in measurements.items:
    #     data = {"id": measurement.id,
    #             "temperature": measurement.temperature,
    #             "pollution": measurement.pollution,
    #             "humidity": measurement.humidity}
    #     response['results'].append(data)
    # return  json.dumps(response)

    return measurement_pagination_schema.dumps(measurements)

@measurement_bp.get('/<int:id>')
def get_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
    if not measurement:
        return NotFound(description=f"Measurement with {id} doesn't exists.")
    # if measurement:
    #     data = {"id": measurement.id,
    #             "temperature": measurement.temperature,
    #             "pollution": measurement.pollution,
    #             "humidity": measurement.humidity}
    return measurement_response_schema.dump(measurement)


@measurement_bp.get('/latest')
def get_latest():
    measurement = db.session.query(Measurement).order_by(Measurement.id.desc()).first()
    if measurement:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
    return measurement_response_schema.dump(measurement)

@measurement_bp.post('')
def insert():
    data = request.json
    var = measurement_post_schema.load(data)
    measurement = Measurement(var.temperature, var.pollution, var.humidity)
    db.session.add(measurement)
    db.session.commit()
    # data = {"id": measurement.id,
    #         "temperature": measurement.temperature,
    #         "pollution": measurement.pollution,
    #         "humidity": measurement.humidity}
    return measurement_response_schema.dump(measurement)


@measurement_bp.patch('/<int:id>')
def patch(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
    if not measurement:
        return NotFound(description=f"Measurement with {id} doesn't exists")

    data = request.json

    var = measurement_patch_schema.load(data)

    if var.get('temperature'):
        measurement.temperature = var['temperature']
    if var.get('pollution'):
        measurement.pollution = var['pollution']
    if var.get('humidity'):
        measurement.humidity = var['humidity']
    # data = {"id": measurement.id,
    #         "temperature": measurement.temperature,
    #         "pollution": measurement.pollution,
    #         "humidity": measurement.humidity}
    db.session.add(measurement)
    db.session.commit()
    return measurement_response_schema.dumps(measurement)



