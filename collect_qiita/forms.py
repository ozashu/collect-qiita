from flask.ext.wtf import Form
from wtforms.field import TextField, PasswordField
from wtforms.validators import Required, Email
from util.valodators import Unique
from models import User

class EmailPasswordForm(Form):
    email = TextField('Email', validators=[Required(), Email(),
    Unique(
        User,
        User.email,
        message='There is already an account with that email.'])
    password = PasswordField('Password', validators=[Required()]

class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class EmailForm(Form):
    email = TextField('Email', validators=[Required(), Email()])

class PasswordForm(Form):
    password = PasswordField('Email', validators=[Required()])
