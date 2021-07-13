import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from app import db

from app.models import Measurement

def test():
    mm = Measurement(pollution=8.0, humidity=9.0, temperature=9.0)
    db.session.add(mm)
    db.session.commit()

if __name__ == "__main__":
    test()