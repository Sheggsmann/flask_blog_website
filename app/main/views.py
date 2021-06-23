from flask import render_template, request, current_app
from . import main
from ..models import Post
from datetime import datetime


@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('home.html', posts=posts, datetime=datetime, pagination=pagination)


@main.route('/about')
def about():
    return render_template('about.html')


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@main.app_errorhandler(403)
def not_allowed(error):
    return render_template('errors/403.html'), 403