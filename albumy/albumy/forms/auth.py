from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from albumy.models import User


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='The Username should contain only a-z, A-Z, 0-9.')])
    password = PasswordField("Password", validators=[DataRequired(), Length(5, 128), EqualTo('password2')])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("The Email is already in use.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("The Username is already in use.")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(5, 128)])
    remember_me = BooleanField('remember me', default=True)
    submit = SubmitField()
