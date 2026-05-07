from uuid import uuid4

from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_login import current_user, login_user

from app.forms import LoginForm, SignupForm
from app.extensions import db
from app.models import Book, Comment, Rating, User, WantToRead


def seed_books_if_empty():
    if Book.query.first():
        return

    books = [
        Book(
            title="The Midnight Library",
            author="Matt Haig",
            description="A novel about choices, regrets, and the different lives a person could have lived.",
            rating=4.2,
            reads=1247
        ),
        Book(
            title="Atomic Habits",
            author="James Clear",
            description="A practical book about building good habits and breaking bad ones through small daily changes.",
            rating=4.6,
            reads=2100
        ),
        Book(
            title="Project Hail Mary",
            author="Andy Weir",
            description="A science fiction story about survival, problem solving, and saving humanity.",
            rating=4.5,
            reads=1680
        ),
        Book(
            title="Normal People",
            author="Sally Rooney",
            description="A story about friendship, love, communication, and growing up.",
            rating=4.0,
            reads=980
        ),
        Book(
            title="Dune",
            author="Frank Herbert",
            description="A classic science fiction novel about politics, power, religion, and survival on a desert planet.",
            rating=4.4,
            reads=1900
        ),
        Book(
            title="Before the Coffee Gets Cold",
            author="Toshikazu Kawaguchi",
            description="A gentle story about time travel, memory, regret, and human connection.",
            rating=4.1,
            reads=870
        ),
    ]

    db.session.add_all(books)
    db.session.commit()

    comments = [
        Comment(
            username="Reader1",
            book_id=books[0].id,
            stars=4,
            text="Great book! The idea was simple but really interesting."
        ),
        Comment(
            username="Alice",
            book_id=books[0].id,
            stars=5,
            text="I loved the message of this book."
        ),
        Comment(
            username="Tom",
            book_id=books[1].id,
            stars=5,
            text="Very useful and easy to understand."
        ),
    ]

    db.session.add_all(comments)
    db.session.commit()


def format_review(comment):
    return {
        "username": comment.username,
        "book_id": comment.book_id,
        "book_title": comment.book.title,
        "stars": comment.stars,
        "text": comment.text,
        "time": comment.created_at.strftime("%Y-%m-%d")
    }


def build_rating_summary(book):
    all_stars = [rating.stars for rating in book.ratings]
    all_stars += [comment.stars for comment in book.comments]

    total = len(all_stars)

    if total == 0:
        return {
            "average": book.rating,
            "total": 0,
            "distribution": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        }

    distribution = {}

    for star in [5, 4, 3, 2, 1]:
        count = all_stars.count(star)
        distribution[star] = round(count / total * 100)

    average = round(sum(all_stars) / total, 1)

    return {
        "average": average,
        "total": total,
        "distribution": distribution
    }

def get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid4())

    return session["session_id"]


def get_display_rating(book):
    rating_summary = build_rating_summary(book)
    return rating_summary["average"]


def register_routes(app: Flask) -> None:
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/profile")
    @app.route("/profile.html")
    def profile():
        return render_template("profile.html")

    @app.route("/login", methods=["GET", "POST"])
    @app.route("/login.html", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        form = LoginForm()

        if form.validate_on_submit():
            identifier = form.username_or_email.data.strip()
            user = User.query.filter(
                db.or_(
                    User.username == identifier,
                    User.email == identifier,
                )
            ).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("profile"))

            form.password.errors.append("Invalid username/email or password.")

        return render_template("login.html", form=form)

    @app.route("/signup", methods=["GET", "POST"])
    @app.route("/signup.html", methods=["GET", "POST"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        form = SignupForm()

        if form.validate_on_submit():
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip().lower(),
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("profile"))

        return render_template("signup.html", form=form)

    @app.route("/edit-profile")
    @app.route("/edit-profile.html")
    def edit_profile():
        return render_template("edit-profile.html")

    @app.route("/read")
    @app.route("/read.html")
    def read():
        return render_template("read.html")

    @app.route("/currently-reading")
    @app.route("/currently-reading.html")
    def currently_reading():
        return render_template("currently-reading.html")

    @app.route("/to-be-read")
    @app.route("/to-be-read.html")
    def to_be_read():
        return render_template("to-be-read.html")

    @app.route("/did-not-finish")
    @app.route("/did-not-finish.html")
    def did_not_finish():
        return render_template("did-not-finish.html")

    @app.route("/my-reviews")
    @app.route("/my-reviews.html")
    def my_reviews():
        return render_template("my-reviews.html")
