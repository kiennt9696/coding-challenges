from quiz import create_app
import os

from helpers.util import load_config

config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
config = None
if os.path.isfile(config_file):
    config = load_config(config_file)

application = create_app()
