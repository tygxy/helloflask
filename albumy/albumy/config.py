import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    ALBUMY_ADMIN_USERNAME = 'admin'

    ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    ALBUMY_PHOTO_SIZE = {'small':400, 'medium': 800}
    ALBUMY_PHOTO_SUFFIX = {
        ALBUMY_PHOTO_SIZE['small']: '_s',
        ALBUMY_PHOTO_SIZE['medium']: '_m',
    }
    ALBUMY_PHOTO_PER_PAGE = 12
    ALBUMY_COMMENT_PER_PAGE = 10
    ALBUMY_USER_PER_PAGE = 10
    ALBUMY_NOTIFICATION_PER_PAGE = 20
    ALBUMY_SEARCH_RESULT_PER_PAGE = 10
    ALBUMY_MANAGE_USER_PER_PAGE = 10
    ALBUMY_MANAGE_PHOTO_PER_PAGE = 10
    ALBUMY_MANAGE_TAG_PER_PAGE = 10
    ALBUMY_MANAGE_COMMENT_PER_PAGE = 10


    AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
    AVATARS_SAVE_TUPLE = (30, 100, 30)

    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_ENABLE_CSRF = True

    MAX_CONTENT_FILES = 3 * 1024 * 1024
    WHOOSHEE_MIN_STRING_LEN = 1


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


config = {
    'development': DevelopmentConfig
}
