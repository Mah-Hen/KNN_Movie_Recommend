CREATE DATABASE movie_recommendation;
USE movie_recommendation;

CREATE TABLE movies(
movie_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
title VARCHAR(100), 
year INT, 
runtime INT,
rating VARCHAR(10),  
imdb_score NUMERIC(5, 2), 
genre VARCHAR (15),
language VARCHAR(20)
);

CREATE TABLE users(
user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
user_name VARCHAR(50),
user_password VARCHAR(50)
);

CREATE TABLE actors(
actor_id INTEGER PRIMARY KEY AUTO_INCREMENT,
actorFirst_name VARCHAR(100),
actorLast_name VARCHAR(100)
);

CREATE TABLE writers(
writer_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
writerFirst_name VARCHAR(100),
writerLast_name VARCHAR(100)
);

CREATE TABLE directors(
director_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
directorFirst_name VARCHAR(100), 
directorLast_name VARCHAR(100)
);

CREATE TABLE genres(
genre_id INTEGER PRIMARY KEY AUTO_INCREMENT,
genre_name VARCHAR(50)
);

CREATE TABLE languages(
language_id INTEGER PRIMARY KEY AUTO_INCREMENT,
movie_language VARCHAR(50)
);

# Intersection table
CREATE TABLE movie_user(
movie_id INTEGER, 
user_id INTEGER, 
liked BOOLEAN, 
rating INTEGER CHECK (rating >= 1 AND rating <= 5),
PRIMARY KEY (movie_id, user_id),
FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE movie_actor(
movie_id INTEGER, 
actor_id INTEGER,
PRIMARY KEY (movie_id, actor_id),
FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);

CREATE TABLE movie_director(
movie_id INTEGER, 
director_id INTEGER, 
PRIMARY KEY (movie_id, director_id),
FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
FOREIGN KEY (director_id) REFERENCES directors(director_id)
);

CREATE TABLE movie_writer(
movie_id INTEGER, 
writer_id INTEGER, 
PRIMARY KEY (movie_id, writer_id),
FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
FOREIGN KEY (writer_id) REFERENCES writers(writer_id)
);

CREATE TABLE movie_genre(
movie_id INTEGER,
genre_id INTEGER, 
PRIMARY KEY (movie_id, genre_id), 
FOREIGN KEY (movie_id) REFERENCES movies(movie_id), 
FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE movie_language(
movie_id INTEGER,
language_id INTEGER, 
PRIMARY KEY (movie_id, language_id),
FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
FOREIGN KEY (language_id) REFERENCES languages(language_id)
);

#DROP TABLE movie_director;
DROP DATABASE movie_recommendation;
SELECT movie_id, title FROM movies; 

SELECT g.genre_name AND m.title
FROM genres g AND movies m
JOIN movie_genre mg ON g.genre_id = mg.genre_id 
WHERE mg.movie_id = 2;

