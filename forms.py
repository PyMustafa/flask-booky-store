from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Regexp
from datetime import datetime

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
