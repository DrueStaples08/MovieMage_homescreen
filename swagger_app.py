import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_restx import Api, Resource, fields, apidoc
from flasgger import Swagger
# import sys
# sys.path.append('../lib/')
from lib.gcp import user_login, user_signup, client

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lib/movie-grader-394211-4edbebb0a607.json"
TABLE_NAME = os.getenv('TABLE_NAME')
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


app = Flask(__name__)




# Initialize Flask-RESTx API
api = Api(app, version='1.0', title='Login/Signup API', description='API includes the get and post requests for user login and signup')

# Namespace for the API
# ns = api.namespace('login-signup-op', description='Login and Signup Operations')
# Create a namespace (a container for routes)
ns = api.namespace('sample', description='Sample Namespace')




login_model = api.model('LoginModel', {
    'email': fields.String(description='User email', required=True),
    'password': fields.String(description='User password', required=True)
})

@ns.route("/login_post_swagger/<string:email>/<string:password>", methods=["POST"]) # remove get
class UserLoginSwagger(Resource):
    # @api.expect(login_model)
    def post(self, email, password): # change to post
        c = client()
        user_in_database = user_login(c, email, password)
        if user_in_database:
            return 'Success'
        else:
            return 'There is no account present'
        

@ns.route("/signup_post_swagger/<string:first_name>/<string:last_name>/<string:handle>/<string:email>/<string:dob>/<string:phone_prefix>/<string:phone_number>/<string:ethnicity>/<string:race>/<string:gender>/<string:gender_identity>/<string:sexual_orientation>/<string:political_party>/<string:password>", methods=["POST"])
class UserSignup(Resource):
    def post(self, first_name, last_name, handle, email, dob, phone_prefix, phone_number, ethnicity, race, gender, gender_identity, sexual_orientation, political_party, password):
        c = client()
        result = user_signup(c, first_name, last_name, handle, email, dob, phone_prefix, phone_number, ethnicity, race, gender, gender_identity, sexual_orientation, political_party, password)
        return result



if __name__ == '__main__':
    app.run(debug=True, port=5001)