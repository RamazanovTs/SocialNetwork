from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    body = db.Column(db.String(256))
    like = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like = db.Column(db.Integer, default=0)

    def like_toggle(self, user_id):
        existing_like = Like.query.filter_by(post_id=self.id, user_id=user_id).first()

        if existing_like:
            db.session.delete(existing_like)
            self.like -= 1
        else:
            new_like = Like(post_id=self.id, user_id=user_id)
            db.session.add(new_like)
            self.like += 1

        db.session.commit()

    @property
    def like_count(self):
        return self.like

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id'),)
