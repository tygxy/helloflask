import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    BLUEBLOG_EMAIL = '574232205@qq.com'

    BLUEBLOG_POST_PER_PAGE = 10
    BLUEBLOG_COMMENT_PER_PAGE = 15
    BLUEBLOG_MANAGE_POST_PER_PAGE = 30
    BLUEBLOG_MANAGE_CATEGORY_PER_PAGE = 10
    BLUEBLOG_MANAGE_COMMENT_PER_PAGE = 30

    BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-dev.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}