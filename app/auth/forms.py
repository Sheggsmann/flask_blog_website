from . import auth
from .. import db
from ..models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Regexp(r'\w+@\w+.com$')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 20)])
    email = StringField('Email', validators=[DataRequired(), Regexp(r'\w+@\w+.com$')])
    password = PasswordField('Password', validators=[
        DataRequired(), Regexp(r'[a-zA-Z0-9]+')
    ])
    confirm_password = PasswordField('Confirm', validators=[
        DataRequired(),
         EqualTo('password', 'Passwords do not match.')
    ])
    picture = FileField('Profile Picture', validators=[
        FileAllowed(['png', 'jpg'])
    ])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use.')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')


