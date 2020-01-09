from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
csrf = CSRFProtect()
ckeditor = CKEditor()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from blueblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login in first'
login_manager.login_message_category = 'warning'
