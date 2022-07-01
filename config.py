import os.path

base_dir = os.path.dirname(__file__)


class Config(object):
    secret_key = "kfdsjfjfkdslfjksd"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sdfFSDSDFfdas'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data.db')
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data.db')


config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}
