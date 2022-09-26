# from datetime import datetime

from flask import current_app
from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, URLSafeTimedSerializer
# from itsdangerous import URLSafeSerializer as Serializer

from flaskapp import db, login_manager
import jwt
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        # v = jwt.encode(
        #     {
        #         "confirm": self.id,
        #         "exp": datetime.datetime.now(tz=datetime.timezone.utc)
        #                + datetime.timedelta(seconds=expires_sec)
        #     },
        #     current_app.config['SECRET_KEY'],
        #     algorithm="HS256"
        # )

        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        v = s.dumps({'user_id': self.id}).decode('utf-8')
        return v

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"