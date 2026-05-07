from uuid import uuid4
from itertools import islice

from flask import Flask, render_template, abort, request, redirect, url_for, session, flash, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import or_

from app.forms import LoginForm, SignupForm, EditProfileForm
from app.extensions import db
from app.models import Book, Comment, Rating, User, WantToRead, ShelfItem


def chunked(iterable, size):
    it = iter(iterable)
    return iter(lambda: list(islice(it, size)), [])


def get_shelf_counts(session_id):
    return {
        "read": ShelfItem.query.filter_by(session_id=session_id, status="Read").count(),
        "currently_reading": ShelfItem.query.filter_by(session_id=session_id, status="Currently Reading").count(),
        "to_be_read": ShelfItem.query.filter_by(session_id=session_id, status="To Be Read").count(),
        "did_not_finish": ShelfItem.query.filter_by(session_id=session_id, status="Did Not Finish").count(),
    }


def seed_books_if_empty():
    if Book.query.first():
        return

    books = [
        Book(title="The Midnight Library", author="Matt Haig", description="A novel about choices, regrets, and the different lives a person could have lived.", pages=304, cover_url="https://m.media-amazon.com/images/I/71qsovx-x6L._AC_UF1000,1000_QL80_.jpg", rating=4.2, reads=1247),
        Book(title="Atomic Habits", author="James Clear", description="A practical book about building good habits and breaking bad ones through small daily changes.", pages=320, cover_url="https://m.media-amazon.com/images/I/81kg51XRc1L.jpg", rating=4.6, reads=2100),
        Book(title="Project Hail Mary", author="Andy Weir", description="A science fiction story about survival, problem solving, and saving humanity.", pages=496, cover_url="https://m.media-amazon.com/images/I/91ENQs2KLAL._AC_UF1000,1000_QL80_.jpg", rating=4.5, reads=1680),
        Book(title="Normal People", author="Sally Rooney", description="A story about friendship, love, communication, and growing up.", pages=288, cover_url="https://m.media-amazon.com/images/I/61nFGO425OL.jpg", rating=4.0, reads=980),
        Book(title="Dune", author="Frank Herbert", description="A classic science fiction novel about politics, power, religion, and survival on a desert planet.", pages=489, cover_url="https://m.media-amazon.com/images/I/71oO1E-XPuL.jpg", rating=4.4, reads=1900),
        Book(title="Before the Coffee Gets Cold", author="Toshikazu Kawaguchi", description="A gentle story about time travel, memory, regret, and human connection.", pages=208, cover_url="https://m.media-amazon.com/images/I/71kW0ESYl5L.jpg", rating=4.1, reads=870),
        Book(title="Sunrise on the Reaping", author="Suzanne Collins", description="The newest book in The Hunger Games series", pages=400, cover_url="https://m.media-amazon.com/images/I/81RUJzM+wvL._UF894,1000_QL80_.jpg", rating=4.6, reads=2300),
    ]

    db.session.add_all(books)
    db.session.commit()

    comments = [
        Comment(username="Reader1", book_id=books[0].id, stars=4, text="Great book! The idea was simple but really interesting."),
        Comment(username="Alice", book_id=books[0].id, stars=5, text="I loved the message of this book."),
        Comment(username="Tom", book_id=books[1].id, stars=5, text="Very useful and easy to understand."),
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
        "time": comment.created_at.strftime("%Y-%m-%d"),
    }


def build_rating_summary(book):
    all_stars = [rating.stars for rating in book.ratings]
    total = len(all_stars)
    if total == 0:
        return {"average": book.rating, "total": 0, "distribution": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}, "counts": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}}
    distribution = {}
    counts = {}
    for star in [5, 4, 3, 2, 1]:
        count = all_stars.count(star)
        counts[star] = count
        distribution[star] = round(count / total * 100)
    average = round(sum(all_stars) / total, 1)
    return {"average": average, "total": total, "distribution": distribution, "counts": counts}


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
        trending_books = Book.query.order_by(Book.rating.desc()).all()
        most_read_books = Book.query.order_by(Book.reads.desc()).all()
        comments = Comment.query.order_by(Comment.created_at.desc()).all()
        reviews = [format_review(comment) for comment in comments]
        return render_template("home.html", trending_books=trending_books, most_read_books=most_read_books, reviews=reviews)

    @app.route("/shelf/<int:item_id>/progress", methods=["POST"])
    def update_progress(item_id):
        item = ShelfItem.query.get_or_404(item_id)
        current_page = request.form.get("current_page", type=int)
        if current_page is None or current_page < 0:
            abort(400)
        if item.book.pages and current_page > item.book.pages:
            current_page = item.book.pages
        item.current_page = current_page
        if item.book.pages and current_page >= item.book.pages:
            item.status = "Read"
            item.current_page = item.book.pages
        else:
            item.status = "Currently Reading"
        db.session.commit()
        return redirect(url_for("currently_reading"))

    @app.route("/profile")
    @app.route("/profile.html")
    def profile():
        if current_user.is_authenticated:
            counts = get_shelf_counts_for_user(current_user.id) if 'get_shelf_counts_for_user' in globals() else get_shelf_counts(get_session_id())
        else:
            session_id = get_session_id()
            counts = get_shelf_counts(session_id)
        return render_template("profile.html", counts=counts)

    @app.route("/login", methods=["GET", "POST"])
    @app.route("/login.html", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        form = LoginForm()
        if form.validate_on_submit():
            identifier = form.username_or_email.data.strip()
            user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()
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
            user = User(username=form.username.data.strip(), email=form.email.data.strip().lower())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("profile"))
        return render_template("signup.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("home"))

    @app.route("/edit-profile", methods=["GET", "POST"])
    @app.route("/edit-profile.html", methods=["GET", "POST"])
    @login_required
    def edit_profile():
        form = EditProfileForm(original_username=current_user.username, original_email=current_user.email)
        if form.validate_on_submit():
            current_user.username = form.username.data.strip()
            current_user.email = form.email.data.strip().lower()
            current_user.bio = form.bio.data.strip() if form.bio.data else ""
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for("profile"))
        if request.method == "POST" and not form.validate():
            for field in form:
                for err in field.errors:
                    flash(f"{field.label.text}: {err}", "danger")
        elif request.method == "GET":
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.bio.data = current_user.bio or ""
        return render_template("edit-profile.html", form=form)

    @app.route("/read")
    @app.route("/read.html")
    def read():
        if current_user.is_authenticated:
            items = ShelfItem.query.filter_by(user_id=current_user.id, status="Read").all()
            shelf_rows = chunked(items, 6)
            counts = get_shelf_counts_for_user(current_user.id) if 'get_shelf_counts_for_user' in globals() else {}
        else:
            session_id = get_session_id()
            items = ShelfItem.query.filter_by(session_id=session_id, status="Read").all()
            shelf_rows = chunked(items, 6)
            counts = get_shelf_counts(session_id)
        return render_template("read.html", shelf_rows=shelf_rows, counts=counts)

    @app.route("/currently-reading")
    @app.route("/currently-reading.html")
    def currently_reading():
        if current_user.is_authenticated:
            items = ShelfItem.query.filter_by(user_id=current_user.id, status="Currently Reading").all()
            counts = get_shelf_counts_for_user(current_user.id) if 'get_shelf_counts_for_user' in globals() else {}
        else:
            session_id = get_session_id()
            items = ShelfItem.query.filter_by(session_id=session_id, status="Currently Reading").all()
            counts = get_shelf_counts(session_id)
        return render_template("currently-reading.html", items=items, counts=counts)

    @app.route("/to-be-read")
    @app.route("/to-be-read.html")
    def to_be_read():
        if current_user.is_authenticated:
            items = ShelfItem.query.filter_by(user_id=current_user.id, status="To Be Read").all()
            shelf_rows = chunked(items, 6)
            counts = get_shelf_counts_for_user(current_user.id) if 'get_shelf_counts_for_user' in globals() else {}
        else:
            session_id = get_session_id()
            items = ShelfItem.query.filter_by(session_id=session_id, status="To Be Read").all()
            shelf_rows = chunked(items, 6)
            counts = get_shelf_counts(session_id)
        return render_template("to-be-read.html", shelf_rows=shelf_rows, counts=counts)

    @app.route("/did-not-finish")
    @app.route("/did-not-finish.html")
    def did_not_finish():
        if current_user.is_authenticated:
            items = ShelfItem.query.filter_by(user_id=current_user.id, status="Did Not Finish").all()
            shelf_rows = chunked(items, 6)
            counts = get_shelf_counts_for_user(current_user.id) if 'get_shelf_counts_for_user' in globals() else {}
        else:
            session_id = get_session_id()
            items = ShelfItem.query.filter_by(session_id=session_id, status="Did Not Finish").all()
            shelf_rows = chunked(items, 6)
            counts = get_shelf_counts(session_id)
        return render_template("did-not-finish.html", shelf_rows=shelf_rows, counts=counts)

    @app.route("/my-reviews")
    @app.route("/my-reviews.html")
    def my_reviews():
        return render_template("my-reviews.html")

    @app.route("/book/<int:book_id>")
    def book_detail(book_id):
        book = Book.query.get_or_404(book_id)
        rating_summary = build_rating_summary(book)
        comments = Comment.query.filter_by(book_id=book_id).all()
        reviews = [format_review(c) for c in comments]
        user_rating = 0
        if current_user.is_authenticated:
            rating = Rating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        else:
            session_id = get_session_id()
            rating = Rating.query.filter_by(session_id=session_id, book_id=book_id).first()
        if rating:
            user_rating = rating.stars
        shelf_status = None
        if current_user.is_authenticated:
            shelf_item = ShelfItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        else:
            session_id = get_session_id()
            shelf_item = ShelfItem.query.filter_by(session_id=session_id, book_id=book_id).first()
        if shelf_item:
            shelf_status = shelf_item.status
        author = None
        return render_template("book_detail.html", book=book, author=author, rating_summary=rating_summary, reviews=reviews, user_rating=user_rating, shelf_status=shelf_status)

    @app.route("/book/<int:book_id>/shelf", methods=["POST"])
    def update_shelf_status(book_id):
        book = Book.query.get_or_404(book_id)
        status = request.form.get("status")
        allowed_status = ["Read", "Currently Reading", "To Be Read", "Did Not Finish", "remove"]
        if status not in allowed_status:
            abort(400)
        if current_user.is_authenticated:
            shelf_item = ShelfItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        else:
            session_id = get_session_id()
            shelf_item = ShelfItem.query.filter_by(session_id=session_id, book_id=book_id).first()
        if status == "remove":
            if shelf_item:
                db.session.delete(shelf_item)
        else:
            if shelf_item:
                shelf_item.status = status
            else:
                if current_user.is_authenticated:
                    shelf_item = ShelfItem(user_id=current_user.id, book_id=book_id, status=status)
                else:
                    shelf_item = ShelfItem(session_id=session_id, book_id=book_id, status=status)
                db.session.add(shelf_item)
        db.session.commit()
        return redirect(url_for("book_detail", book_id=book_id))

    @app.route("/book/<int:book_id>/rate", methods=["POST"])
    def rate_book(book_id):
        book = Book.query.get_or_404(book_id)
        stars = request.form.get("stars", type=int)
        if stars is None or stars < 0 or stars > 5:
            abort(400)
        if current_user.is_authenticated:
            existing_rating = Rating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
            if existing_rating:
                if stars == 0:
                    db.session.delete(existing_rating)
                else:
                    existing_rating.stars = stars
            elif stars > 0:
                rating = Rating(user_id=current_user.id, book_id=book_id, stars=stars, username=current_user.username)
                db.session.add(rating)
        else:
            session_id = get_session_id()
            existing_rating = Rating.query.filter_by(session_id=session_id, book_id=book_id).first()
            if existing_rating:
                if stars == 0:
                    db.session.delete(existing_rating)
                else:
                    existing_rating.stars = stars
            elif stars > 0:
                rating = Rating(session_id=session_id, book_id=book_id, stars=stars)
                db.session.add(rating)
        db.session.commit()
        return redirect(url_for("book_detail", book_id=book_id))

    @app.route("/book/<int:book_id>/review", methods=["POST"])
    def post_review(book_id):
        book = Book.query.get_or_404(book_id)
        text = request.form.get("text", "").strip()
        stars = request.form.get("stars", type=int)
        if not text:
            abort(400)
        if stars is None or stars < 1 or stars > 5:
            abort(400)
        if current_user.is_authenticated:
            existing_rating = Rating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
            if existing_rating:
                existing_rating.stars = stars
            else:
                rating = Rating(user_id=current_user.id, book_id=book_id, stars=stars, username=current_user.username)
                db.session.add(rating)
            comment = Comment(user_id=current_user.id, username=current_user.username, book_id=book_id, text=text, stars=stars)
        else:
            session_id = get_session_id()
            existing_rating = Rating.query.filter_by(session_id=session_id, book_id=book_id).first()
            if existing_rating:
                existing_rating.stars = stars
            else:
                rating = Rating(session_id=session_id, book_id=book_id, stars=stars)
                db.session.add(rating)
            comment = Comment(session_id=session_id, username="Anonymous", book_id=book_id, text=text, stars=stars)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("book_detail", book_id=book_id))

    @app.route("/search")
    def search():
        query = request.args.get("q", "").strip()
        books = []
        empty_query = False
        if query:
            books = Book.query.filter(or_(Book.title.ilike(f"%{query}%"), Book.author.ilike(f"%{query}%"))).all()
        else:
            empty_query = True
        return render_template("search-result.html", query=query, books=books, empty_query=empty_query)

    @app.route("/search-suggestions")
    def search_suggestions():
        query = request.args.get("q", "").strip()
        if not query:
            return jsonify([])
        books = Book.query.filter(or_(Book.title.ilike(f"%{query}%"), Book.author.ilike(f"%{query}%"))).limit(5).all()
        suggestions = [{"id": b.id, "title": b.title, "author": b.author} for b in books]
        return jsonify(suggestions)
