from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Regexp, Email, EqualTo
from datetime import datetime
from models import User

class AuthorForm(FlaskForm):
    name = StringField('Author Name', validators=[
        DataRequired(message="❗ Author name is required."),
        Length(min=2, max=100, message="❗ Author name must be between 2 and 100 characters."),
        Regexp(r'^[A-Za-z\s .]+$', message="❗ Author name must contain only letters and spaces.")
    ])
    submit = SubmitField('Add Author')


class BookForm(FlaskForm):
    name = StringField('Book Name', validators=[
        DataRequired(message="❗ Book name is required."),
        Length(min=2, max=200, message="❗ Book name must be between 2 and 200 characters."),
        Regexp(r'^[A-Za-z\s]+$', message="❗ Book name must contain only letters and spaces.")
    ])

    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[
        DataRequired(message="❗ Publish date is required.")
    ])

    price = FloatField('Price', validators=[
        DataRequired(message="❗ Price is required."),
        NumberRange(min=0, message="❗ Price must be a positive number.")
    ])

    appropriate_age = SelectField('Appropriate Age', choices=[
        ('Under 8', 'Under 8'),
        ('8-15', '8-15'),
        ('Adults', 'Adults')
    ], validators=[
        DataRequired(message="❗ Appropriate age is required.")
    ])

    author_id = SelectField('Author', coerce=int, validators=[
        DataRequired(message="❗ Author is required.")
    ])

    image = FileField('Book Image', validators=[
        DataRequired(message="❗ Book image is required.")
    ])

    submit = SubmitField('Add Book')

    def validate_publish_date(self, field):
        if field.data > datetime.today().date():
            raise ValidationError("❗ Publish date cannot be in the future.")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')