from app import db
from sqlalchemy import func


class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    pollution = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime(timezone=True), nullable=False,
                        server_default=func.now())

    def __init__(self, pollution, humidity, temperature):
        self.pollution = pollution
        self.humidity = humidity
        self.temperature = temperature

    def __repr__(self):
        return f"Temperature: {self.temperature}; Humidity: {self.humidity}; "\
               f"Pollution: {self.pollution}"
