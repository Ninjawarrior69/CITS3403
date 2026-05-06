from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship("Comment", backref="user", lazy=True)
    ratings = db.relationship("Rating", backref="user", lazy=True)
    want_to_reads = db.relationship("WantToRead", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    reads = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship(
        "Comment",
        backref="book",
        lazy=True,
        cascade="all, delete-orphan"
    )

    ratings = db.relationship(
        "Rating",
        backref="book",
        lazy=True,
        cascade="all, delete-orphan"
    )

    want_to_reads = db.relationship(
        "WantToRead",
        backref="book",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, default="Anonymous")
    text = db.Column(db.Text, nullable=False)
    stars = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, default="Anonymous")
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Rating {self.id}>"
    

class WantToRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("book_id", "session_id", name="unique_book_session_want_to_read"),
    )

    def __repr__(self) -> str:
        return f"<WantToRead book={self.book_id}>"