from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app,
            resources={
                r"/api/*": {
                    "origins": "*"
                }
            },
            supports_credentials=True)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.measurements import measurement_bp

app.register_blueprint(measurement_bp)
