import os
from flask_caching import Cache

CACHE_CONFIG = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}


def initialise_cache(app):
    print(os.environ.get('CACHE_CONFIG'))
    app.config.from_mapping(CACHE_CONFIG)
    cache = Cache(app)
    return cache
