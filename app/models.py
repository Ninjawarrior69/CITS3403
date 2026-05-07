from datetime import datetime

from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship("Comment", backref="user", lazy=True)
    ratings = db.relationship("Rating", backref="user", lazy=True)
    shelf_items = db.relationship("ShelfItem", backref="user", lazy=True)

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

    shelf_item = db.relationship(
        "ShelfItem",
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
    session_id = db.Column(db.String(120), nullable=True)

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, default="Anonymous")
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    session_id = db.Column(db.String(120), nullable=True)

    def __repr__(self) -> str:
        return f"<Rating {self.id}>"
    

class ShelfItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    session_id = db.Column(db.String(120), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  

    __table_args__ = (
        db.UniqueConstraint("book_id", "session_id", name="unique_book_session_shelf_item"),
        db.UniqueConstraint("book_id", "user_id", name="unique_book_user_shelf_item")
    )

    def __repr__(self) -> str:
        return f"<ShelfItem book={self.book_id} status={self.status}>"