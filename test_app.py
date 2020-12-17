import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import db, Actor, Movie, setup_db, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9jMHQ1TVRrTllGeUhsX2NTcHVhNyJ9.eyJpc3MiOiJodHRwczovL2xhd3JlbmNlcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc0MDk0MDU5NTU4MTgxNzkyMDkiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9sYXdyZW5jZXAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwODIyMjkyOSwiZXhwIjoxNjA4MzA5MzI5LCJhenAiOiJsclJUUkJib09scUxWTFl4U0N0bU4zbVQwN29VdFJ1QyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.uSW_Xjan6DLU4ufgKfwS7_EFIMogY7NUk7QJt5Kskrt7c6374b2R5jIckoOqpPbBB6loXYfVaXyND16X7ZrN4jfRenlZ5Wa9XrmyvDMHXYAM8xOtk5DK32VrqkKzc4uvKv76YO2KTq0M-3vr2LZ8VHZomcJNA-W4tPmrzZeILIdB2pL1RgNVu-TV5RJTrZJU7dU0Ilp4hQ4NgU1nIHOWMxfnDgzbbr88-dby8KLgbrlcktN6ZE4nbCBpPoI3P-uN2g8IwKjEFJ6Bxwdflhl2MeDKUi8jjFXvdT7jEHtrRk584bFxm6hwgt_5wMlVqidFwkhT7MmS25K5iHbYUW0Lfg'

class AgencyTest(unittest.TestCase):

   def setUp(self):
      """Define test variables and initialize app."""
      self.app = create_app()
      self.client = self.app.test_client
      self.headers = {'Content-Type': 'application/json'}
      self.database_name = 'agency'
      self.database_path =  'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
      setup_db(self.app, self.database_path)

      # binds the app to the current context
      with self.app.app_context():
         self.db = SQLAlchemy()
         self.db.init_app(self.app)
         # create all tables
         self.db.create_all()
    
   def tearDown(self):
      """Executed after reach test"""
      pass


   def test_public_add_actor(self):
      new_actor = {
         'name': 'Dwayne Johnson',
         'age': 50,
         'gender': 'male'
      }

      res = self.client().post('/actors', json=new_actor)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
   
    
   def test_add_actor(self):
      new_actor = {
         'name': 'Dwayne Johnson',
         'age': 50,
         'gender': 'male'
      }
      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().post('/actors', json=new_actor, headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)

   def test_public_get_actors(self):
      res = self.client().get('/actors')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
    
   def test_get_actors(self):
      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().get('/actors', headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)

   def test_public_update_actor(self):
      updated_actor = {
         'name': 'Carl'
      }

      res = self.client().patch('/actors/1', json=updated_actor)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
    
   def test_update_actor(self):

      actor = Actor(name='Dwaine Johnsen', age=50,
                           gender='male')
      actor.insert()
      actor_id = actor.id

      updated_actor = {
         'name': 'Dwayne Johnson'
      }

      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().patch(f'/actors/{actor_id}', json=updated_actor, headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)

   def test_public_delete_actor(self):

      res = self.client().delete('/actors/1', )
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
    
   def test_delete_actor(self):
      actor = Actor(name='Bruce Willis', age=60,
                           gender='male')
      actor.insert()
      actor_id = actor.id

      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().delete(f'/actors/{actor_id}', headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['delete'], str(actor_id))


   def test_public_add_movie(self):
      new_movie = {
         'title': 'Transformers',
         'release_date': '01.12.2010'
      }

      res = self.client().post('/movies', json=new_movie)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
   
    
   def test_add_movie(self):
      new_movie = {
         'title': 'Transformers',
         'release_date': '01-10-2010'
      }
      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().post('/movies', json=new_movie, headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)

   def test_public_get_movies(self):
      res = self.client().get('/movies')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
    
   def test_get_movies(self):
      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().get('/movies', headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)

   def test_public_update_movie(self):
      updated_movie = {
         'title': 'Avengers'
      }

      res = self.client().patch('/movies/1', json=updated_movie)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
    
   def test_update_movie(self):
      movie = Movie(title='Mission Impossible', release_date='January-5-2010')
      movie.insert()
      movie_id = movie.id

      updated_movie = {
         'title': 'Mission Impossible 2'
      }

      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().patch(f'/movies/{movie_id}', json=updated_movie, headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)

   def test_public_delete_movie(self):

      res = self.client().delete('/movies/1', )
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 401)
    
   def test_delete_movie(self):
      movie = Movie(title='Avengers', release_date='March-25-2010')
      movie.insert()
      movie_id = movie.id

      self.headers.update({'Authorization': 'Bearer ' + TOKEN})

      res = self.client().delete(f'/movies/{movie_id}', headers=self.headers)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['delete'], str(movie_id))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()