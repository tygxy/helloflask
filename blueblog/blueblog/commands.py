# coding=utf-8
import click

from blueblog.extensions import db
from blueblog.models import Admin, Category


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        from blueblog.fakes import fake_admin, fake_categories, fake_comments, fake_posts

        db.drop_all()
        db.create_all()

        click.echo("Generating the admin...")
        fake_admin()

        click.echo("Generating %d categories..." % category)
        fake_categories(category)

        click.echo("Generating %d posts..." % post)
        fake_posts(post)

        click.echo("Generating %d comments..." % comment)
        fake_comments(comment)

        click.echo("Done.")

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    @click.option('--post', default=30, help='Quantity of posts, default is 30.')
    @click.option('--comment', default=50, help='Quantity of comments, default is 50.')
    def init(username, password, post, comment):
        click.echo("Initializing the databases...")

        db.drop_all()
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo("Admin already exists, updating...")
            admin.username = username
            admin.set_password(password)
        else:
            click.echo("Creating the admin account...")
            admin = Admin(
                username=username,
                blog_title='北邮郭大宝',
                blog_sub_title="专注大数据、机器学习",
                name="Admin",
                about='专注Python技术栈'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo("Creating the default category...")
            category = Category(name='默认')
            db.session.add(category)
        db.session.commit()

        from blueblog.fakes import fake_posts, fake_comments

        click.echo("Generating %d posts..." % post)
        fake_posts(post)

        click.echo("Generating %d comments..." % comment)
        fake_comments(comment)

        click.echo("Done.")
