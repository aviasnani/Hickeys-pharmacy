import os

 

class Config:
  SQLALCHEMY_DATABASE_URI = 'mysql://admin:Thisismydatabase/database.czg8iiuiehd4.eu-west-1.rds.amazonaws.com:3306/database'
  SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a warning
  SESSION_COOKIE_SECURE = True
  SECRET_KEY = 'Iaminevitable'
