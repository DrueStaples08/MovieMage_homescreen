# Logout function: sends user back to login/signup screen
from flask import Flask, redirect, url_for, request, render_template

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_restx import Api, Resource, fields, apidoc
from flasgger import Swagger
# import sys
# sys.path.append('../login_signp/templates/index.html')
# from lib.gcp import user_login, user_signup, client

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lib/movie-grader-394211-4edbebb0a607.json"
TABLE_NAME = os.getenv('TABLE_NAME')
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    # render_template("../templates/index.html")
    return render_template("index.html")

    # return {'greet': "hello"}    


@app.route("/logout", methods=["GET"])
def logout():
    # return redirect(url_for("../../login_signp/templates/index.html"))
    # return redirect(url_for("index.html"))
    return render_template("../login_signp/templates/index.html")
# /Users/druestaples/projects/movie_app/movie_app_1/login_signup/templates/index.html


@app.route('/search', methods=["POST"])
def search():
    query = request.form['search-query']
    return query


@app.route('/my_movies', methods=["GET"])
def my_movies():
    pass
    # connect with biquery table to extract movies that a specied user has graded. 




if __name__ == "__main__":
    app.run(debug=True)