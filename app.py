# Logout function: sends user back to login/signup screen
from flask import Flask, redirect, url_for, request, render_template, jsonify, session
import json
import secrets
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_restx import Api, Resource, fields, apidoc
from flasgger import Swagger
from lib.gcp import search_all_movies, extract_user_movie_grades, view_my_movies, user_update_grade_json
from lib.gcp import user_login, user_signup, client, search_my_movies, user_update_grade, update_user_table_with_new_grade

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lib/movie-grader-394211-4edbebb0a607.json"

TABLE_NAME = os.getenv('TABLE_NAME')
# CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
USER_TABLE_NAME = os.getenv('USER_TABLE_NAME')
MOVIE_TABLE_NAME = os.getenv('MOVIE_TABLE_NAME')
SECURE_COOKIES_TOKEN = os.getenv('SECURE_COOKIES_TOKEN')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = SECURE_COOKIES_TOKEN





### Login/Signup
# The Login and Signup Screen which is the first thing a user sees when they open app. 
@app.route("/")
def login_signup_index():
    return render_template('login_signup_index.html')

# Homepage for application once a user logs in or signs up
@app.route("/homepage")
def homepage():
    return render_template("index.html")

# Logs user out of app and sends them back to homepage
@app.route("/logout", methods=["GET"])
def logout():
    return redirect(url_for("login_signup_index"))

# Will display if the user's requested login information is incorrect e.g. email or password
@app.route('/login_fail')
def login_fail():
    return render_template('login_signup_index.html', login_failed=True)

# Will display if the user's requested signup information is incorrect e.g. no birthdate, user already in database i.e existing email
@app.route('/signup_fail')
def signup_fail():
    return render_template('login_signup_index.html', signup_failed=True)

# User logs into app
@app.route("/login_post", methods=["POST"], endpoint='login_post')
def login_post():
    c = client()
    email = request.form['login-username']
    password = request.form['login-password']
    session['email'] = email
    session['password'] = password
    user_in_database = user_login(c, email, password)
    if user_in_database:
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login_fail'))

# User signs up for app
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
    session['email'] = email
    session['password'] = password
    result = user_signup(c, first_name, last_name, handle, email, dob, phone_prefix, phone_number, ethnicity, race, gender, gender_identity, sexual_orientation, political_party, password)
    if result == 'Signup Successful!':
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('signup_fail'))





### Search/My Movies     
# Search: direct query matching to search for any movie in the BQ table which itself will display as a table in the front end
# Today: Update a user grade and save it to the user table 
# Todo: Update the movie votes, movie grade, and movie letter grade when a user grades a movie
@app.route('/search', methods=["POST", "GET"])
def search():
    email = session.get('email', 'No email found')
    password = session.get('password', 'No password found')
    # query = request.form.to_dict()['search-query']
    query = session.get('search-query')

    session['search-query'] = query

    search_result = search_all_movies(query)
    search_result = search_my_movies(search_result, email, password)


    return render_template("search_results_index_2.html", column_names=search_result['column_names'], values=search_result['values'])


    # the function works up till I change the grade and hit confirm, then it doesn't recognize the search-query key. 
    # this is because hitting confirm connects to this search function but since nothing is being searched
    # when a grade is being changed, we get a KeyError. 

    # data = request.form.get('change_movie_grade')
    # print(data)
    # x = request.form.get('movie_title')
    # print(x)


# search_result, 'The Kid', 'good'
# Search update should activate when a user hits the confirm button 
# search result contains the old info so this wont hold the new updated grade
# def search_update(query: str,  title: str, new_grade: str)->bool:
#     # Change and Save Grade !!!!!!!!! IMPORTANT
#     email = session.get('email', 'No email found')
#     password = session.get('password', 'No password found')
#     search_result = search_all_movies(query)
#     search_result = search_my_movies(search_result, email, password)
#     user_new_grade_dict = user_update_grade(search_result, title, new_grade) 
#     user_new_grade_json = user_update_grade_json(user_new_grade_dict, email, password)
#     update_user_table_with_new_grade(user_new_grade_json, email, password)
#     movie_grade_change_confirmed()
#     search_result
#     return render_template("search_results_index_2.html", column_names=search_result['column_names'], values=search_result['values'])



# app.route('/update_grade', methods=['POST'], endpoint='update_grade')
# def movie_grade_change_confirmed():
#     new_grade_confirmation = request.form
#     print(new_grade_confirmation, '*****************************')
#     # return jsonify(new_grade_confirmation)


@app.route('/update_grade', methods=['GET', 'POST'])
def update_grade():
    email = session.get('email', 'No email found')
    password = session.get('password', 'No password found')
    user_updated_grade = request.form.get('grade')
    row_data = json.loads(request.form.get('row_data'))
    query = session.get('search-query')
    movie_id = session.get('movie_id')
    movie_title = row_data[0]
    # print('!!!!!!!!!!!!!!!!!!!!!!Xxxxxsssssssssssssssss', row_data, query, movie_id, user_updated_grade)
    # return jsonify(
    #     {'new_grade': 
    #      {'updated_user_grade': user_updated_grade, 
    #      'row_data': row_data,
    #     'search_query': query
    #     }
    #     }
                    # )
    # return redirect(url_for('homepage'))
    # update the movie_database here 

    search_result = search_all_movies(query)
    search_result = search_my_movies(search_result, email, password)
    # user_new_grade_dict = user_update_grade(search_result, 'The Kid', 'good') 
    user_new_grade_dict = user_update_grade(search_result, movie_title, user_updated_grade) 

    user_new_grade_json = user_update_grade_json(user_new_grade_dict, email, password)
    movie_id = user_new_grade_dict.popitem()[0]
    session['movie_id'] = movie_id
    update_user_table_with_new_grade(user_new_grade_json, email, password)
    return redirect(url_for('search', query=query))   
    # return redirect(url_for("search"))
        # try:
        #     movie_id = request.form.get('movie_id')
        #     new_grade = request.form.get('grade')
        #     # movie_title = request.form.get('title')
        #     # new_grade = request.form.get('grade')
        #     # return jsonify({movie_title: new_grade})
        #     print(f"Movie ID: {movie_id}, New Grade: {new_grade}")

        #     print('update_grade here^^^^^^^^^^^^^^^^^^^')
        #     return jsonify({'message': f"Movie ID: {movie_id}, New Grade: {new_grade}"})
        # except Exception as e:
        #     # Handle exceptions appropriately (e.g., log the error)
        #     print(f"Error updating grade: {e}")
        #     return jsonify({'error': 'Failed to update grade'}), 500

# My Movies: return the graded movies and other quantitative data to be displayed in the front end
# Todo: Update the movie votes, movie grade, and movie letter grade when a user grades a movie
# @app.route('/my_movies', methods=["GET"])
# def my_movies():
#     email = session.get('email', 'No email found')
#     password = session.get('password', 'No password found')
#     res = extract_user_movie_grades(email, password)
#     result = view_my_movies(res)
#     return render_template("search_results_index.html", column_names=result['column_names'], values=result['values'])

# @app.route('/update_grade', methods=['POST'])
# def update_grade():
#     email = session.get('email', 'No email found')
#     password = session.get('password', 'No password found')
#     res = extract_user_movie_grades(email, password)
#     result = view_my_movies(res)
#     new_grade = request.form.get('newGrade')
#     movie_title = request.form.get('movieTitle')
#     return render_template("search_results_index_2.html", column_names=result['column_names'], values=result['values'])

@app.route('/my_movies', methods=["GET", "POST"])
def my_movies():
    email = session.get('email', 'No email found')
    password = session.get('password', 'No password found')
    res = extract_user_movie_grades(email, password)
    if request.method == "GET":
        result = view_my_movies(res)
        return render_template("search_results_index.html", column_names=result['column_names'], values=result['values'])
    if request.method == "POST":
        new_grade = request.form.get('newGrade')
        movie_title = request.form.get('movieTitle')
        #return render_template("search_results_index_2.html", column_names=result['column_names'], values=result['values'])




if __name__ == '__main__':
    app.run(debug=True)
