from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json()
        print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                # print('gothere1')
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # print('gothere2')
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                # print('gothere3')
                auth_token = user.encode_auth_token(user.id)
                print(auth_token)
                # print('gothere4')
                
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                # print('done')
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                # print('exceptuion')
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)


# code for my registered users
"""
class IndexAPI(MethodView):
    
    #User Registration Resource
    

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Gotten but need to print it out.'
        }
        get_data = request.get_json(); print(request)
        # check if user already exists
        try:
            user = User.query.filter_by(email=get_data.get('email')).first()
            return make_response(jsonify(user)), 201
            
        except:
            #return "<p>No such user exists<p>"
            return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json(); print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                # Here I need to send the user data to /users/index
            
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

list_users_view = IndexAPI.as_view('index_api')
auth_blueprint.add_url_rule(
    '/users/index',
    view_func=list_users_view,
    methods=['GET']
)


from flask_marshmellow import Marshmellow
ma = Marshmellow(app)
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

@app.route('/users/index')
def index():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.data
    return jsonify(output)
    
"""
