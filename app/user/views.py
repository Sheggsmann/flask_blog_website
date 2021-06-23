from . import user
from .. import db
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from ..models import User
from .forms import UpdateAccountForm
from ..utils import save_image
import os
from datetime import datetime


@user.route('/user/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    image_file = url_for('static', filename=f'profile_pictures/{user.profile_picture}')
    return render_template('user.html', user=user, image_file=image_file, datetime=datetime)


@user.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_picture))
            filename = save_image(form.picture.data)
            current_user.profile_picture = filename
        current_user.name = form.name.data
        db.session.commit()
        flash('Account Updated Successfully', 'success')
        return redirect(url_for('.edit_profile'))
    form.name.data = current_user.name
    image_file = url_for('static', filename=f'profile_pictures/{current_user.profile_picture}')
    return render_template('edit_profile.html', form=form, image_file=image_file)
    

@user.route('/posts/<int:id>')
def user_posts(id):
    user = User.query.get_or_404(id)
    posts = user.posts.all()
    posts_num = len(posts)
    return render_template('user_posts.html', posts=posts, user=user, datetime=datetime, posts_num=posts_num)
    