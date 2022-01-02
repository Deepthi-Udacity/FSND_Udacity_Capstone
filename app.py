import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from werkzeug.local import release_local

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  ''' 
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
      )
      response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
      )
      return response

  '''
  Endpoint to handle GET requests 
  for movies.
  '''
  '''
    [GET all movies endpoint]
    Returns:
        movies: all movies
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    return jsonify(
        {
          "success": True,
          "movies":[movie.format() for movie in movies]
        })

  '''
    [POST Add a  movie endpoint]
    Input :
        title : title of the movie
        releaseDate : date of release of the movie
    Returns:
        created : created movie id
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movies(payload):
    body = request.get_json()
    title =  body.get("title", None)
    releaseDate=  body.get("releaseDate", None)
    try:
        newMovie = Movie(title =title ,releaseDate=releaseDate)
        newMovie.insert()
        return jsonify(
          {
            "success": True,
            "created": newMovie.id
          })
    except:
            abort(422)

  '''
  Endpoint to handle GET requests 
  for actors.
  '''
  '''
    [GET all actors endpoint]
    Returns:
        actors: all actors
  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    return jsonify(
        {
          "success": True,
          "actors":[actor.format() for actor in actors]
        })

  '''
    [POST Add a  actor endpoint]
    Input :
        name : name of the actor
        age : age of the actor
        gender : gender of the actor
    Returns:
        created : created actor id
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actors(payload):
    body = request.get_json()
    name =  body.get("name", None)
    age =  body.get("age", None)
    gender=  body.get("gender", None)
    try:
        newActor = Actor(name=name, age=age, gender=gender)
        newActor.insert()
        return jsonify(
          {
            "success": True,
            "created": newActor.id
          })
    except:
            abort(422)

  '''
    [DELETE a  movie endpoint]
    Path Param :
        movie_id : integer
    Returns:
        deleted : deleted movie id
  '''
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload,movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    movie.delete()
    return jsonify(
      {
        "success": True,
        "deleted": movie_id
      })

  '''
    [DELETE a  actor endpoint]
    Path Param :
        actor_id : integer
    Returns:
        deleted : deleted actor id
  '''
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload,actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    actor.delete()
    return jsonify(
      {
        "success": True,
        "deleted": actor_id
      })

  '''
    [PATCH Edit a  actor endpoint]
    Input :
        name : name of the actor
        age : age of the actor
        gender : gender of the actor
    Returns:
        updated : updated actor id
        name : name of the actor
        age : age of the actor
        gender : gender of the actor
  '''
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actors(payload,actor_id):
    body = request.get_json()
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if not actor:
        abort(404)
    try:
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')
        if new_name:
            actor.name = new_name
        if new_age:
            actor.age = new_age
        if new_gender:
            actor.gender = new_gender
        actor.update()
        updated_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    except BaseException:
        abort(400)

    return jsonify(
        {
        'success': True,
        "updated_actor": updated_actor.format()
        })

  '''
    [PATCH Edit a  movie endpoint]
    Input :
        title : title of the movie
        releaseDate : releaseDate of the movie
    Returns:
        updated : updated movie id
        title : title of the movie
        releaseDate : releaseDate of the movie
  '''
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movies(payload,movie_id):
    body = request.get_json()
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if not movie:
        abort(404)
    try:
        new_title = body.get('title')
        new_releaseDate = body.get('releaseDate')
        if new_title:
            movie.title = new_title
        if new_releaseDate:
            movie.releaseDate = new_releaseDate
        movie.update()
        updated_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    except BaseException:
        abort(400)

    return jsonify(
        {
        'success': True,
        "updated_movie": updated_movie.format()
        })

  ''' 
  Error handlers for all expected errors 
  '''
  # 404 - Resource Not found
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource Not found"
      }), 404

  # 422 - Unprocessable entry
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable entry"
    }), 422

  # 400 - Bad Request
  @app.errorhandler(400)
  def badrequest(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
      }), 400

  # 405 - Method Not allowed
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

  # 500 - Internal Server Error
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401

  return app

app = create_app()

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port , debug=True)
