from flask import Flask
from flask_caching import Cache
from playhouse.flask_utils import FlaskDB
from playhouse.pool import PooledPostgresqlDatabase

import config

DATABASE = PooledPostgresqlDatabase(**config.dbauth)

if config.sentryDSN:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=config.sentryDSN,
        integrations=[FlaskIntegration()]
    )

CACHE_TYPE = "RedisCache"

if config.production:
    CACHE_REDIS_URL = "unix:///run/redis-crsearch/redis-server.sock"

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(app)
flask_db = FlaskDB(app)

db = flask_db.database
