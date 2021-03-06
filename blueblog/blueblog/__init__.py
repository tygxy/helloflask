import os
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError


from blueblog.blueprints.admin import admin_bp
from blueblog.blueprints.auth import auth_bp
from blueblog.blueprints.blog import blog_bp
from blueblog.commands import register_commands
from blueblog.config import config
from blueblog.extensions import bootstrap, db, moment, login_manager, csrf, ckeditor
from blueblog.models import Admin, Category, Comment


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('blueblog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_logging(app)
    register_shell_context(app)
    register_errors(app)
    register_template_context(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_logging(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments)
