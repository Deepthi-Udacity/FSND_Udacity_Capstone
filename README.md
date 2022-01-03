# Casting Agency

## Capstone Project for Udacity's Full Stack Developer Nanodegree

Heroku Link: https://fsndudacityfinalproject.herokuapp.com/

While running locally: http://localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   - `delete:movies`
6. Create new roles for:
   - Casting Assistant
     - can `get:actors`
     - can `get:movies`
   - Casting Director
     - can `get:actors`
     - can `get:movies`
     - can `post:actors`
     - can `delete:actors`
     - can `patch:actors`
     - can `patch:movies`
   - Executive Producer
     - can `get:actors`
     - can `get:movies`
     - can `post:actors`
     - can `post:movies`
     - can `delete:actors`
     - can `delete:movies`
     - can `patch:actors`
     - can `patch:movies`
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the Casting Assistant role to one and Casting Director role to the other and Executive Producer to the remaining.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter/Casting Agency.postman_collection.json`
   - Right-clicking the each collection folder, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## Setup Database

 Run the commands below from the same directory.

```
dropdb castingagency
createdb castingagency
psql castingagency < casting.psql

```
## API Reference

### Getting Started
- Base URL: At present this app is hosted in Heroku - https://fsndudacityfinalproject.herokuapp.com/ 
- When running locally, the app can be accessed by `http://127.0.0.1:5000/`
- Authentication: is managed by Auth0

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
```
The API will return below error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not Allowed
- 500: Internal Server Error

### Endpoints 

#### GET /movies
- General:
    - Returns a list of movies
    - requires get:movies permission
``` 
 https://fsndudacityfinalproject.herokuapp.com/movies
```
Response:
``` {
    "movies": [
        {
            "id": 1,
            "releaseDate": "2012-12-17",
            "title": "Movie1"
        },
        {
            "id": 2,
            "releaseDate": "2022-12-17",
            "title": "Movie2"
        }
    ],
    "success": true
}
```
#### GET /actors
- General:
    - Returns a list of actors
    - requires get:actors permission
``` 
https://fsndudacityfinalproject.herokuapp.com/actors
```
Response:
``` {
    "actors": [
        {
            "age": 30,
            "gender": "Male",
            "id": 1,
            "name": "Actor1"
        },
        {
            "age": 60,
            "gender": "Female",
            "id": 3,
            "name": "Actor3"
        }
    ],
    "success": true
}
```

#### POST /movies
- General:
    - Creates a new movie
    - Returns the id of the created movie, success value
    - requires post:movies permission

Request:
```
https://fsndudacityfinalproject.herokuapp.com/movies

```
Request Body:
```
{
    "title" : "Movie1",
    "releaseDate" : "2021-11-16"
}
```
Response:
```
{
    "created": 1,
    "success": true
}
```

#### POST /actors
- General:
    - Creates a new actor
    - Returns the id of the created actor, success value
    - requires post:actors permission

Request:
```
https://fsndudacityfinalproject.herokuapp.com/actors

```
Request Body:
```
{
    "name" : "Actor1",
    "age" : 80,
    "gender" : "Male"
}
```
Response:
```
{
    "created": 1,
    "success": true
}
```

#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. 
    - Returns the id of the deleted movie, success value. 
    - requires delete:movies permission

Request:
```
https://fsndudacityfinalproject.herokuapp.com/movies/1
```
Response:
```
{
    "deleted": 1,
    "success": true
}

```
#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor of the given ID if it exists. 
    - Returns the id of the deleted actor, success value. 
    - requires delete:actors permission

Request:
```
https://fsndudacityfinalproject.herokuapp.com/actors/1
```
Response:
```
{
    "deleted": 1,
    "success": true
}

```

#### PATCH /movies/movie_id
- General:
    - Updates the movie for given ID
    - Returns the full details of the updated movie, success value
    - requires patch:movies permission

Request:
```
https://fsndudacityfinalproject.herokuapp.com/movies/1

```
Request Body:
```
{
    "releaseDate" : "2022-11-18"
}
```
Response:
```
{
    "success": true,
    "updated_movie": {
        "id": 1,
        "releaseDate": "2022-11-18",
        "title": "Movie1"
    }
}
```

#### PATCH /actors/actor_id
- General:
    - Updates the actor for given ID
    - Returns the full details of the updated actor, success value
    - requires patch:actors permission

Request:
```
https://fsndudacityfinalproject.herokuapp.com/actors/1

```
Request Body:
```
{
    "age" : 40
}
```
Response:
```
{
    "success": true,
    "updated_actor": {
        "age": 40,
        "gender": "Male",
        "id": 1,
        "name": "Actor1"
    }
}
```
## Testing
To run the tests,

 Run the commands below from the same directory.

```
dropdb castingagencytest
createdb castingagencytest
psql castingagencytest < casting.psql
python test_app.py
```

## Postman Collection
You can also test the application using Postman collection in \Casting Agency.postman_collection.json

