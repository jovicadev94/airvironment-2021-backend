from app import app
from flask import render_template

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

    return render_template("home.html", asd=lista)