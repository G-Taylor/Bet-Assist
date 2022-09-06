from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


def initialise_cache(app):
    app.config.from_mapping(config)
    cache = Cache(app)
    return cache

