import configparser
import os
from .logger import logger

CONFIG_FILE = os.path.expanduser("~/.rotate_that_batch.ini")

def load_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'default_angle': '90',
        'default_directory': '.',
        'output_directory': ''
    }
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        logger.info(f"Loaded configuration from {CONFIG_FILE}")
    else:
        logger.info(f"No configuration file found. Using default settings.")
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    logger.info(f"Saved configuration to {CONFIG_FILE}")

def get_config_value(key, default=None):
    config = load_config()
    return config['DEFAULT'].get(key, default)

def set_config_value(key, value):
    config = load_config()
    config['DEFAULT'][key] = str(value)
    save_config(config)
    logger.info(f"Updated configuration: {key} = {value}")
