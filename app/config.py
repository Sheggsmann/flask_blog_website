import os

class Config:
    SECRET_KEY = 'to be changed later'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = r'Flask_tutorials\flaskblog\app\static\profile_pictures'
    ALLOWED_EXTENSTIONS = ['png', 'jpeg', 'jpg', 'gif']
    POSTS_PER_PAGE = 6
    COMMENTS_PER_PAGE = 5