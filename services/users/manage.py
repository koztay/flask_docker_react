import coverage
import unittest

from flask.cli import FlaskGroup


from project import create_app, db
from project.api.models import User


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=['project/tests/*', 'project/config.py']
)

COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def seed_db():
    """Seeds the database"""
    db.session.add(User(
        username="blabla",
        email="blahablaha@fuckyou.com",
        password="1234abcd"))
    db.session.add(User(
        username="daget",
        email="dagetlaordan@uzayavrum.com",
        password="1234bcda"))
    db.session.commit()


if __name__ == '__main__':
    cli()
