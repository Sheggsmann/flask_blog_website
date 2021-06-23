from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from ..models import Post


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(4, 60), DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, field):
        if Post.query.filter_by(title=field.data).first():
            raise ValidationError('Post already exists!')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(4, 60), DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_title(self, field):
        if field.data != self.title.data and Post.query.filter_by(title=field.data).first():
            raise ValidationError('Post already exists')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')
    