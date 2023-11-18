from google.cloud import bigquery
import os
import json
from dotenv import load_dotenv
import pandas as pd
import warnings

load_dotenv()

# GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "movie-grader-394211-4edbebb0a607.json"
TABLE_NAME = os.getenv('TABLE_NAME') 
USER_TABLE_NAME = os.getenv('USER_TABLE_NAME')
MOVIE_TABLE_NAME = os.getenv('MOVIE_TABLE_NAME')








# Search function: allows users to look up movies by title
def search_all_movies(query):
    c = client()
    query_statement = f'''SELECT * EXCEPT(movieID) FROM {MOVIE_TABLE_NAME} WHERE LOWER(movie_title) LIKE LOWER('%{query}%') '''
    result = c.query(query_statement)
    df = result.to_dataframe()
    column_names = df.keys()
    values = df.values.tolist()
    return {'column_names': column_names, 'values': values}


# Select all graded movies from a user and rank them by grade
def view_my_movies(email: str, password: str):
    c = client()
    QUERY = f"""SELECT graded_movies FROM {USER_TABLE_NAME} WHERE email = '{email}' and password = '{password}' """
    result = c.query(QUERY)
    # new_grade = {'1729da40-ab67-4149-836c-6519e99d0849': 'good'}
    graded_movies_dict = {}
    for row in result:
        graded_movies_json = row['graded_movies']
        graded_movies_dict = json.loads(graded_movies_json)
    # new_dict = {**graded_movies_dict, **new_grade}
    new_dict = graded_movies_dict
    movie_ids = list(new_dict.keys())
    movie_grades = list(new_dict.values())
    return {'column_names': movie_ids, 'values': movie_grades}


def view_my_movies_two(my_movies_dict: dict):
    c = client()
    movie_ids = my_movies_dict['column_names']
    movie_grades = my_movies_dict['values']
    title_movie = []
    year_release = []
    votes_movie = []
    grade_movie = []
    grade_letter_movie = []
    keys = []
    for m in movie_ids:
        QUERY = f"""SELECT * EXCEPT(movieId) FROM {MOVIE_TABLE_NAME} WHERE movieId = '{m}' """
        result = c.query(QUERY) 
        row = result.result().to_dataframe()
        # print(row)
        title_movie.append(row['movie_title'].item())
        year_release.append(row['release_year'].item())
        votes_movie.append(row['movie_votes'].item())
        grade_movie.append(row['movie_grade'].item())
        grade_letter_movie.append(row['movie_letter_grade'].item())
        keys.extend(list(row.keys()))
        # keys = list(row.keys())
    keys.append('my_grade')
    # df = pd.DataFrame([[title_movie], [year_release], [votes_movie], [grade_movie], [grade_letter_movie]],)
    data = list(zip(title_movie, year_release, votes_movie, grade_movie, grade_letter_movie, movie_grades))
    df = pd.DataFrame(data, columns=keys)
    # print(df)
    column_names = df.keys()
    values = df.values.tolist()
    return {'column_names': column_names, 'values': values}
    # print(df)
    # print('\n')
    # print(movie_grades)
    # # print(title_movie)

    # print(keys)
    # movie_ids = list(new_dict.keys())
    # movie_grades = list(new_dict.values())
    # return {'column_names': movie_ids, 'values': movie_grades}
    # return df







# # Select all graded movies from a user and rank them by grade
# def view_my_movies(email: str, password: str):
#     c = client()
#     QUERY = f"""SELECT graded_movies FROM {USER_TABLE_NAME} WHERE email = '{email}' and password = '{password}' """
#     result = c.query(QUERY)
#     new_grade = {'1729da40-ab67-4149-836c-6519e99d0849': 'good'}
#     graded_movies_dict = {}
#     for row in result:
#         graded_movies_json = row['graded_movies']
#         graded_movies_dict = json.loads(graded_movies_json)
#     new_dict = {**graded_movies_dict, **new_grade}
#     movie_ids = list(new_dict.keys())
#     movie_grades = list(new_dict.values())
#     return {'column_names': movie_ids, 'values': movie_grades}




def client():
    return bigquery.Client()

def basic_query_job(client):

    QUERY = (
        'SELECT * from {TABLE_NAME}'
    )
    job = client.query(QUERY)
    final_job = job.result().to_dataframe()
    return final_job


def user_login(client, email: str, password: str)->int:
    QUERY = (
        f"""SELECT email, password FROM {TABLE_NAME} WHERE email = '{email}' and password = '{password}'"""
    )
    job = client.query(QUERY)
    login_job = job.result().to_dataframe()
    user_in_database =  len(login_job)

    return user_in_database


# User Signup should also include a function to make sure there are no matching accounts
def user_signup(client, first_name: str, last_name: str, handle: str, email: str, dob: str, phone_prefix: str, phone_number: str, ethnicity: str, race: str, gender: str, gender_identity: str, sexual_orientation: str, political_party: str, password: str):
    existing_user = user_exists(client, email)
    if not existing_user:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            QUERY = f"""
            INSERT INTO {TABLE_NAME} VALUES (GENERATE_UUID(), '{first_name}', '{last_name}',
            '{handle}', '{email}', '{password}', '{ethnicity}', '{race}', '{gender}', '{gender_identity}', '{sexual_orientation}', '{dob}', 
            '{phone_prefix}', '{phone_number}', '{political_party}', JSON_OBJECT() )
            """
            # JSON_OBJECT('dummy_key', NULL)
            job = client.query(QUERY)
            result = job.result()
            # return result
            return 'Signup Successful!'
    else:
        return 'User Already Exists'

def user_exists(client, email):
    QUERY = f"""SELECT * FROM {TABLE_NAME} WHERE email = '{email}'"""
    job = client.query(QUERY)
    result_len = len(job.result().to_dataframe())
    return True if result_len > 0 else False


# def user_logout(client, email: str, password: str)->bool:
#     QUERY = f"""UPDATE {USER_TABLE_NAME} SET logged_in = false WHERE email = {email} and password = {password}"""
#     job = client.query(QUERY)
#     job.result()
#     return True


def user_grade_movie(client, email: str, password: str, user_grade):
    QUERY = f"""UPDATE {USER_TABLE_NAME}"""
    '''
    graded_movies['The Kid'] = user_grade
    '''

def update_movie_table():
    QUERY = f"""UPDATE {MOVIE_TABLE_NAME}"""



# if __name__ == "__main__":
#     # print(search_all_movies("The K"))

#     # ---------------------------

#     c = client()    
#     # print(query_job(c))
#     # print(user_login(c, 'drue@email.com', 'drue_pass123v'))
#     # print(user_signup(c, 'Albus', 'Dumbledore', 'elderWand', 'dd@email.com', '10-4-1213', '1', '892-343-4233', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'dd_pass123'))  
#     # # print(user_exists(c, 'drue@email.com'))
#     # print('Done')


#     vmm = view_my_movies('drue@email.com', 'drue_pass123')
#     vmmt = view_my_movies_two(vmm)
#     print(vmmt)

