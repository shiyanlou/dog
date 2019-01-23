import os

class BaseConfig:
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost?charset=utf8'
    
class TestConfig(BaseConfig):
    pass

configs = {
    'dev': DevelopConfig,
    'test': TestConfig
}
