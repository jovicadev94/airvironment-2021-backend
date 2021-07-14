from app import app
from flask import render_template
from app import db
from app.measurements.models import Measurement

lista = [
    {
        "temperature": 25
    },
    {
        "temperature": 35
    }
]

@app.route("/")
def hello_world():
    temperature_list = db.session.query(Measurement).all()
    return render_template("home.html", asd=temperature_list)