import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello world'
    SQLALCHEMY_COMMIT_ON_TEAMDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevConfig(BaseConfig):
    # SERVER 和 PORT 是需要网上查的，各家的邮箱都不同
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    # 下面这俩通常这么设置
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # USERNAME 是发信人的邮箱，PASSWORD 是从邮箱那里获得的授权码
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')   # '1195581533@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')   # 'mhdccxqgqwcmhhfc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

class TestConfig(BaseConfig):
    pass

configs = {
    'dev': DevConfig,
    'test': TestConfig
}
