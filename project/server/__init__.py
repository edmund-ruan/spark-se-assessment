import os
import sys

if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(
        branch=True,
        include='project/*',
        omit=[
            'project/tests/*',
            'project/server/config.py',
            'project/server/*/__init__.py'
        ]
    )
    COV.start()

import click
from flask import Flask, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.models import User
migrate = Migrate(app, db)

@app.route("/")
def root_site():
    return "<p>It works!</p>"

from project.server.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

#my code here for new route

"""
from flask_marshmallow import Marshmallow
from flask import jsonify
ma = Marshmallow(app)
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

@app.route("/users/index")
def index_site():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.data
    return jsonify(output)

"""

import json
from json import JSONEncoder

@app.route("/users/test", methods=['GET'])
def test_url():
    #for user_item in db.session:
        #print(user_item.email)
    #User.query.all()
    #for u in User.query.all():
        #print(u.__dict__)
    #user_list = User.query.all()
    #return "<p>It works for TESTING!</p>"
    #class EmployeeEncoder(JSONEncoder):
        #def default(self, o):
            #return o.__dict__
    #return EmployeeEncoder().encode(user_list)
    #return jsonify(user_list)
    #return User
    result = db.session.query(User).all()
    data = '{"users":['
    #temp_dict = dict({"users":{"admin":"adminval", "email":"emailval", "id": "idval", "registered_on": "r_val"}})
    for row in result:
        print("admin: ",row.admin)
        print("email: ",row.email)
        print("id: ",row.id)
        print("registered_on: ",row.registered_on)
        print()

        current_item = {"admin: ":row.admin,
            "email: ":row.email,
            "id: ":row.id,
            "registered_on: ":row.registered_on}
        #temp_dict["users"].update(current_item)
        s = json.dumps(current_item, indent=4, sort_keys=True, default=str)
        data += s + ","
    data=data[:-1]
    data += "]}"
    return data
    
    


#
@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
                help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        if COV:
            COV.stop()
            COV.save()
            print('Coverage Summary:')
            COV.report()
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)
            print('HTML version: file://%s/index.html' % covdir)
            COV.erase()
        return 0
    return 1
