import os

from flask import Flask
from time import sleep


__DEFAULT_STARTUP_COALESCING_SECONDS=7

def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)
    # configure the app from various sources
    app.config.from_mapping(
        SECRET_KEY='development',
        STARTUP_COALESCING_SECONDS=str(__DEFAULT_STARTUP_COALESCING_SECONDS),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print('> booting')
    # bits should be coalesced after this, amirite?
    sleep(int(app.config['STARTUP_COALESCING_SECONDS']))
    print('> booted')

    from . import dynamic
    app.register_blueprint(dynamic.bp)
    app.add_url_rule('/', endpoint='index')

    return app

