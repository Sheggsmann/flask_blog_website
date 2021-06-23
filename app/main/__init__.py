from flask import Blueprint

main = Blueprint(__name__, 'main')

from . import views
