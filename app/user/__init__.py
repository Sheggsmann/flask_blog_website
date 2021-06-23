from flask import Blueprint

user = Blueprint(__name__, 'user')

from . import views