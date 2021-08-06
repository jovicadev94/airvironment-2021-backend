# RBT Summer Internship 2021 Backend

Backend code written in Python-Flask for Airvironment 2021 Summer internship.

Running applications are live on
`https://airvironment.live` and `https://airvironment.dev`

PostgreSQL is used to store data and it should be installed in order to run
the application locally. Instructions on how to install PostgreSQL depend on
 the Operating System. Further instructions can be
found [here](https://www.postgresql.org/download/).
After installing and starting PostgreSQL, a user, along with a database,
should be created.
```bash
psql postgres
create database <database_name>;
create user <user_name> with encrypted password <password>;
grant all privileges on database <database_name> to <user_name>;
```

The application can be started locally in developer mode by running:

```bash
python3 run.py
```

or in production mode by running following commands:

```bash
export FLASK_APP=run.py
flask run
```

Before running the project, a `.env` file should be created in the root
directory with following key/values:

```
DEBUG=1
ENVIRONMENT="Development"
DATABASE_URL="postgresql+psycopg2://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>"
```

## Requests and Responses
GET /api/measurements
Query params:
```JSON
{
   "page": "Int, optional",
   "per_page": "Int, optional",
   "all": "Bool, optional",
   "group_by": "String, optional, allowed values: 'year', 'month', 'day', 'hour', default: 'hour'",
   "date_from": "DateTime, optional",
   "date_to": "DateTime, optional",
   "temperature_from": "Float, optional",
   "temperature_to": "Float, optional",
   "humidity_from": "Float, optional",
   "humidity_to": "Float, optional",
   "pollution_from": "Float, optional",
   "pollution_to": "Float, optional",
   "order_by": "String, optional, allowed values: 'created', 'temperature', 'humidity', 'pollution', default: 'created'",
    "direction": "String, optional, allowd values: 'asc', 'desc', default: 'asc'"
}
```

Response if all = True:
Response:
```JSON
[
    {
       "id": "Int",
       "pollution": "Float",
       "temperature": "Float",
       "humidity": "Float",
       "created": "DateTime"
    }
]

```

Response if all = False:
```JSON
{
   "meta": {
      "total": "Int",
      "page": "Int",
      "per_page": "Int",
      "has_next": "Bool"
   },
   "response": [
       {
          "id": "Int",
          "pollution": "Float",
          "temperature": "Float",
          "humidity": "Float",
          "created": "DateTime"
       }
   ]
}
```

POST /api/measurements
Post Request:
```JSON
{
   "pollution": "Float, required",
   "temperature": "Float, required",
   "humidity": "Float, required"
}
```

Response:
```JSON
{
   "id": "Int",
   "pollution": "Float",
   "temperature": "Float",
   "humidity": "Float",
   "created": "DateTime"
}
```

GET /api/measurements/latest
Response:
```JSON
{
  "id": "Int",
  "pollution": "Float",
  "temperature": "Float",
  "humidity": "Float",
  "created": "DateTime"
}

GET /api/measurements/<int: id>
Response:
```JSON
{
   "id": "Int",
   "pollution": "Float",
   "temperature": "Float",
   "humidity": "Float",
   "created": "DateTime"
}
```

PATCH /api/measurements/<int: id>
Post Request:
```JSON
{
   "pollution": "Float, optional",
   "temperature": "Float, optional",
   "humidity": "Float, optional"
}
```

Response:
```JSON
{
   "id": "Int",
   "pollution": "Float",
   "temperature": "Float",
   "humidity": "Float",
   "created": "DateTime"
}
```
