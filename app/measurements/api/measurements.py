from werkzeug.exceptions import NotFound
from app import db
from app.measurements import measurement_bp
from app.measurements.models import Measurement
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE

@measurement_bp.get('')
def get_all():
    page = int(request.args.get("page", PAGE))
    per_page = int(request.args.get("per_page", PER_PAGE))
    measurements = db.session.query(Measurement).paginate(page=page, per_page=per_page)

    response = {"meta": {"total": measurements.total,
                         "page": measurements.page,
                         "per_page": measurements.per_page},
                "results": []}
    a = 1
    # all = request.args.get('all')
    # if all:
    #     return {"asdf": 1}
    # measurements = db.session.query(Measurement).all()
    # list_of_measurements = []
    #
    for measurement in measurements.items:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
        response['results'].append(data)
    return  json.dumps(response)

@measurement_bp.get('/<int:id>')
def get_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
    if not measurement:
        return NotFound(description=f"Measurement with {id}")
    if measurement:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
    return data

@measurement_bp.get('/latest')
def get_latest():
    measurement = db.session.query(Measurement).order_by(Measurement.id.desc()).first()
    if measurement:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
    return data

@measurement_bp.post('')
def insert():
    data = request.json
    measurement = Measurement(data['temperature'], data['pollution'], data['humidity'])
    db.session.add(measurement)
    db.session.commit()
    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    return json.dumps(data)


@measurement_bp.patch('/<int:id>')
def patch(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).first()
    if not measurement:
        return NotFound(description=f"Measurement with {id} doesn't exists")

    data = request.json
    if data.get('temperature'):
        measurement.temperature = data['temperature']
    if data.get('pollution'):
        measurement.pollution = data['pollution']
    if data.get('humidity'):
        measurement.humidity = data['humidity']
    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    db.session.add(measurement)
    db.session.commit()
    return json.dumps(data)



