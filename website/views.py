from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Post, User, Like

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.all()
    authors = User.query.all()
    return render_template('Home.html', user=current_user, posts=posts, authors=authors)

@views.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == "POST":
        Title = request.form.get('title')
        Body = request.form.get('body')
        new_post = Post(title=Title, body=Body, like=0, user_id=current_user.id)
        if len(Title) < 5:
            flash('Title must be at least 5 characters!', category='error')
        elif len(Body) < 8:
            flash('Content must be at least 8 characters!', category='error')
        else:
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template('Post.html', user=current_user)

@views.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.like_toggle(current_user.id)
    return redirect(request.referrer)

@views.route('/myposts', methods=['GET'])
@login_required
def myposts():
    posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('myposts.html', user=current_user, posts=posts)

@views.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(post_id=post_id).first()
    if post.user_id == current_user.id:
        db.session.delete(post)
        if like:
            db.session.delete(like)
        db.session.commit()
        flash('Post deleted successfully!', category='success')
    else:
        flash('You are not authorized to delete this post.', category='error')
    return redirect(url_for('views.myposts'))

@views.route('/users/<int:user_id>/posts', methods=['GET'])
@login_required
def userpost(user_id):
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('userpost.html', user=user, posts=posts)