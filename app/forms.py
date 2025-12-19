from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[
        DataRequired(), 
        Length(min=3, max=200, message='Product name must be between 3 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(), 
        Length(min=10, message='Description must be at least 10 characters long')
    ])
    price = FloatField('Price (₹)', validators=[
        DataRequired(), 
        NumberRange(min=1, message='Price must be greater than 0')
    ])
    category = SelectField('Category', choices=[
        ('Decorative Items', 'Decorative Items'),
        ('Utensils', 'Utensils'),
        ('Religious Items', 'Religious Items'),
        ('Lamps & Diyas', 'Lamps & Diyas'),
        ('Statues', 'Statues'),
        ('Tableware', 'Tableware'),
        ('Home Decor', 'Home Decor'),
        ('Others', 'Others')
    ], validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only! (JPG, PNG, GIF)')
    ])
    submit = SubmitField('Save Product')
