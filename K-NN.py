import mysql.connector
import requests
import json
import math
import random
# Could do a dictionary that holds a list as the value


def getUserMovie():
    user = input("Enter a movie: ")
    if len(user) >= 1 and not user.isspace():
        return user
        

def normalizeData(dictionary):
    normalizedDict = {}
    valueList = dictionary.values()
    keyList = list(dictionary.keys())
    max_ = max(valueList) # (C6-MIN(C$2:C$14))/(MAX(C$2:C$14)-MIN(C$2:C$14))
    min_ = min(valueList)
    cnt = 0
    for data in valueList:
        normalized = (data-min_)/(max_-min_)
        #print(f"{keyList[cnt]}: {normalized}")
        normalizedDict.update({keyList[cnt]:normalized})
        cnt += 1
    return normalizedDict

def normalizeRating(dictionary):
    normalizeDict = {}
    valueList = list(dictionary.values())
    keyList = list(dictionary.keys())
    cnt = 0
    for rating in valueList:
        if rating == 'G':
            normalizeDict.update({keyList[cnt]:1})
        elif rating == 'PG':
            normalizeDict.update({keyList[cnt]:2})
        elif rating == 'PG-13':
            normalizeDict.update({keyList[cnt]:3})
        elif rating == 'R':
            normalizeDict.update({keyList[cnt]:4})
        elif rating == 'NC-17':
            normalizeDict.update({keyList[cnt]:5})
        cnt += 1
    return normalizeDict

'''
One-hot encoding for genres
'''        

    
    
def K_NearestNeighbor(k, neighbors):
    kNeighbors = []
    neighbors = dict(sorted(neighbors.items(), key=lambda item: item[1])) # Sort based on distance in ascending order
    cnt = 0
    for title, distance in neighbors.items():
        if cnt == k:
            break
        kNeighbors.append(title)
        cnt+=1
    return kNeighbors

def createSimilarityMatrix():
    genre_similarity_matrix =  [
     [1, 0.6, 0.6, 0.5, 0.2, 0.6, 0.6, 0.3, 0.7, 0.3, 0.2, 0.6, 0.3, 0.2, 0.6, 0.1, 0.2, 0.5, 0.5, 0.3, 0.5, 0.3],
    [0.6, 1, 0.5, 0.5, 0.3, 0.6, 0.3, 0.6, 0.5, 0.2, 0.2, 0.7, 0.4, 0.2, 0.7, 0.1, 0.2, 0.6, 0.5, 0.2, 0.6, 0.2],
    [0.6, 0.5, 1, 0.5, 0.3, 0.2, 0.5, 0.3, 0.6, 0.3, 0.2, 0.6, 0.2, 0.2, 0.2, 0.1, 0.1, 0.5, 0.3, 0.5, 0.5, 0.2],
    [0.5, 0.5, 0.5, 1, 0.6, 0.4, 0.3, 0.5, 0.6, 0.4, 0.3, 0.4, 0.4, 0.4, 0.5, 0.4, 0.3, 0.3, 0.5, 0.3, 0.5, 0.2],
    [0.2, 0.3, 0.3, 0.6, 1, 0.3, 0.2, 0.5, 0.4, 0.3, 0.3, 0.5, 0.4, 0.3, 0.3, 0.2, 0.4, 0.3, 0.4, 0.2, 0.4, 0.2],
    [0.6, 0.6, 0.2, 0.4, 0.3, 1, 0.3, 0.5, 0.5, 0.2, 0.2, 0.6, 0.5, 0.4, 0.3, 0.2, 0.3, 0.5, 0.2, 0.2, 0.2, 0.4],
    [0.6, 0.3, 0.5, 0.3, 0.2, 0.3, 1, 0.3, 0.4, 0.2, 0.2, 0.5, 0.2, 0.2, 0.2, 0.1, 0.1, 0.4, 0.3, 0.2, 0.3, 0.2],
    [0.3, 0.6, 0.3, 0.5, 0.5, 0.5, 0.3, 1, 0.4, 0.2, 0.3, 0.5, 0.6, 0.6, 0.6, 0.3, 0.5, 0.3, 0.4, 0.2, 0.5, 0.4],
    [0.7, 0.5, 0.6, 0.6, 0.4, 0.5, 0.4, 0.4, 1, 0.4, 0.2, 0.4, 0.4, 0.3, 0.6, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.4],
    [0.3, 0.2, 0.3, 0.4, 0.3, 0.2, 0.2, 0.2, 0.4, 1, 0.4, 0.3, 0.2, 0.3, 0.2, 0.4, 0.4, 0.3, 0.5, 0.6, 0.5, 0.4],
    [0.2, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.3, 0.2, 0.4, 1, 0.5, 0.4, 0.6, 0.2, 0.1, 0.9, 0.1, 0.4, 0.4, 0.3, 0.3],
    [0.6, 0.7, 0.6, 0.4, 0.5, 0.6, 0.5, 0.5, 0.4, 0.3, 0.5, 1, 0.6, 0.5, 0.7, 0.3, 0.5, 0.6, 0.6, 0.3, 0.6, 0.6],
    [0.3, 0.4, 0.2, 0.4, 0.4, 0.5, 0.2, 0.6, 0.4, 0.2, 0.4, 0.6, 1, 0.7, 0.7, 0.1, 0.2, 0.1, 0.3, 0.2, 0.3, 0.5],
    [0.2, 0.2, 0.2, 0.4, 0.3, 0.4, 0.2, 0.6, 0.3, 0.3, 0.6, 0.5, 0.7, 1, 0.6, 0.2, 0.6, 0.1, 0.4, 0.3, 0.3, 0.4],
    [0.6, 0.7, 0.2, 0.5, 0.3, 0.3, 0.2, 0.6, 0.6, 0.2, 0.2, 0.7, 0.7, 0.6, 1, 0.2, 0.4, 0.4, 0.1, 0.2, 0.2, 0.4],
    [0.1, 0.1, 0.1, 0.4, 0.2, 0.2, 0.1, 0.3, 0.2, 0.4, 0.1, 0.3, 0.1, 0.2, 0.2, 1, 0.3, 0.2, 0.3, 0.6, 0.2, 0.2],
    [0.2, 0.2, 0.1, 0.3, 0.4, 0.3, 0.1, 0.5, 0.2, 0.4, 0.9, 0.5, 0.2, 0.6, 0.4, 0.3, 1, 0.1, 0.4, 0.3, 0.5, 0.4],
    [0.5, 0.6, 0.5, 0.3, 0.3, 0.5, 0.4, 0.3, 0.3, 0.3, 0.1, 0.6, 0.1, 0.1, 0.4, 0.2, 0.1, 1, 0.5, 0.3, 0.4, 0.1],
    [0.5, 0.5, 0.3, 0.5, 0.4, 0.2, 0.3, 0.4, 0.4, 0.5, 0.4, 0.6, 0.3, 0.4, 0.1, 0.3, 0.4, 0.5, 1, 0.6, 0.5, 0.3],
    [0.3, 0.2, 0.5, 0.3, 0.2, 0.2, 0.2, 0.2, 0.5, 0.6, 0.4, 0.3, 0.2, 0.3, 0.2, 0.6, 0.3, 0.3, 0.6, 1, 0.5, 0.3],
    [0.5, 0.6, 0.5, 0.5, 0.4, 0.2, 0.3, 0.5, 0.5, 0.5, 0.3, 0.6, 0.3, 0.3, 0.2, 0.2, 0.5, 0.4, 0.5, 0.5, 1, 0.2],
    [0.3, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.4, 0.4, 0.4, 0.3, 0.6, 0.5, 0.4, 0.4, 0.2, 0.4, 0.2, 0.3, 0.3, 0.2, 1]
]
    return genre_similarity_matrix
    #uniqueGenres = list(uniqueGenres)
    
            
def mySQL():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="Summer2025_!",
    database="movie_recommendation",
)

        
connection = mySQL()
cursor = connection.cursor()
cursor.execute("SELECT * FROM movies")
movies = cursor.fetchall()
yearDict = {}
runtimeDict = {}
ratingDict = {}
scoreDict = {}
genreDict = {}
languageDict = {}
nearNeighbors = {}

IMDbID = 22022452 #random.randint(4000000, 22022452)
yourkey = "8c7046f1"
result = False
userMovie = ""
while not result:
    userMovie = getUserMovie()
    # Can add the userMovie to database.
    if userMovie is not None:
        try:
            URL = f"http://www.omdbapi.com/?t={userMovie}&apikey={yourkey}&type=movie"

            # print(f"This ID Number: ({IMDbID}). Gave us this URL: {URL}")
            response = requests.get(URL)
            data = json.loads(response.text)
        

            Title = data["Title"] # Movies table 
            Year = int(data["Year"]) # Movies table 
            Rating = data["Rated"] # Movies table
            Release_Date = data["Released"] # Movies table
            Runtime = int(data["Runtime"][:-4]) # Movies table
            Genres = data["Genre"] # Genre Table
            Directors = data["Director"] # Directors Table
            Writers = data["Writer"] # Writers Table
            Actors = data["Actors"] # Actors Table We could use Jaccard Similarity - |(A^B)/(AUB)|
            Languages = data["Language"] # Languages Table 
            Country = data["Country"]
            Score = float(data["Ratings"][1]["Value"][:-1])
            Genres = Genres.split(", ")
            Languages = Languages.split(", ")
            genre = "".join(Genres[:1])
            language = "".join(Languages[:1])
            result = True
            if Rating == "N/A" or Genres == "N/A" or Directors == "N/A" or Writers == "N/A" or Actors == "N/A":
                result = False
                raise ValueError()
        except ValueError:
            print("\n\t\tNo Movie Found")
            continue
        except IndexError:
            print("\n\t\tNo Movie Found")
            continue
target_movie = (1, Title, Year, Runtime, Rating, (Score/100), Genres, language) #(1, 'The Shawshank Redemption', 1994, 142, 'R', 89.00, 'Drama', 'English')
#print(target_movie)
movies.append(target_movie)

'''Retrieve the Genres and create a Hot-Key Vector'''
cursor.execute('''SELECT m.title AS movie_title,
GROUP_CONCAT(g.genre_name SEPARATOR ', ') AS genres
FROM movies m 
JOIN movie_genre mg ON m.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
GROUP BY m.title;''')
movie_Genres = cursor.fetchall()
movie_Genres.append((Title, ", ".join(Genres)))
uniqueGenres = {} #set()
for title, genres in movie_Genres:
    for genre in genres.split(", "):
        uniqueGenres[genre] = None
genres = list(uniqueGenres.keys())
genre_similarity_matrix = createSimilarityMatrix()
'''
for i in range(len(genres)):
    for j in range(len(genres)):
        if genre_similarity_matrix[i][j] == 1:
            print(f"Genres {genres[i]} and {genres[j]} are the same")
        elif genre_similarity_matrix[i][j] > 0.5:
            print(f"Genres {genres[i]} and {genres[j]} are quite similar with a score of {genre_similarity_matrix[i][j]}")
        elif genre_similarity_matrix[i][j] > 0.3:
            print(f"Genres {genres[i]} and {genres[j]} have moderate similarity with a score of {genre_similarity_matrix[i][j]}")
        else:
            print(f"Genres {genres[i]} and {genres[j]} have low similarity with a score of {genre_similarity_matrix[i][j]}")

genre_vector = [0]
'''
'''Retrieve all the languages and create a language vector'''
cursor.execute('''SELECT m.title AS title, 
GROUP_CONCAT(l.movie_language SEPARATOR ', ') AS languages
FROM movies m
JOIN movie_language ml ON m.movie_id = ml.movie_id
JOIN languages l ON ml.language_id = l.language_id
GROUP BY m.title;''')
movie_Languages = cursor.fetchall()
movie_Languages.append((Title, ", ".join(Languages)))
uniqueLanguages = set()
for title, languages in movie_Languages:
    for language in languages.split(", "):
        uniqueLanguages.add(language)
uniqueLanguages = list(uniqueLanguages)
language_vector = [0]

for movie in movies:
    movie_name = movie[1]
    year = movie[2]
    runtime = movie[3]
    rating = movie[4]
    score = float(movie[5])
    #genre = movie[6]
    language = movie[7]

    yearDict.update({movie_name:year})
    runtimeDict.update({movie_name:runtime})
    ratingDict.update({movie_name:rating})
    scoreDict.update({movie_name:score})
    '''
    for title, genres in movie_Genres:
        if movie_name == title:
            movie_Genres = [movie for movie in movie_Genres if movie[0] is not title] # Shrink the movie_Genres list
            genre_vector = [0] * len(genres.split(", "))
            for genre in genres.split(", "):
                genre_vector[idx] = 1
            genreDict[movie_name] = genre_vector #simlar to update
            break
    
        
    for title, languages in movie_Languages[::-1]:
        if movie_name == title:
            movie_Languages = [movie for movie in movie_Languages[::-1] if movie[0] is not title]
            language_vector = [0] * len(uniqueLanguages)
            for language in languages.split(", "):
                idx = uniqueLanguages.index(language)
                language_vector[idx] = 1
            languageDict[movie_name] = language_vector #simlar to update
            break
    '''
    
    
    

    
#for title, genre_vector in genreDict.items():
#    print(f"Title: {title}, One-Hot Encoded Genre: {genre_vector}")


#Normalization
normalizedYearDict = normalizeData(yearDict)
normalizedRunTimeDict = normalizeData(runtimeDict)
normalizedRatingDict = normalizeRating(ratingDict)
movieDict = {}
featureList = []

for movie in movies:
    title = movie[1]
    movieGenres = movie[6] # list of genres
    for film_title, film_genre in movie_Genres:
        if title in normalizedYearDict and title in normalizedRunTimeDict and title in normalizedRatingDict and title == film_title: # Hell slow
            featureList = [
                normalizedYearDict[title],
                normalizedRunTimeDict[title],
                float(movie[5]),  # score
                normalizedRatingDict[title],
                film_genre,
                    
                #genres = movie[6]
                #for genre in genres if genre in 
                #genreDict[title]
            ]
            movieDict[title] = featureList

                        
                    

                    

#Euclidean Distance
#print(movieDict)
target_movie = movieDict.popitem() # get user entered target movie

target_title, target_features = target_movie
bitSum = 0
featureSum = 0
recommendedDict = {}
quit_loop = False
'''Calculate Euclidean  Distance'''
for title, normalizedFeatures in movieDict.items():
    featureSum = 0
    genreList = []
    for i in range(len(normalizedFeatures)): # Year, Runtime, Score, Rating, Genre, Languages 
        if i == 4: # genre
            target_genres = target_features[i].split(", ")
            normalized_genres = normalizedFeatures[i].split(", ")
            for target_genre in target_genres: 
                for genre in normalized_genres:
                    if quit_loop:
                        quit_loop = False
                    for step in range(len(genres)):
                        if quit_loop:
                            break
                        if target_genre == genres[step]:
                            for second_step in range(len(genres)):
                                if genre == genres[second_step]:
                                    #print(f"{target_genre} and {genre}: ", genre_similarity_matrix[step][second_step])
                                    genreList.append(genre_similarity_matrix[step][second_step])
                                    quit_loop = True
                                    break
                        if  genre == genres[step]:
                            for second_step in range(len(genres)): # can do a set() and return value
                                if target_genre == genres[second_step]:
                                    #print(f"{genre} and {target_genre}: ", genre_similarity_matrix[step][second_step])
                                    genreList.append(genre_similarity_matrix[step][second_step])
                                    quit_loop = True
                                    break
            featureSum += min(genreList)**2
            
            #print(f"{normalizedFeatures[i]} - {target_features[i]}")
            #for bit in range(len(normalizedFeatures[i])):
                #featureSum += (target_features[i][bit]-normalizedFeatures[i][bit])**2
                #print(f"({normalizedFeatures[i][bit]}-{target_features[i][bit]})^2 = {(normalizedFeatures[i][bit]-target_features[i][bit])**2}")
                #featureSum += bitSum
        else:  
            #print(f"{target_title}: {target_features[i]}\n{title}: {normalizedFeatures[i]}")
            #print(f"({target_features[i]}-{normalizedFeatures[i]})^2={(target_features[i]-normalizedFeatures[i])**2}")
            featureSum += (target_features[i]-normalizedFeatures[i])**2
    #print(f"{title}: {math.sqrt(featureSum)}")
    recommendedDict[title] = math.sqrt(featureSum)

print()    
print(K_NearestNeighbor(5, recommendedDict))
exit()


