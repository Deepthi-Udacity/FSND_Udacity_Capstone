import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZNc1F5YlpvQjFlT3I5cUdJV25rQSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHkzaWFtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MWI4ZjI3YjM2YmY2NTAwNzE1YmNkYWEiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjQxMTQxNDk1LCJleHAiOjE2NDEyMjc4OTUsImF6cCI6IlBHS01SbW40ekl1OGlXVHVlY0lObjdCM0V1ZGlBUnhTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.hlqlT5L3-SsxdfiWUyCxb_EMcYDv2NaWbgFB4DgpiPLWeNP2LQfiqz9bhuvFSSGIR8J8bQDe5jEQToihWhrEr3PaCeA6Sk0H6RjDQISLKfxNU01DNL895qEApKnCmcWwHcH4cUtwHDXqJHlU7PgkvEK31Q1v2zADaCvXMo32SpGsxbUZy7tWyr9a5qSczPk-FQnkF_FO-PF9FkS4A2LjeJz9A1mL0WCYyVg3lT84hJ3R8-cLYz6nwAGt8GXB8iH-gc07I9_3pcbYzzkFiawnvD-kQRA6gdKWYcx-ZlSHMeDB4SQtNcUEUWt3EDKsK-8sH-WRmfYDYysHJSA8y8SIQQ"
        self.director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZNc1F5YlpvQjFlT3I5cUdJV25rQSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHkzaWFtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MWI4ZWNkMGY2NGQ0YTAwNzJhZTc2YmEiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjQxMTQwOTA1LCJleHAiOjE2NDEyMjczMDUsImF6cCI6IlBHS01SbW40ekl1OGlXVHVlY0lObjdCM0V1ZGlBUnhTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.eRzLlF3hnykX1etV7jWIi1g_lMxV7eSTDtKfVFXp4jgeNj-BtIoaO3d5alfbCewOWglACpT1-JIjMn-h1kvUU6D6u3lvKLas9bwbiPrQpLv6Mq_UtTjb9B2MLqwnjahbBz5MwyeK861RIRA8jfLeoAcIlgEtss4DZcglQEd9P-nErJxyN_zqsxntePiNfCGLieuLQXEotO1mbD8kqK5rQoBjEKmfQuYsHRmSltaAUZ5IgOI7iqDX7U33F5AwTh2K6pYnIvNpWfOE7fNLDqPiYd6yHACxsyBDwf6SkekWRhKRL14jcVhbDGRrXrTe1ToNwxI8Iw3vNWoL7dSf8wjeHw"
        self.producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZNc1F5YlpvQjFlT3I5cUdJV25rQSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHkzaWFtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MWI4ZjI0YWZhMmNkMTAwNjllYThkYjIiLCJhdWQiOiJDYXN0aW5nQWdlbmN5IiwiaWF0IjoxNjQxMTQxODI4LCJleHAiOjE2NDEyMjgyMjgsImF6cCI6IlBHS01SbW40ekl1OGlXVHVlY0lObjdCM0V1ZGlBUnhTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.RvJlhbbvLUZ3bs7hCDMXw8_10HaKypQLk-q6Wk7gvSISk2JCdHE-Yu5F_wMP1cExkOLihnQ4AaF2BaKIp3M5NwSD4GvYM0D6moVk5d9FJkt6Pklg0LXcnOyISf2_WxII1zFEgoTQ9yUAEBrnTjWGHQCpkhn6rUIlxWXMV2SBBqcDN5ns3SxFlWrIqViqEZ7j6QIYFy0hm9G-IqkB0z6qxAdpxCHCcPyY6cl79eWEnW_5-hOuXip37_hkgEwaoRw0QP5sjCr0ItejNviAJB06kv7Tj4FzV-5wxb3VZxI16-ebkxZmpi8CpBtGWJBcSfKIcJ2jCY0ZPhBEHXqDRc3R0A"

        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagencytest"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name": "Test Actor",
            "age": 40,
            "gender": "Male"
            }
        self.new_movie = {
            "title" : "Test Movie",
            "releaseDate" : "2021-11-16"
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #Failing Test trying to make a call without token
    def test_without_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization header is expected.")

    # Test to get list of all movies successfully
    # Success test for Assistant role
    # Expected - 200 
    def test_get_movies(self):
        res = self.client().get("/movies", headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    # Test to get list of all actors successfully
    # Success test for Assistant role
    # Expected - 200 
    def test_get_actors(self):
        res = self.client().get("/actors", headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    # Test to delete a actor - to get 403 for Assistant role
    # Failure test for Assistant role
    # Expected - 403
    def test_delete_actor_403(self):
        res = self.client().delete("/actors/2", headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Access denied. Permission not found.")

    # Test to get list of all movies -405 Error
    # Expected - 405
    def test_get_movies_405(self):
        res = self.client().delete("/movies", headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    # Test to get list of all actors -405 Error
    # Expected - 405
    def test_get_actors_405(self):
        res = self.client().delete("/actors", headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    # Test to get Resource Not found error
    # Expected - 404
    def test_get_404(self):
        res = self.client().delete("/actor", headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not found")

    # Test to delete a actor successfully
    # Expected - 200
    # Success test for Director role
    # Delete a different actor in each attempt
    # def test_delete_actor(self):
    #     res = self.client().delete("/actors/2", headers={
    #         'Authorization': "Bearer {}".format(self.director_token)
    #     })
    #     data = json.loads(res.data)

    #     actor = Actor.query.filter(Actor.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 2)

    # Test to delete an actor -get 404
    # Expected - 404
    # Delete a different actor in each attempt
    def test_delete_actor_404(self):
        res = self.client().delete("/actors/2", headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not found")

    # Test to delete a movie -403 for Director
    # Expected - 403
    # Failure test for Director role
    # Delete a different movie in each attempt
    def test_delete_movie_403(self):
        res = self.client().delete("/movies/1", headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Access denied. Permission not found.")

    # Test to delete a movie successfully
    # Expected - 200
    # Success test for Producer role
    # Delete a different movie in each attempt
    # def test_delete_movie(self):
    #     res = self.client().delete("/movies/2", headers={
    #         'Authorization': "Bearer {}".format(self.producer_token)
    #     })
    #     data = json.loads(res.data)

    #     movie = Movie.query.filter(Movie.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 2)

    # Test to delete a movie -get 404
    # Expected - 404
    # Success test for Producer role
    def test_delete_movie_404(self):
        res = self.client().delete("/movies/2", headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not found")

    # Test to add a new actor successfully
    # Expected - 200
    def test_create_actor(self):
        res = self.client().post("/actors", json=self.new_actor , headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    # Test to get an error when an incorrect input is given
    # Expected - 422
    def test_create_actor_422(self):
        input = {
            "name": "Test Actor",
            "age": "f",
            "gender": "Male"
            }
        res = self.client().post("/actors", json=input , headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable entry")

    # Test to add a new movie successfully
    # Expected - 200
    def test_create_movie(self):
        res = self.client().post("/movies", json=self.new_movie, headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    # Test to update a movie successfully
    # Expected - 200
    def test_update_movie(self):
        input = {
            "releaseDate" : "2021-11-16"
            }
        res = self.client().patch("/movies/1", json=input, headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated_movie"])

    # Test to update a actor successfully
    # Expected - 200
    def test_update_actor(self):
        input = {
            "age" : "16"
            }
        res = self.client().patch("/actors/3", json=input, headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated_actor"])

    # Test to get 400 error when incorrect input is given
    # Expected - 400
    def test_update_actor_400(self):
        input = {
            "age" : "f"
            }
        res = self.client().patch("/actors/3", json=input, headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
