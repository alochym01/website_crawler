from flask_app import app, db
from flask_app.models.youtube import YOUTUBE
from flask_app.models.packtpub import PACKTPUB
from flask_app.models.vtv import VTV
from flask_migrate import Migrate
import click

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, VTV=VTV, YOUTUBE=YOUTUBE, PACKTPUB=PACKTPUB)


@app.cli.command(with_appcontext=True)
def create_admin():
    """Creates the admin user."""
    click.echo(db)
    # db.session.add(User(
    #     email="ad@min.com",
    #     password="admin",
    #     username="admin"
    # )
    # db.session.commit()


# if __name__ == '__main__':
#     create_admin()
