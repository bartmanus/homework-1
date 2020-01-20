from flask import Flask
from os import environ
from time import sleep


__DEFAULT_SECRET_KEY='development'
__DEFAULT_STARTUP_COALESCING_SECONDS=7

def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)
    # configure the app from various sources
    app.config.from_mapping(
        SECRET_KEY=environ['SECRET_KEY'] if 'SECRET_KEY' in environ else __DEFAULT_SECRET_KEY,
        STARTUP_COALESCING_SECONDS=int(environ['STARTUP_COALESCING_SECONDS']) \
            if 'STARTUP_COALESCING_SECONDS' in environ \
            else __DEFAULT_STARTUP_COALESCING_SECONDS,
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    if app.config['STARTUP_COALESCING_SECONDS'] < 5 \
        or app.config['STARTUP_COALESCING_SECONDS'] > 15:
        raise ValueError('coalesce time must be between 5 and 15 seconds')

    if test_config is None:
        print('> booting')
        # bits should be coalesced after this, amirite?
        sleep(int(app.config['STARTUP_COALESCING_SECONDS']))
        print('> booted')

    from . import dynamic
    app.register_blueprint(dynamic.bp)
    app.add_url_rule('/', endpoint='index')

    return app

