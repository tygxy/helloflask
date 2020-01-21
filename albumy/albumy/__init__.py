import click
import os

from flask import Flask
from flask_login import current_user

from albumy.blueprints.auth import auth_bp
from albumy.blueprints.admin import admin_bp
from albumy.blueprints.main import main_bp
from albumy.blueprints.user import user_bp
from albumy.blueprints.ajax import ajax_bp
from albumy.config import config
from albumy.extensions import bootstrap, ckeditor, csrf, moment, db, login_manager, dropzone, avatars, whooshee
from albumy.models import Role, Notification


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_template_context(app)
    return app


def register_extensions(app):
    avatars.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    dropzone.init_app(app)
    whooshee.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            notification_count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
        else:
            notification_count = None
        return dict(notification_count=notification_count)


def register_commands(app):
    @app.cli.command()
    def init():
        click.echo("creating database and tables...")
        db.drop_all()
        db.create_all()

        click.echo("Initializing the roles and permission...")
        Role.init_role()

        click.echo("Done...")
