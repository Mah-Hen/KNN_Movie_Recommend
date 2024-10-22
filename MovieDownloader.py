import requests
import random
import json
import mysql.connector
import re
import os

def createProfile():
    user = ""
    password = ""
    user = input("Enter Username: ")
    if user.isalpha():
        password = input("Enter Password: ")
        cursor.execute(
            "INSERT INTO users (user_name, user_password) VALUES (%s, %s)", (user, password)
        )

def verifyProfile():
    currUser = ""
    userPassword = ""
    correct_user = True
    correct_pass = False
    
    while(correct_user):
        currUser = input("Enter Username: ")
        if currUser.isalnum():
            cursor.execute(
                "SELECT user_name FROM users WHERE user_name = %s", (currUser, )
            )
            validUserName = cursor.fetchone()
            if validUserName is None:
                print("\n\tThere's no evidence of that user existing.")
                createProfile = input("Would you like to create a new profile? (Yes/No) ")
                if createProfile.isalpha():
                    if createProfile.lower() == "yes" or createProfile.lower() == "y":
                        clear()
                        createProfile()
                    elif createProfile.lower() == "no" or createProfile.lower() == "n":
                        clear()
                        createProfile()
                else:
                    continue
            else:
                while(correct_pass):
                    validUserName = validUserName[0]
                    clear()
                    userPassword = input("Enter Password: ")
                    if userPassword.isalnum():
                        print("\nValidating....")
                        cursor.execute("SELECT user_password FROM users WHERE user_password = %s", (userPassword, ))
                        validUserPassword = cursor.fetchone()
                        if validUserPassword is None:
                            print("\n\tIncorrect Password. Try again.")
                        else:
                            print("*Click*")
        
def insertMovie(cursor, Title, Year, Runtime, Rating, Score, Genres, Languages):
    print(f"Inserting movie: {Title}, {Year}, {Runtime}, {Rating}, {Score}, {Genres}, {Languages}\n")
    Genres = [genre for genre in Genres.split(", ")]
    Languages = [language for language in Languages.split(", ")]
    cursor.execute(
        "INSERT INTO movies (title, year, runtime, rating, imdb_score, genre, language) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (Title, Year, Runtime, Rating, Score, Genres[0], Languages[0]),
    )
    #connection.commit()
    return cursor.lastrowid # retrieve the movie ID


def insertActor(cursor, Actors, movieID):
    actors = [actor for actor in Actors.split(", ")]
    for actor in actors:
        if len(actor.strip().split(" ")) > 2: # Get rid of middle name/ extra names
            actor = actor.strip().split(" ")[0] + " " + actor.strip().split(" ")[-1]
        try:    
            first_name, last_name = actor.strip().split()
        except ValueError:
            first_name = actor
            last_name = "N/A"
        print(f"Inserting actor: {first_name} {last_name}")
        
        cursor.execute( # Checking to see if the actor already exist
        "SELECT actor_id FROM actors WHERE actorFirst_name = %s AND actorLast_name = %s",
        (first_name, last_name),
        )
        actorRow = cursor.fetchone()
        if actorRow is not None:
            actorID = actorRow[0]  # Retrieve the ID number in the Actor entry
        else:
            cursor.execute(
                "INSERT INTO actors (actorFirst_name, actorLast_name) VALUES (%s, %s)",
                (first_name, last_name),
            )
            actorID = cursor.lastrowid
        
        insertMovie_Actor(movieID, actorID)
        #connection.commit()
        

def insertGenre(movieID, Genres):
    print(f"From {Title}, inserting genres: {Genres} ")
    Genres = [genre for genre in Genres.split(", ")]
    for genre in Genres:
        cursor.execute( # Checking to see if the actor already exist
        "SELECT genre_id FROM genres WHERE genre_name = %s",
        (genre,),
        )
        genreRow = cursor.fetchone()
        if genreRow is not None:
            genreID = genreRow[0]  # Retrieve the ID number in the Actor entry
        else:
            cursor.execute("INSERT INTO genres (genre_name) VALUES (%s)", (genre,),)
            genreID = cursor.lastrowid
        insertMovie_Genre(movieID, genreID)
        #connection.commit()

def insertDirector(MovieID, Directors):
    print(f"Inserting {Directors}")
    Directors = [director for director in Directors.split(", ")]
    for director in Directors:
        if len(director.strip().split(" ")) > 2: # Get rid of middle name/ extra names
            director = director.strip().split(" ")[0] + " " + director.strip().split(" ")[-1]
        try:    
            first_name, last_name = director.strip().split()
        except ValueError:
            first_name = director
            last_name = "N/A"
        cursor.execute("SELECT director_id FROM directors WHERE directorFirst_name = %s AND directorLast_name = %s", (first_name, last_name))
        directorRow = cursor.fetchone()
        if directorRow is not None:
            directorID = directorRow[0]
        else:
            cursor.execute("INSERT INTO directors (directorFirst_Name, directorLast_name) VALUES (%s, %s)", (first_name, last_name))
            directorID = cursor.lastrowid
        insertMovie_Director(movieID, directorID)
        #connection.commit()



def insertWriter(MovieID, Writers):
    print(f"Inserting {Writers}")
    Writers = [writer for writer in Writers.split(", ")]
    for writer in Writers:
        if len(writer.strip().split(" ")) > 2: # Get rid of middle name/ extra names
            writer = writer.strip().split(" ")[0] + " " + writer.strip().split(" ")[-1]
        first_name, last_name = writer.strip().split(" ")
        cursor.execute("SELECT writer_id FROM writers WHERE writerFirst_name = %s AND writerLast_name = %s", (first_name, last_name))
        writerRow = cursor.fetchone()
        if writerRow is not None:  
            writerID = writerRow[0]  
        else:
            cursor.execute("INSERT INTO writers (writerFirst_Name, writerLast_name) VALUES (%s, %s)", (first_name, last_name))
            writerID = cursor.lastrowid
        insertMovie_Writer(movieID, writerID)
        #connection.commit()

def insertLanguage(MovieID, Languages):
    print(f"Inserting {Languages}")
    Languages = [language for language in Languages.split(", ")]
    for language in Languages:
        cursor.execute("SELECT language_id FROM languages WHERE movie_language = %s", (language,))
        languageRow = cursor.fetchone()
        if languageRow is not None:
            languageID = languageRow[0] 
        else:
            cursor.execute("INSERT INTO languages (movie_language) VALUES (%s)", (language,))
            languageID = cursor.lastrowid
        insertMovie_Language(movieID, languageID)
        #connection.commit()


def insertMovie_Actor(movieID, actorID):
    cursor.execute(
        "INSERT INTO movie_actor (movie_id, actor_id) VALUES (%s, %s)",
        (movieID, actorID),
    )   
    cursor.fetchall()  # Fetch all remaining results to clear the cursor  
    
def insertMovie_Genre(movieID, genreID):
     cursor.execute(
        "INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)",
        (movieID, genreID),
    ) 
     cursor.fetchall()  # Fetch all remaining results to clear the cursor

def insertMovie_Director(movieID, directorID):
    cursor.execute(
        "INSERT INTO movie_director (movie_id, director_id) VALUES (%s, %s)", (movieID, directorID)
    ) 
    cursor.fetchall()  # Fetch all remaining results to clear the cursor 

def insertMovie_Writer(movieID, writerID):
    cursor.execute(
        "INSERT INTO movie_writer (movie_id, writer_id) VALUES (%s, %s)", (movieID, writerID)
    ) 
    cursor.fetchall()  # Fetch all remaining results to clear the cursor

def insertMovie_Language(movieID, languageID):
    cursor.execute(
        "INSERT INTO movie_language (movie_id, language_id) VALUES (%s, %s)",
        (movieID, languageID),
    )
    cursor.fetchall()  # Fetch all remaining results to clear the cursor


def clear():
     print(flush=True)

def searchMovie(title, yourkey):
    URL = f"http://www.omdbapi.com/?t={title}&apikey={yourkey}"
    response = requests.get(URL) 
    data = json.loads(response.text)  
    if len(data) == 2: # No data found
        return
    Title = data["Title"] # Movies table 
    Year = int(data["Year"]) # Movies table 
    Rating = data["Rated"] # Movies table
    if Rating == "N/A":
        return
    Release_Date = data["Released"] # Movies table
    Runtime = int(data["Runtime"][:-4]) # Movies table
    Genres = data["Genre"] # Genre Table
    Directors = data["Director"] # Directors Table
    Writers = data["Writer"] # Writers Table
    Actors = data["Actors"] # Actors Table
    Languages = data["Language"] # Languages Table 
    Country = data["Country"]
    #boxOffice = data["boxOffice"]
    scores = 0
    for i in range(len(data["Ratings"])):
        rating = data["Ratings"][i]["Value"]
        if "/" in rating:
            split_rating = rating.split("/")
            scores += float(split_rating[0])/float(split_rating[-1])
            
        else:
            rating = rating[:-1]
            scores += float(rating)/100
    Score = scores/len(data["Ratings"])
    cursor.execute("SELECT title FROM movies WHERE title = %s", (Title,))
    movie = cursor.fetchone()
    '''
    if movie is None:
        exit()
        # print(f"{Title}, Actors: {Actors}")
        movieID = insertMovie(cursor, Title, Year, Runtime, Rating, Score, Genres, Languages)  # Insert the movie and retrieve the movie ID
        insertActor(cursor, Actors, movieID) # Insert Actors into SQL database via Query 
        insertGenre(movieID, Genres) # Insert Genre into SQL database via Query
        insertDirector(movieID, Directors) # Insert Director into SQL database via Query
        insertWriter(movieID, Writers) # Insert Writer into SQL database via Query
        insertLanguage(movieID, Languages) # Insert Language into SQL database via Query
    '''

yourkey = "8c7046f1"
movieTitles = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", "Schindler's List", "Pulp Fiction", "The Lord of the Rings: The Return of the King", "Forrest Gump", "Fight Club", "Inception", "The Matrix", "Goodfellas", "Se7en", "Interstellar"]
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Summer2025_!",
    database="movie_recommendation",
)

cursor = connection.cursor()

sqlData = []
done = False
cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
#createProfile()
#connection.commit()
#verifyProfile()

#For testing purposes. Remember to deleter later. 

cursor.execute("ALTER TABLE movies AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE actors AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE genres AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE directors AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE writers AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE languages AUTO_INCREMENT = 1")

with open("/Users/mahla/Downloads/SQL/movies.txt", "r") as f:
    for line in f:
        title = ""
        text = line.split("/")
        text = re.sub('[(..)]', '', text[0])
        title = re.sub('\d', '', text)
        
        #title = ''.join([i for i in title if i.isalpha])
        searchMovie(title, yourkey)

        
       
    

cursor.close()
connection.close()
print("DONE!")   

