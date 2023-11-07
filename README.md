# MovieMage_homescreen
This is the home screen for a movie grading application called MovieMage

### About
1. This will be connected to the login/signup screen

2. Once a user is logged in, they will see this home page
- For now the home page will just display what the app is and what it can be used for, along with a description of the grading system, and a movie manifesto. 

3. Then they will be able to access other API's and backend functionalities including:
- My Movies API (code is in other project): movies that were graded by user ranked by grade then number of votes
<!-- - My Mage API (code is in other project): a user can create lists of movies pertaining to anything they want. (e.g. Vampire movies, Christmas Movies, Marvel Movies, Watch Later, etc.) -->
- Recommendations API (code is in other project): showcases the recommended films based on graded movies by user (THIS DOES NOT TAKE DATA FROM "My Playlist API" as features for the model)
- Search (code is in this project): This allows the user to search for direct matches for the movie they are searching
- Settings (code is in this project): For the beta version this just allows the user to signout. Will add additionally funcitons to it like "About Us", "Contact US", "Notifications", etc.



### Run Flask App
```
FLASK_ENV=development
FLASK_APP=app.py
flask run
```



### Still Left to do
- Containerization
- CI/CD 
- Kubernetes
- Seldon Core vs Vertex AI

### Final Steps
- Ensure everthing is connected properly

### Next Version
- Allow users to grade anyone with a credit
- Alow users to generate their own playlists of movies, like vampires, Christmas, Drew Barrymore
- Create an api that shows the vote count vs grade for films from the last week, last month, last 3 months, last 6 months, all time 
- Display what is trending (vote count vs grade for films from the last 24 hours)
- Add more movies, tv shows, original streaming projects, documentaries, specials, trailers, etc. 
