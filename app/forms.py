from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
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


class ReviewForm(FlaskForm):
    """Form for submitting a book review."""
    text = TextAreaField(
        "Your Review",
        validators=[
            DataRequired(message="Review text is required"),
            Length(min=5, max=2000, message="Review must be between 5 and 2000 characters")
        ],
        render_kw={"rows": 5, "placeholder": "Share your thoughts about this book..."}
    )
    stars = IntegerField(
        "Rating",
        validators=[
            DataRequired(message="Rating is required"),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5 stars")
        ]
    )
    submit = SubmitField("Submit Review")


class EditProfileForm(FlaskForm):
    """Form for editing user profile."""
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
    bio = TextAreaField(
        "Bio",
        validators=[Length(max=500, message="Bio must be less than 500 characters")],
        render_kw={"rows": 4, "placeholder": "Tell us about yourself..."}
    )
    submit = SubmitField("Update Profile")

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, field):
        """Check if new username already exists."""
        if field.data != self.original_username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError("Username already exists. Choose a different one.")

    def validate_email(self, field):
        """Check if new email already exists."""
        if field.data != self.original_email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError("Email already in use. Choose a different one.")
