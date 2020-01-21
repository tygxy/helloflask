from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_dropzone import Dropzone
from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_whooshee import Whooshee

avatars = Avatars()
bootstrap = Bootstrap()
csrf = CSRFProtect()
ckeditor = CKEditor()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
dropzone = Dropzone()
whooshee = Whooshee()


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False


login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login in first'
login_manager.login_message_category = 'warning'
login_manager.anonymous_user = Guest
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message_category = 'warning'
