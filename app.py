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

if config.production:
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "unix:///run/redis-crsearch/redis-server.sock"
else:
    CACHE_TYPE = "NullCache"

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__,static_folder='dist/assets/',static_url_path='/assets/')
app.config.from_object(__name__)
cache = Cache(app)
flask_db = FlaskDB(app)

db: PooledPostgresqlDatabase = flask_db.database
