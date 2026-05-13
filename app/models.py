from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

favorite_books = db.Table(
    "favorite_books",

    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True
    ),

    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id"),
        primary_key=True
    )
)

followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text, default="")
    avatar = db.Column(db.String(255), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    following = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic"
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    comments = db.relationship("Comment", backref="user", lazy=True)
    ratings = db.relationship("Rating", backref="user", lazy=True)
    shelf_items = db.relationship("ShelfItem", backref="user", lazy=True)
    favorite_books = db.relationship(
        "Book",
        secondary=favorite_books,
        backref="favorited_by",
        lazy=True
    )

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def get_to_be_read_books(self) -> list["Book"]:
        """Return books the user has marked as to-be-read."""
        return (
            Book.query.join(ShelfItem, ShelfItem.book_id == Book.id)
            .filter(ShelfItem.user_id == self.id)
            .order_by(ShelfItem.created_at.desc())
            .all()
        )

    def get_read_books(self) -> list["Book"]:
        """Return books the user has interacted with via ratings or comments."""
        rated_book_ids = (
            db.session.query(Rating.book_id)
            .filter(Rating.user_id == self.id)
            .subquery()
        )
        commented_book_ids = (
            db.session.query(Comment.book_id)
            .filter(Comment.user_id == self.id)
            .subquery()
        )

        return (
            Book.query
            .filter(
                db.or_(
                    Book.id.in_(db.select(rated_book_ids.c.book_id)),
                    Book.id.in_(db.select(commented_book_ids.c.book_id)),
                )
            )
            .order_by(Book.title.asc())
            .all()
        )

    def get_books_by_status(self, status: str) -> list["Book"]:
        """Return user books for a supported status key."""
        normalized = status.strip().lower().replace("-", "_")

        if normalized in {"to_be_read", "want_to_read"}:
            return self.get_to_be_read_books()

        if normalized == "read":
            return self.get_read_books()

        return []

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openlibrary_id = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    publish_year = db.Column(db.Integer, nullable=True)
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
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    session_id = db.Column(db.String(120), nullable=True)

    __table_args__ = (db.UniqueConstraint("user_id", "book_id", name="unique_user_book_review"),)

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

    current_page = db.Column(db.Integer, default=0)
  

    __table_args__ = (
        db.UniqueConstraint("book_id", "session_id", name="unique_book_session_shelf_item"),
        db.UniqueConstraint("book_id", "user_id", name="unique_book_user_shelf_item")
    )

    def __repr__(self) -> str:
        return f"<ShelfItem book={self.book_id} status={self.status}>"