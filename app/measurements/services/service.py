from sqlalchemy import func, desc

from app import db
from app.measurements.models import Measurement
from werkzeug.exceptions import NotFound


class MeasurementService:
    @staticmethod
    def get_by_id(id):
        measurement = db.session.query(Measurement).\
            filter(Measurement.id == id).\
            one_or_none()

        if not measurement:
            raise NotFound(description=f"Measurement with id {id} not found")

        return measurement

    @staticmethod
    def get_all(data):
        group_by = data.get('group_by')
        all = data.get('all')
        order_by = data.get('order_by', 'created')
        direction = data.get('direction', 'asc')

        subquery = db.session.query(func.min(Measurement.id).label('id')) \
            .group_by(func.date_trunc(group_by, Measurement.created)) \
            .order_by(func.date_trunc(group_by, Measurement.created)) \
            .subquery()

        measurements = db.session.query(Measurement)

        if data.get('date_from'):
            measurements = measurements.\
                filter(Measurement.created >= data['date_from'])

        if data.get('date_to'):
            measurements = measurements.\
                filter(Measurement.created <= data['date_to'])

        if data.get('humidity_from'):
            measurements = measurements.\
                filter(Measurement.humidity >= data['humidity_from'])

        if data.get('humidity_to'):
            measurements = measurements.\
                filter(Measurement.humidity <= data['humidity_to'])

        if data.get('temperature_from'):
            measurements = measurements.\
                filter(Measurement.temperature >= data['temperature_from'])

        if data.get('temperature_to'):
            measurements = measurements.\
                filter(Measurement.temperature <= data['temperature_to'])

        if data.get('pollution_from'):
            measurements = measurements.\
                filter(Measurement.pollution >= data['pollution_from'])

        if data.get('pollution_to'):
            measurements = measurements.\
                filter(Measurement.pollution <= data['pollution_to'])

        if direction == 'asc':
            measurements = measurements.order_by(order_by)
        else:
            measurements = measurements.order_by(desc(order_by))

        if all:
            return measurements \
                .join(subquery, subquery.c.id == Measurement.id) \
                .all()
        else:
            return measurements \
                .join(subquery, subquery.c.id == Measurement.id)\
                .paginate(page=data['page'],
                          per_page=data['per_page'])

    @staticmethod
    def get_latest():
        measurement = db.session.query(Measurement).\
            order_by(Measurement.id.desc()).\
            first()

        if not measurement:
            raise NotFound(description=f"No measurement found")

        return measurement

    @staticmethod
    def create(post_data):
        measurement = Measurement(pollution=post_data['pollution'],
                                  temperature=post_data['temperature'],
                                  humidity=post_data['humidity'])
        db.session.add(measurement)
        db.session.commit()

        return measurement

    def patch(self, id, patch_data):
        measurement = self.get_by_id(id=id)

        if 'pollution' in patch_data:
            measurement.pollution = patch_data['pollution']
        if 'temperature' in patch_data:
            measurement.temperature = patch_data['temperature']
        if 'humidity' in patch_data:
            measurement.humidity = patch_data['humidity']

        db.session.commit()

        return measurement
