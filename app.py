# Logout function: sends user back to login/signup screen
from flask import Flask, redirect, url_for, request, render_template, jsonify

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_restx import Api, Resource, fields, apidoc
from flasgger import Swagger
from lib.gcp import search_all_movies
# import sys
import sys
from os.path import abspath, dirname
# sys.path.append('../login_signp/templates/index.html')
# from ..login_signup.app import index as login_index
# sys.path.insert(0, abspath(dirname(__file__)))


# from lib.gcp import user_login, user_signup, client

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
USER_TABLE_NAME = os.getenv('USER_TABLE_NAME')



# app = Flask(__name__, template_folder='../templates')
# app = Flask(__name__, template_folder='../templates', static_folder='../static')
app = Flask(__name__, static_folder='static', template_folder='templates')



@app.route("/")
def login_signup_index():
    return render_template('login_signup_index.html')
    # return redirect(url_for("login_post"))

@app.route("/homepage")
def homepage():
    return render_template("index.html")


@app.route("/logout", methods=["GET"])
def logout():
    return redirect(url_for("login_signup_index"))

    # return redirect(url_for(".../login_signp/templates/index"))
    # return render_template("../login_signp/templates/index.html")
    # return render_template('login_signup/login.html')
    # return redirect(url_for("index.html"))
    # return render_template("/login_signup/templates/index.html")
    # return render_template("/Users/druestaples/projects/movie_app/movie_app_1/login_signup/templates/index.html")    
    return {'greet': "helloeeeee"}    
       # Construct the absolute file system path to the template
    # template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../login_signup/templates/index.html'))
    
    # Render the template using the absolute path
    # return render_template(template_path)

# /Users/druestaples/projects/movie_app/movie_app_1/login_signup/templates/index.html


@app.route('/search', methods=["POST"])
def search():
    query = request.form['search-query']
    search_query = search_all_movies(query)
    # return search_query
    return jsonify(results=search_query)



@app.route('/my_movies', methods=["GET"])
def my_movies():
    pass
    # connect with biquery table to extract movies that a specied user has graded. 
































# # Initialize Flask-RESTx API
# api = Api(app, version='1.0', title='Login/Signup API', description='API includes the get and post requests for user login and signup')

# # Namespace for the API
# # ns = api.namespace('login-signup-op', description='Login and Signup Operations')
# # Create a namespace (a container for routes)
# ns = api.namespace('sample', description='Sample Namespace')




# login_model = api.model('LoginModel', {
#     'email': fields.String(description='User email', required=True),
#     'password': fields.String(description='User password', required=True)
# })


@app.route('/success/<string:username>')
def success(username):
    return f"Welcome, {username}!"

@app.route('/login_fail')
def login_fail():
    return render_template('login_signup_index.html', login_failed=True)


@app.route('/signup_fail')
def signup_fail():
    return render_template('login_signup_index.html', signup_failed=True)
    # redirect("http://127.0.0.1:5000/signup_fail#")
    # return render_template('index.html/signup_fail', signup_failed=True)


@app.route("/login_post", methods=["POST"], endpoint='login_post')
def login_post():
    c = client()
    email = request.form['login-username']
    password = request.form['login-password']
    user_in_database = user_login(c, email, password)
    if user_in_database:
        # return redirect(url_for('success', username=email)) # redirect to home page
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login_fail'))

@app.route("/signup_post", methods=['POST'], endpoint='signup_post')
def signup_post():
    c = client()
    first_name = request.form['signup-firstname']
    last_name = request.form['signup-lastname']
    handle = request.form["signup-handlename"]
    email = request.form["signup-email"]
    dob = request.form["signup-dob"]
    phone_prefix = request.form["signup-phone-prefix"]
    phone_number = request.form["signup-phone-number"]
    ethnicity = request.form["signup-ethnicity"]
    race = request.form["signup-race"]
    gender = request.form["signup-gender"]
    gender_identity = request.form["signup-gender-identity"]
    sexual_orientation = request.form["signup-sexual-orientation"]
    political_party = request.form["signup-political-party"]
    password = request.form["signup-password"]
    # confirm_password = request.form["signup-confirm-password"]
    result = user_signup(c, first_name, last_name, handle, email, dob, phone_prefix, phone_number, ethnicity, race, gender, gender_identity, sexual_orientation, political_party, password)
    if result == 'Signup Successful!':
        # return redirect(url_for('success', username=email))
        return redirect(url_for('homepage'))

    else:
        return redirect(url_for('signup_fail'))

if __name__ == '__main__':
    app.run(debug=True)
