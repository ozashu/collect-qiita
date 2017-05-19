from sqlalchemy.orm import synonym
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime, date
from . import db, bcrypt

def verify_password(hash_pass, original_pass):
    return check_password_hash(hash_pass, original_pass)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True, nullable=False)
    fav = db.relationship("Fav", backref=db.backref('users'))
 
    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def is_authenticated(self):
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
            return False
    
    def get_id(self):
        return self.username

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    @staticmethod
    def login(username, password):

        u = User.query.filter_by(username=username).first()
        if u and verify_password(u.password, password):
            return u
        return None

"""
    @classmethod
    def authenticate(cls, query, email, password):
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return u'<User id={self.id} email={self.email!r}>'.format(self=self)
"""

class Fav(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(200), unique=True)
    title = db.Column(db.String(200), unique=True)
    publish_date = db.Column(db.DateTime,nullable=True, default=datetime.now)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Entry id={id} user_id={user_id }username={username} url={url}>'.format(id=self.id,user_id=self.user_id,  username=self.username, url=self.url)

def init():
    db.create_all()
