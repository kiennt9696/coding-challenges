import os
from os import path
import logging
import logging.config
import connexion
# from flask_cors import CORS
from werkzeug.exceptions import default_exceptions

from quiz import extensions
from quiz.exceptions import api_error_handler
from helpers.util import load_config


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
APPLICATION_ROOT = os.path.join(MODULE_DIR, '..')

app_config = None
if app_config is None:
    config_file = os.path.join(APPLICATION_ROOT, 'config.yaml')
    if os.path.isfile(config_file):
        app_config = load_config(config_file)
    else:
        raise Exception('No valid configuration found')


def create_app(config=None):
    """ Create an Flask application instance.

    :param config:
    :return:
    """

    if not config:
        config = app_config
    app = connexion.App(__name__, specification_dir="./openapi/")
    app.add_api("swagger.yaml", arguments={"title": "files"})

    flask_app = app.app
    flask_app.config.from_mapping(config)
    flask_app.config['SECRET_KEY'] = os.urandom(24)
    flask_app.instance_path = MODULE_DIR

    configure_app(flask_app)

    return app


def configure_app(app):
    """
    Configure a Flask app
    :param app:
    :param filename:
    :return:
    """
    configure_log_handlers(app)
    configure_extensions(app)
    configure_exception_handlers(app)


def configure_log_handlers(app):
    """
    Config log
    :param app: flask app
    :return: not return
    """
    log_file_path = path.join(path.dirname(path.abspath(__file__)), "..", app.config['LOGGER_CONFIG_PATH'])
    logging.config.fileConfig(log_file_path)

    logger = logging.getLogger('root')

    # unify log format for all handlers
    for h in logger.root.handlers:
        app.logger.addHandler(h)
    app.logger.setLevel(logger.root.level)

    app.logger.info('Start api services info log')
    app.logger.error('Start api services error log')


def configure_extensions(app):
    """
    :param app: flask app (main app)
    :return:
    """
    extensions.action_logger.init_app(app, logging.getLogger('action'))
    extensions.redis_client.init_app(app)


def configure_exception_handlers(app):
    for exception in default_exceptions:
        app.register_error_handler(exception, api_error_handler)
    app.register_error_handler(Exception, api_error_handler)