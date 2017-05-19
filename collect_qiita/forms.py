from flask_wtf.form import Form
from wtforms.fields import StringField, TextField, PasswordField, HiddenField, SubmitField, BooleanField
# from wtforms.validators import Required
from wtforms_alchemy import model_form_factory
from wtforms.validators import Required, Email, DataRequired, Length
from .util.validators import Unique
from .models import User
from . import db

"""
BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_sessin(self):
        return db.session

class UserPasswordForm(ModelForm):
    class Meta:
        model = User
        include_foreign_keys = True
        field_args = {'username':{'ユーザ名'},
                      'password':{'パスワード'}}

"""

class EmailPasswordForm(Form):
    username = StringField('Username', validators=[
        DataRequired(message='ユーザー名が未登録です'),
        Length(max=10,message='ユーザー名は10文字までにして下さい')
    ])

    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])

"""
class EmailPasswordForm(Form):
    email = TextField('Email', validators=[Required(), Email(),
    Unique(
        User,
        User.email,
        message='There is already an account with that email.')])
    password = PasswordField('Password', validators=[Required()])
"""

class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')

class EmailForm(Form):
    email = TextField('Email', validators=[Required(), Email()])

class PasswordForm(Form):
    password = PasswordField('Email', validators=[Required()])
