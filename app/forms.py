from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """Form for user login."""
    username_or_email = StringField(
        "Username or Email",
        validators=[DataRequired(message="Username or email is required")]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required")]
    )
    submit = SubmitField("Log In")


class SignupForm(FlaskForm):
    """Form for user registration."""
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=80, message="Username must be between 3 and 80 characters")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Invalid email address")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Password confirmation is required"),
            EqualTo("password", message="Passwords must match")
        ]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        """Check if username already exists."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already exists. Choose a different one.")

    def validate_email(self, field):
        """Check if email already exists."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already in use. Choose a different one.")

