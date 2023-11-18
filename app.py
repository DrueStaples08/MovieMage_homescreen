# Logout function: sends user back to login/signup screen
from flask import Flask, redirect, url_for, request, render_template, jsonify, session
import secrets
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_restx import Api, Resource, fields, apidoc
from flasgger import Swagger
from lib.gcp import search_all_movies, view_my_movies, view_my_movies_two
from lib.gcp import user_login, user_signup, client

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lib/movie-grader-394211-4edbebb0a607.json"

TABLE_NAME = os.getenv('TABLE_NAME')
# CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
USER_TABLE_NAME = os.getenv('USER_TABLE_NAME')
MOVIE_TABLE_NAME = os.getenv('MOVIE_TABLE_NAME')
SECURE_COOKIES_TOKEN = os.getenv('SECURE_COOKIES_TOKEN')
# secret_key = secrets.token_hex(16)  # 16 bytes gives a 32-character hex string


# app = Flask(__name__, template_folder='../templates')
# app = Flask(__name__, template_folder='../templates', static_folder='../static')
app = Flask(__name__, static_folder='static', template_folder='templates')
# app.secret_key = secret_key
app.secret_key = SECURE_COOKIES_TOKEN

@app.route("/")
def login_signup_index():
    return render_template('login_signup_index.html')
    # return redirect(url_for("login_post"))

@app.route("/homepage")
def homepage():
    # email = request.args.get('email')
    # password = request.args.get('password')
    # return render_template("index.html", column_names=my_movies['column_names'], values=my_movies['values'])
    return render_template("index.html")



@app.route("/logout", methods=["GET"])
def logout():
    return redirect(url_for("login_signup_index"))



@app.route('/search', methods=["POST"])
def search():
    query = request.form['search-query']
    result = search_all_movies(query)
    return render_template("search_results_index.html", column_names=result['column_names'], values=result['values'])



@app.route('/my_movies', methods=["GET"])
def my_movies():
    email = session.get('email', 'No email found')
    password = session.get('password', 'No password found')
    res = view_my_movies(email, password)
    result = view_my_movies_two(res)
    # return {'d': 'r'}
    # connect with biquery table to extract movies that a specied user has graded. 
    # return render_template("my_movies_index.html", column_names=result['column_names'], values=result['values'])
    return render_template("search_results_index.html", column_names=result['column_names'], values=result['values'])

    # USE A DIFFERENT HTML PAGE, one with movie title and column, and graded_movies should be the title, LOOK AT view_my_movies

































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
    # Store the information in the session
    session['email'] = email
    session['password'] = password
    user_in_database = user_login(c, email, password)
    if user_in_database:
        # user_movie_data = view_my_movies(c, email, password)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!extract the userId and the graded movies to be loaded into the my_movies page the moment a user logs in. 
        # return redirect(url_for('homepage', my_movies=user_movie_data))
        return redirect(url_for('homepage'))

    #     return render_template("index.html", column_names=my_movies['column_names'], values=my_movies['values'])

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
    # Store the information in the session
    session['email'] = email
    session['password'] = password
    # confirm_password = request.form["signup-confirm-password"]
    result = user_signup(c, first_name, last_name, handle, email, dob, phone_prefix, phone_number, ethnicity, race, gender, gender_identity, sexual_orientation, political_party, password)
    if result == 'Signup Successful!':
        # user_movie_data = view_my_movies(c, email, password)

        # return redirect(url_for('success', username=email))
        return redirect(url_for('homepage'))
        # return redirect(url_for('homepage', my_movies=user_movie_data))

    else:
        return redirect(url_for('signup_fail'))

if __name__ == '__main__':
    app.run(debug=True)
