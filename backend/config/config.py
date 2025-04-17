import os

basedir = os.path.abspath(os.path.dirname(__file__)) # (co-pilot)
instance_path = os.path.join(basedir, '..', 'instance')  # One level up
if not os.path.exists(instance_path): # (co-pilot)
    os.makedirs(instance_path) # (co-pilot) 

class Config:
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'database.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a warning
  SECRET_KEY = 'Iaminevitable'
