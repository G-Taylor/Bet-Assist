from flask_caching import Cache

CACHE_CONFIG = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

# SKY_SPORTS_CONFIG
SS_STRIPPED_TEAM_NAME = 'swap-text__target'
# "SS_HOME_TEAM": "matches__participant--side1"
# "SS_AWAY_TEAM": "matches__participant--side2",
# "SS_SCRAPE_RESULTS": "fixres__item",
# "SS_MATCH_INFO": "matches__item-col matches__info",
# "SS_MATCH_SCORES": "matches__teamscores-side",
# "SS_LEAGUE_TABLE": "standing-table__row",
# "SS_TABLE_TEAM_POSITION": "standing-table__cell",
# "SS_TABLE_TEAM_NAME": "standing-table__cell--name",


def initialise_cache(app):
    app.config.from_mapping(CACHE_CONFIG)
    cache = Cache(app)
    return cache

