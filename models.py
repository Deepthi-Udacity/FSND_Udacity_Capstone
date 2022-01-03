import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

# DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
# DB_USER = os.getenv('DB_USER', 'student')
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'student')
# DB_NAME = os.getenv('DB_NAME', 'castingagency')

# DB_PATH = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
DB_PATH = os.getenv('DATABASE_URL','postgres://kongfkxwwongyq:897d9c27cbd78535c7d8f3b9603cbd018630055662fc2cbaab7ae8981ef0f852@ec2-3-213-41-172.compute-1.amazonaws.com:5432/ddlsms9to8onoo')
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
      db.app = app
      db.init_app(app)
      db.create_all()

'''
Cast
'''
Cast = db.Table('cast',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)

'''
Movie

'''
class Movie(db.Model):  
  __tablename__ = 'movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  releasedate = Column(String)
  actors = db.relationship('Actor', secondary=Cast, backref=db.backref('movies', lazy=True))

  def __init__(self, title, releasedate):
    self.title = title
    self.releasedate = releasedate

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'releasedate': self.releasedate
    }

'''
Actor

'''
class Actor(db.Model):  
  __tablename__ = 'actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }