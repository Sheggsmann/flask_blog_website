from flask import Blueprint

post = Blueprint(__name__, 'post')

from . import views