import requests
import mysql.connector
import os
import json
'''
URL = "https://www.imdb.com/chart/top"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

target_div = soup.body.find('div', id="__next")  # /html/body/div[2]
target_main = target_div.find('main')       # /html/body/div[2]/main
target = target_main.find('div')  # /html/body/div[2]/main/div/div[3]
target_section = target.find_all('div')[1].find("section")
print(target_section)

#/html/body/div[2]/main/div/div[3]/section

'''

URL = "https://github.com/mikeleguedes/json-movie-list.git"
directory = "json-movie-list"

#git.Repo.clone_from(URL, directory)

movies_folder = os.path.join(directory, "movies")

# List files in the folder
for file_name in os.listdir(movies_folder)[:1]:
    movie_folder = os.path.join(movies_folder, file_name)
    for movie_name in os.listdir(movie_folder):
        movie_name = movie_name[:-5].replace("-", " ")
        print(movie_name)
        yourkey = "8c7046f1"
        URL = f"http://www.omdbapi.com/?t={movie_name}&apikey={yourkey}"
        # print(f"This ID Number: ({IMDbID}). Gave us this URL: {URL}")
        response = requests.get(URL)
        data = json.loads(response.text)


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Summer2025_!",
    database="movie_recommendation",
)

cursor = connection.cursor()
directory = "json-movie-list"

#git.Repo.clone_from(URL, directory) # Uncomment this to clone repo to your local machine

movies_folder = os.path.join(directory, "movies")

# List files in the folder

            
        
