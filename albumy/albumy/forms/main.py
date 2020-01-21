from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class DescriptionForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired(), Length(0, 500)])
    submit = SubmitField()


class TagForm(FlaskForm):
    tag = StringField('Add Tag (use space to separate)', validators=[DataRequired(), Length(0, 64)])
    submit = SubmitField()


class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField()
