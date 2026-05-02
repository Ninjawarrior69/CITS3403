from uuid import uuid4

from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_login import current_user

from app.extensions import db
from app.models import Book, Comment, Rating, WantToRead


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
        seed_books_if_empty()

        trending_books = Book.query.order_by(Book.created_at.desc()).limit(6).all()
        most_read_books = Book.query.order_by(Book.reads.desc()).limit(5).all()

        recent_comments = (
            Comment.query
            .order_by(Comment.created_at.desc())
            .limit(4)
            .all()
        )

        reviews = [format_review(comment) for comment in recent_comments]

        return render_template(
            "home.html",
            trending_books=trending_books,
            most_read_books=most_read_books,
            reviews=reviews
        )

    @app.route("/profile")
    @app.route("/profile.html")
    def profile():
        return render_template("profile.html")

    @app.route("/login")
    @app.route("/login.html")
    def login():
        return render_template("login.html")

    @app.route("/signup")
    @app.route("/signup.html")
    def signup():
        return render_template("signup.html")

    @app.route("/edit-profile")
    @app.route("/edit-profile.html")
    def edit_profile():
        return render_template("edit-profile.html")

    @app.route("/book/<int:book_id>")
    def book_detail(book_id):
        seed_books_if_empty()

        book = Book.query.get_or_404(book_id)

        session_id = get_session_id()
        
        want_to_read = WantToRead.query.filter_by(
            book_id=book.id,
            session_id=session_id
        ).first()
        
        want_to_read_count = WantToRead.query.filter_by(book_id=book.id).count()

        author = {
            "bio": f"{book.author} is the author of this book. More author information will be added later.",
            "followers": 0,
            "books": Book.query.filter_by(author=book.author).count()
        }

        reviews = [format_review(comment) for comment in book.comments]
        rating_summary = build_rating_summary(book)
        user_rating = session.get(f"book_{book.id}_rating", 0)

        return render_template(
            "book_detail.html",
            book=book,
            author=author,
            reviews=reviews,
            rating_summary=rating_summary,
            user_rating=user_rating,
            want_to_read=want_to_read is not None,
            want_to_read_count=want_to_read_count
        )

    @app.route("/book/<int:book_id>/rate", methods=["POST"])
    def rate_book(book_id):
        book = Book.query.get_or_404(book_id)

        try:
            stars = int(request.form.get("stars", 0))
        except ValueError:
            abort(400)

        if stars < 1 or stars > 5:
            abort(400)

        rating = Rating(
            book_id=book.id,
            username=current_user.username if current_user.is_authenticated else "Anonymous",
            user_id=current_user.id if current_user.is_authenticated else None,
            stars=stars
        )

        db.session.add(rating)
        db.session.commit()

        session[f"book_{book.id}_rating"] = stars

        return redirect(url_for("book_detail", book_id=book.id))

    @app.route("/book/<int:book_id>/review", methods=["POST"])
    def post_review(book_id):
        book = Book.query.get_or_404(book_id)

        text = request.form.get("text", "").strip()

        try:
            stars = int(request.form.get("stars", 0))
        except ValueError:
            abort(400)

        if not text or stars < 1 or stars > 5:
            abort(400)

        comment = Comment(
            book_id=book.id,
            username=current_user.username if current_user.is_authenticated else "Anonymous",
            user_id=current_user.id if current_user.is_authenticated else None,
            text=text,
            stars=stars
        )

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("book_detail", book_id=book.id))
    
    @app.route("/book/<int:book_id>/want-to-read", methods=["POST"])
    def toggle_want_to_read(book_id):
        book = Book.query.get_or_404(book_id)
        session_id = get_session_id()

        existing = WantToRead.query.filter_by(
            book_id=book.id,
            session_id=session_id
        ).first()

        if existing:
            db.session.delete(existing)
        else:
            want_to_read = WantToRead(
                book_id=book.id,
                session_id=session_id,
                user_id=current_user.id if current_user.is_authenticated else None
            )
            db.session.add(want_to_read)

        db.session.commit()

        return redirect(url_for("book_detail", book_id=book.id))