from google.cloud import bigquery
import os
import json
from dotenv import load_dotenv
import pandas as pd
import warnings
from typing import Optional

load_dotenv()

# GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "movie-grader-394211-4edbebb0a607.json"
TABLE_NAME = os.getenv('TABLE_NAME') 
USER_TABLE_NAME = os.getenv('USER_TABLE_NAME')
MOVIE_TABLE_NAME = os.getenv('MOVIE_TABLE_NAME')




# def movie_update_table(movie_title: str):
#     c = client()
#     QUERY = f"""SELECT movie_title, movie_votes, movie_grade, movie_letter_grade FROM {MOVIE_TABLE_NAME} WHERE movie_title = {movie_title}"""
#     result = c.query(QUERY)
#     x = result.to_dataframe()
#     return x




# When searching a movie, this function allows a user to see what movies they have already graded
# Update the new grade to the dictionary 
# e.g. old_grade = {'1729da40-ab67-4149-836c-6519e99d0849': 'good'} -> new_grade = {'1729da40-ab67-4149-836c-6519e99d0849': 'great'} 
def user_update_grade(search_my_movies_dict: dict, movie_title: str, new_grade: str):
    grade_movie = {}
    movie_info = search_my_movies_dict['values']
    user_movie_titles = [title[0] for title in movie_info]
    if movie_title in user_movie_titles:
        movie_title_index = user_movie_titles.index(movie_title)
        # movie_info[movie_title_index][-2]= new_grade
        movie_info[movie_title_index][-2]= new_grade
    movie_id = search_my_movies_dict['movie_ids'][movie_title_index]
    # print(movie_info, movie_id)
    # return movie_info, movie_id
    grade_movie[movie_id] = new_grade
    print(grade_movie)
    return grade_movie
    #     print(search_my_movies_dict, movie_title, new_grade)

    # return search_my_movies_dict, movie_title, new_grade
    # all_search_movie_titles = search_my_movies_dict['values']
    # if movie_title in all_search_movie_titles:
    #     movie_change_index = search_my_movies_dict['values'].index(movie_title)
    #     search_my_movies_dict['values'][movie_change_index] = new_grade
    # print(search_my_movies_dict)
    # return json.loads(search_my_movies_dict)
    '''
    graded_movies['The Kid'] = user_grade
    '''



# Updates the user table with the new grade
def user_update_grade_json(user_update_grade_dict: dict, email: str, password: str)->dict:
    # print('working')
    # new_user_all_grades_dict = {}
    # print(user_update_grade_dict, 'PPPPPPPPPPPPPPPP')
    c = client()
    QUERY = f"""SELECT graded_movies FROM {USER_TABLE_NAME} WHERE email = '{email}' and password = '{password}' """
    result = c.query(QUERY)
    # print(result.result())
    for row in result:
        movie = json.loads(dict(row.items())['graded_movies'])
        # print('MOVIE **************************',movie)
    new_user_all_grades_dict = {**movie, **user_update_grade_dict} 
    # my_movie_update = movie.popitem()
    # movie_id = my_movie_update[0]
    # movie_grade = my_movie_update[1]
    # user_update_grade_dict[movie_id] = movie_grade
    # # print(new_user_all_grades_dict, new_user_grade_dict, type(movie))
    # print(user_update_grade_dict)
    # return user_update_grade_dict

    # new_user_all_grades_dict[movie_id] = movie_grade
    # print(new_user_all_grades_dict, new_user_grade_dict, type(movie))
    print(new_user_all_grades_dict)
    return new_user_all_grades_dict

def update_user_table_with_new_grade(new_user_all_grades_dict: dict, email: str, password: str):
    c = client()
    # print('Dddddddddddddddddd', new_user_all_grades_dict)
    movie_id_grade = new_user_all_grades_dict.popitem()
    movie_id = movie_id_grade[0]
    movie_grade = movie_id_grade[1]

    # json_grades = json.dumps(new_user_all_grades_dict)
    QUERY = f"""UPDATE {USER_TABLE_NAME} SET graded_movies = JSON_OBJECT('{movie_id}', '{movie_grade}') WHERE email = '{email}' and password = '{password}' """
    result = c.query(QUERY)
    # print(result, email, password)
    return True if result else False


# search_my_movies: User Table
# view_my_movies: Movie Table

# Search for the movie ids that a user has graded, this will update the dictionary with the users grade of that movie while the movies 
# ...the user hasn't graded display as NYG for Not Yet Graded

# Possibly remove
def search_my_movies(search_all_movies_dict: list, email: str, password: str)->dict:
    c = client()
    QUERY = f"""SELECT graded_movies FROM {USER_TABLE_NAME} where email = '{email}' and password = '{password}' """
    result = c.query(QUERY)
    df = result.to_dataframe()
    my_graded_movies = json.loads(df['graded_movies'].values[0])
    my_grade_movies_ids = list(my_graded_movies.keys())
    search_movie_ids = search_all_movies_dict['movie_ids']
    for movie_id in my_grade_movies_ids:
        if movie_id in search_movie_ids:
            my_movie_grade =  my_graded_movies[movie_id]
            search_matching_index = search_all_movies_dict['movie_ids'].index(movie_id)
            search_all_movies_dict['values'][search_matching_index][-2] = my_movie_grade
    return search_all_movies_dict





# Search function: allows users to look up movies by title
def search_all_movies(query):
    c = client()
    # QUERY = f'''SELECT * EXCEPT(movieID) FROM {MOVIE_TABLE_NAME} WHERE LOWER(movie_title) LIKE LOWER('%{query}%') '''
    QUERY = f"""SELECT * FROM {MOVIE_TABLE_NAME} WHERE LOWER(movie_title) LIKE LOWER('%{query}%') """
    result = c.query(QUERY)
    df = result.to_dataframe()
    movie_ids = df['movieId'].values.tolist()
    # df = df.iloc[:, :-1]
    df = df.iloc[:, :-2]
    # df.drop(columns='movieId')
    df['my_movie_grade'] = 'NYG'
    df['change_movie_grade'] = 'NYG'
    column_names = df.keys()
    values = df.values.tolist()
    # print(values)
    return {'column_names': column_names, 'values': values, 'movie_ids': movie_ids}


# My Movies - Select all graded movies from a user 
def extract_user_movie_grades(email: str, password: str):
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

# My Movies - Creates the final dictionary of a user's graded movies to be displayed in front end
def view_my_movies(my_movies_dict: dict)->dict:
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
        QUERY = f"""SELECT * EXCEPT(movieId, sum_user_grades) FROM {MOVIE_TABLE_NAME} WHERE movieId = '{m}' """
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











# Big Query SDK Client
def client():
    return bigquery.Client()

# Remove
def basic_query_job(client):

    QUERY = (
        'SELECT * from {TABLE_NAME}'
    )
    job = client.query(QUERY)
    final_job = job.result().to_dataframe()
    return final_job

# Logs in a user into the home page
def user_login(client, email: str, password: str)->int:
    QUERY = (
        f"""SELECT email, password FROM {TABLE_NAME} WHERE email = '{email}' and password = '{password}'"""
    )
    job = client.query(QUERY)
    login_job = job.result().to_dataframe()
    user_in_database =  len(login_job)

    return user_in_database


# User Signup inserts the new user into the user table
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

# Checks if user is already saved in a database for users trying to signup twice
def user_exists(client, email)->bool:
    QUERY = f"""SELECT * FROM {TABLE_NAME} WHERE email = '{email}'"""
    job = client.query(QUERY)
    result_len = len(job.result().to_dataframe())
    return True if result_len > 0 else False

# Remove
# def user_logout(client, email: str, password: str)->bool:
#     QUERY = f"""UPDATE {USER_TABLE_NAME} SET logged_in = false WHERE email = {email} and password = {password}"""
#     job = client.query(QUERY)
#     job.result()
#     return True



# def user_grade_movie_update_movie_table(new_user_grade_dict: dict, email: str, password: str):
#     QUERY = f"""UPDATE {MOVIE_TABLE_NAME} SET graded_movies = '{new_user_grade_dict}' WHERE movie_title = '{movie_title}' """

# # Select all graded movies from a user and rank them by grade
# def extract_user_movie_grades(email: str, password: str):
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


# if __name__ == "__main__":
#     results_dict = search_all_movies("The K")
#     # my_movies_dict = search_my_movies(results_dict, 'drue@email.com', 'drue_pass123')
#     # new_grade_dict = user_grade_movie_update_user_dict(my_movies_dict, '1156fa88-f38a-4754-8c8a-191df28efd5a', 'great')
#     # print(new_grade_dict)
#     print(results_dict)
    # to change the movie grade i need the movie id and the new grade
# #     # ---------------------------

#     c = client()    
#     # print(query_job(c))
#     # print(user_login(c, 'drue@email.com', 'drue_pass123v'))
#     # print(user_signup(c, 'Albus', 'Dumbledore', 'elderWand', 'dd@email.com', '10-4-1213', '1', '892-343-4233', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'Prefer Not to Disclose', 'dd_pass123'))  
#     # # print(user_exists(c, 'drue@email.com'))
#     # print('Done')


#     vmm = extract_user_movie_grades('drue@email.com', 'drue_pass123')
#     vmmt = view_my_movies(vmm)
#     print(vmmt)

