﻿# My Django Project
## setup instructions
"clone the repository"
"go to the project directory"
"set up the virtual environment called venv"
"activate the virtual environment"
"install the requirements"

## Project purpose and reflection
This project involves an api that manages reviews for movies stored in the api it has implemented
core functionalities to enhance api user interface requirements. Users can register, have and update their profiles, create reviews, comment on reviews and like reviews. Users can also receive notifications to see who liked their reviews for what movie and the id. It implements a simple url strategy for making reviews and commenting on them. Apart from reviews users also get to fetch info and data about movies implementations like movie description, rating, release date and even cast and crew info.
These is a list of the core api endpoints added
1. api/review/     for creating a review with a rating for a specific movie
2. api/movies/     for getting all movies
3. api/movies/title(e.g Titanic)/   for getting specific movie
4. api/movies/title/reviews/    for getting and creating reviews for a specific movie
5. api/movies/title/reviews/id(a number representing the id of the review)/ for getting a specific review
6. api/movies/title/reviews/id/comment/ for commenting and getting comments for reviews
7. api/movies/title/reviews/id/like/  for liking a review
8. api/movies/title/reviews/id/unlike/ for unliking a review
9. api/profile/   shows a user profile
10. api/notifications/   shows the notifications for the user
