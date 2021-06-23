from . import post
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import current_user, login_required
from .. import db
from ..models import Post, Comment
from .forms import PostForm, EditPostForm, CommentForm
from datetime import datetime


@post.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('app.main.home'))
    return render_template('create_post.html', form=form)   


@post.route('/post/<title>', methods=['GET', 'POST'])
@login_required
def active_post(title):
    post = Post.query.filter_by(title=title).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.active_post', title=post.title))
    return render_template('posts.html', post=post, datetime=datetime, form=form, comments=comments, pagination=pagination, title=title)


@post.route('/edit_post/<title>', methods=['GET', 'POST'])
@login_required
def edit_post(title):
    form = EditPostForm()
    post = Post.query.filter_by(title=title).first()
    if not post:
        return redirect(url_for('app.main.home'))
    if request.method == 'POST':
        if form.validate_on_submit() and post.author.email == current_user.email:
            post.title = form.title.data
            post.body = form.body.data
            db.session.add(post)
            db.session.commit()
            flash('Post Updated Successfully', 'success')
            return redirect(url_for('app.main.home'))
        else:
            flash('You are not the author of this post')
            return redirect(url_for('app.main.home'))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@post.route('/delete/<title>', methods=['POST'])
@login_required
def delete_post(title):
    post = Post.query.filter_by(title=title).first()
    if current_user.email != post.author.email:
        abort(403)
    for comment in post.comments.all():
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted Successfully', 'success')
    return redirect(url_for('app.main.home'))


@post.route('/delete_comment/<int:id>', methods=['POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)
    if current_user.email != post.author.email:
        abort(403)
    title = comment.post.title
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully', 'success')
    return redirect(url_for('.active_post', title=title))
