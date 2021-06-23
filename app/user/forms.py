from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from ..models import User
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
    name = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['png', 'jpg'])
    ])
    submit = SubmitField('Update')


    def validate_name(self, field):
        if field.data != current_user.name and User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')