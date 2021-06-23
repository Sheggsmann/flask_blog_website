from flask import Blueprint

auth = Blueprint(__name__, 'auth')

from . import views