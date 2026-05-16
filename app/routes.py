from uuid import uuid4
from itertools import islice

from flask import Flask, render_template, abort, request, redirect, url_for, session, flash, jsonify
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_
import requests

from app.forms import LoginForm, SignupForm, EditProfileForm
from app.extensions import db
from app.models import Book, Comment, Rating, User, ShelfItem

from app.helpers.openlibrary_helpers import (
    search_open_library,
    fetch_openlibrary_description,
    fetch_page_count,
    normalize_openlibrary_id,
)
from app.helpers.profile_helpers import (
    save_avatar,
    get_profile_data,
    get_public_profile_data,
    update_profile
)
from app.helpers.search_helpers import (
    normalise_page,
    normalise_search_type,
    search_books,
    search_book_suggestions,
    search_users,
    user_to_suggestion,
)
from app.helpers.review_helpers import create_or_update_review
from app.helpers.seed_data import seed_books_if_empty
from app.helpers.validation_helpers import (
    is_valid_shelf_status,
    is_valid_rating,
    is_valid_review_text,
)

# Used for creating My Books shelves
def chunked(iterable, size):
    iterator = iter(iterable)
    return iter(lambda: list(islice(iterator, size)), [])

# Session ID
def get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid4())
    return session["session_id"]

# Shelf counts to display on profile
def get_user_shelf_counts(user_id):
    return {
        "read": ShelfItem.query.filter_by(user_id=user_id, status="Read").count(),
        "currently_reading": ShelfItem.query.filter_by(user_id=user_id, status="Currently Reading").count(),
        "to_be_read": ShelfItem.query.filter_by(user_id=user_id, status="To Be Read").count(),
        "did_not_finish": ShelfItem.query.filter_by(user_id=user_id, status="Did Not Finish").count()
    }


def format_review(comment):
    review_user = comment.user

    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "session_id": comment.session_id,
        "username": review_user.username if review_user else comment.username,
        "profile_username": review_user.username if review_user else None,
        "avatar": review_user.avatar if review_user else None,
        "book_id": comment.book_id,
        "book_title": comment.book.title,
        "author": comment.book.author,
        "cover_url": comment.book.cover_url,
        "stars": comment.stars,
        "text": comment.text,
        "time": comment.created_at.strftime("%Y-%m-%d"),
    }

# Rating summary
def build_rating_summary(book):
    all_stars = [rating.stars for rating in book.ratings]
    total = len(all_stars)

    if total == 0:
        return {
            "average": book.rating,
            "total": 0,
            "distribution": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0},
            "counts": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0},
        }

    distribution = {}
    counts = {}
    for star in [5, 4, 3, 2, 1]:
        count = all_stars.count(star)
        counts[star] = count
        distribution[star] = round(count / total * 100)

    average = round(sum(all_stars) / total, 1)
    return {
        "average": average,
        "total": total,
        "distribution": distribution,
        "counts": counts,
    }

# Display rating
def get_display_rating(book):
    rating_summary = build_rating_summary(book)
    return rating_summary["average"]


def register_routes(app: Flask) -> None:

    # Define routes which do not require login
    PUBLIC_ROUTES = {
        "home",
        "login",
        "signup",
        "search",
        "search_suggestions",
        "book_detail",
        "import_book",
        "static"
    }

    @app.before_request
    def require_login():
        if request.endpoint in PUBLIC_ROUTES:
            return
        
        if not current_user.is_authenticated:
            return redirect(url_for("login"))

    # Home
    @app.route("/")
    def home():
        seed_books_if_empty()
        trending_books = Book.query.order_by(Book.rating.desc()).all()
        most_read_books = Book.query.order_by(Book.reads.desc()).all()
        comments = Comment.query.order_by(Comment.created_at.desc()).all()
        reviews = [format_review(comment) for comment in comments]
        return render_template("home.html", trending_books=trending_books, most_read_books=most_read_books, reviews=reviews)

    # Current user profile
    @app.route("/profile")
    def profile():
        profile_data = get_profile_data(get_user_shelf_counts)

        profile_data["followers_count"] = current_user.followers.count()
        profile_data["following_count"] = current_user.following.count()
        profile_data["is_own_profile"] = True

        return render_template("profile.html", **profile_data)
    
    # View other users profiles
    @app.route("/user/<username>")
    def public_profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        profile_data = get_public_profile_data(
            user,
            get_user_shelf_counts
        )

        profile_data["followers_count"] = user.followers.count()
        profile_data["following_count"] = user.following.count()
        return render_template("profile.html", **profile_data)  

    # Login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        form = LoginForm()
        if form.validate_on_submit():
            identifier = form.username_or_email.data.strip().lower()
            user = User.query.filter(
                or_(
                    User.username == identifier,
                    User.email == identifier,
                )
            ).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("profile"))

            form.password.errors.append("Invalid username/email or password.")

        return render_template("login.html", form=form)

    # Sign Up
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("profile"))

        form = SignupForm()
        if form.validate_on_submit():
            user = User(
                name=form.username.data.strip().lower(),
                username=form.username.data.strip().lower(),
                email=form.email.data.strip().lower(),
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("profile"))

        return render_template("signup.html", form=form)

    # Logout
    @app.route("/logout")
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("home"))

    @app.route("/edit-profile", methods=["GET", "POST"])
    def edit_profile():
        if request.method == "POST":
            avatar_file = request.files.get("avatar")

            update_profile(request, avatar_file)

            return redirect(url_for("profile"))

        profile_data = get_profile_data(get_user_shelf_counts)

        return render_template("edit-profile.html", **profile_data)

    # My Books - Read
    @app.route("/my-books/read")
    def read():
        items = ShelfItem.query.filter_by(user_id=current_user.id, status="Read").all()
        counts = get_user_shelf_counts(current_user.id)

        shelf_rows = chunked(items, 6)
        return render_template("read.html", shelf_rows=shelf_rows, counts=counts, is_public_shelf=False)

    # My Books - Currently Reading
    @app.route("/my-books/currently-reading")
    def currently_reading():
        items = ShelfItem.query.filter_by(user_id=current_user.id, status="Currently Reading").all()
        counts = get_user_shelf_counts(current_user.id)

        return render_template("currently-reading.html", items=items, counts=counts, is_public_shelf=False)

    # My Books - To Be Read
    @app.route("/my-books/to-be-read")
    def to_be_read():
        items = ShelfItem.query.filter_by(user_id=current_user.id, status="To Be Read").all()
        counts = get_user_shelf_counts(current_user.id)

        shelf_rows = chunked(items, 6)
        return render_template("to-be-read.html", shelf_rows=shelf_rows, counts=counts, is_public_shelf=False)

    # My Books - Did Not Finish
    @app.route("/my-books/did-not-finish")
    def did_not_finish():
        items = ShelfItem.query.filter_by(user_id=current_user.id, status="Did Not Finish").all()
        counts = get_user_shelf_counts(current_user.id)

        shelf_rows = chunked(items, 6)
        return render_template("did-not-finish.html", shelf_rows=shelf_rows, counts=counts, is_public_shelf=False)
    
    # Other users - Read
    @app.route("/user/<username>/read")
    def public_user_read(username):
        user = User.query.filter_by(username=username).first_or_404()
        items = ShelfItem.query.filter_by(user_id=user.id, status="Read").all()
        counts = get_user_shelf_counts(user.id)
        shelf_rows = chunked(items, 6)

        return render_template(
           "read.html",
            shelf_rows=shelf_rows,
            counts=counts,
            profile_user=user,
            is_public_shelf=True,
            shelf_owner_name=user.name or user.username
        )
    
    # Other users - Currently Reading
    @app.route("/user/<username>/currently-reading")
    def public_user_currently_reading(username):
        user = User.query.filter_by(username=username).first_or_404()
        items = ShelfItem.query.filter_by(user_id=user.id, status="Currently Reading").all()
        counts = get_user_shelf_counts(user.id)

        return render_template(
            "currently-reading.html",
            items=items,
            counts=counts,
            profile_user=user,
            is_public_shelf=True,
            shelf_owner_name=user.name or user.username
        )
    
    # Other users - To Be Read
    @app.route("/user/<username>/to-be-read")
    def public_user_to_be_read(username):
        user = User.query.filter_by(username=username).first_or_404()
        items = ShelfItem.query.filter_by(user_id=user.id, status="To Be Read").all()
        counts = get_user_shelf_counts(user.id)
        shelf_rows = chunked(items, 6)

        return render_template(
            "to-be-read.html",
            shelf_rows=shelf_rows,
            counts=counts,
            profile_user=user,
            is_public_shelf=True,
            shelf_owner_name=user.name or user.username
        )
    
    # Other users - Did Not Finish
    @app.route("/user/<username>/did-not-finish")
    def public_user_did_not_finish(username):
        user = User.query.filter_by(username=username).first_or_404()
        items = ShelfItem.query.filter_by(user_id=user.id, status="Did Not Finish").all()
        counts = get_user_shelf_counts(user.id)
        shelf_rows = chunked(items, 6)

        return render_template(
            "did-not-finish.html",
            shelf_rows=shelf_rows,
            counts=counts,
            profile_user=user,
            is_public_shelf=True,
            shelf_owner_name=user.name or user.username
        )

    # My Reviews
    @app.route("/my-reviews")
    def my_reviews():
        comments = Comment.query.filter_by(
            user_id=current_user.id
        ).order_by(Comment.created_at.desc()).all()

        reviews = [format_review(comment) for comment in comments]
        return render_template("my-reviews.html", reviews=reviews)
    
    @app.route("/user/<username>/reviews")
    def public_user_reviews(username):
        user = User.query.filter_by(username=username).first_or_404()
        comments = Comment.query.filter_by(user_id=user.id).order_by(Comment.created_at.desc()).all()
        reviews = [format_review(comment) for comment in comments]

        return render_template(
            "my-reviews.html",
            reviews=reviews,
            profile_user=user,
            is_public_review=True,
            review_owner_name=user.name or user.username
        )

    # Update Currently Reading progress
    @app.route("/shelf/<int:item_id>/progress", methods=["POST"])
    def update_progress(item_id):
        item = ShelfItem.query.get_or_404(item_id)

        if item.user_id != current_user.id:
            abort(403)
            
        current_page = request.form.get("current_page", type=int)

        if current_page is None or current_page < 0:
            abort(400)

        if item.book.page_count and current_page > item.book.page_count:
            current_page = item.book.page_count

        item.current_page = current_page
        if item.book.page_count and current_page >= item.book.page_count:
            item.status = "Read"
            item.current_page = item.book.page_count
        else:
            item.status = "Currently Reading"

        db.session.commit()
        return redirect(url_for("currently_reading"))

    # Book detail
    @app.route("/book/<int:book_id>")
    def book_detail(book_id):
        book = Book.query.get_or_404(book_id)

        viewed_books = set(str(id) for id in session.get("viewed_books", []))
        book_key = str(book_id)

        if book_key not in viewed_books:
            book.reads = (book.reads or 0) + 1

            viewed_books.add(book_key)
            session["viewed_books"] = list(viewed_books)
            session.modified = True

            db.session.commit()

        rating_summary = build_rating_summary(book)
        comments = Comment.query.filter_by(book_id=book_id).order_by(Comment.created_at.desc()).all()
        reviews = [format_review(comment) for comment in comments]

        user_rating = 0
        my_review = None

        if current_user.is_authenticated:
            rating = Rating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
            shelf_item = ShelfItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
            my_review = Comment.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        else:
            session_id = get_session_id()
            rating = Rating.query.filter_by(session_id=session_id, book_id=book_id).first()
            shelf_item = ShelfItem.query.filter_by(session_id=session_id, book_id=book_id).first()
            my_review = Comment.query.filter_by(session_id=session_id, book_id=book_id).first()

        if rating:
            user_rating = rating.stars

        shelf_status = shelf_item.status if shelf_item else None
        author = None

        return render_template(
            "book_detail.html",
            book=book,
            author=author,
            rating_summary=rating_summary,
            reviews=reviews,
            user_rating=user_rating,
            shelf_status=shelf_status,
            my_review=my_review,
        )

    # Book Detail - Add to Shelf status
    @app.route("/book/<int:book_id>/shelf", methods=["POST"])
    def update_shelf_status(book_id):
        Book.query.get_or_404(book_id)
        status = request.form.get("status")

        if not is_valid_shelf_status(status):
            abort(400)

        shelf_item = ShelfItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()

        if status == "remove":
            if shelf_item:
                db.session.delete(shelf_item)
        else:
            if shelf_item:
                shelf_item.status = status
            else:
                shelf_item = ShelfItem(user_id=current_user.id, book_id=book_id, status=status)
                db.session.add(shelf_item)

        db.session.commit()
        return redirect(url_for("book_detail", book_id=book_id))

    # Book Detail - Rate book
    @app.route("/book/<int:book_id>/rate", methods=["POST"])
    def rate_book(book_id):
        book = Book.query.get_or_404(book_id)
        stars = request.form.get("stars", type=int)

        if not is_valid_rating(stars, allow_zero=True):
            abort(400)

        existing_rating = Rating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if existing_rating:
            if stars == 0:
                db.session.delete(existing_rating)
            else:
                existing_rating.stars = stars
        elif stars > 0:
            rating = Rating(user_id=current_user.id, book_id=book_id, stars=stars, username=current_user.username)
            db.session.add(rating)

        db.session.commit()

        rating_summary = build_rating_summary(book)
        book.rating = rating_summary["average"]

        db.session.commit()

        return redirect(url_for("book_detail", book_id=book_id))

    # Book Detail - Post review for book
    @app.route("/book/<int:book_id>/review", methods=["POST"])
    def post_review(book_id):
        book = Book.query.get_or_404(book_id)

        text = request.form.get("text", "").strip()
        stars = request.form.get("stars", type=int)

        if not is_valid_review_text(text):
            abort(400)

        if not is_valid_rating(stars):
            abort(400)

        create_or_update_review(book_id=book_id, stars=stars, text=text, user=current_user)

        db.session.flush()

        rating_summary = build_rating_summary(book)
        book.rating = rating_summary["average"]

        db.session.commit()

        next_page = request.form.get("next")
        if next_page:
            return redirect(next_page)

        return redirect(url_for("book_detail", book_id=book_id))
    
    # Book Detail - Delete review
    @app.route("/review/<int:review_id>/delete", methods=["POST"])
    def delete_review(review_id):
        comment = Comment.query.get_or_404(review_id)
        if comment.user_id != current_user.id:
            abort(403)

        book_id = comment.book_id
        book = Book.query.get_or_404(book_id)

        db.session.delete(comment)
        db.session.flush()

        rating_summary = build_rating_summary(book)
        book.rating = rating_summary["average"]

        db.session.commit()

        next_page = request.form.get("next")
        if next_page:
            return redirect(next_page)

        return redirect(url_for("book_detail", book_id=book_id))

    # Search
    @app.route("/search")
    def search():
        query = request.args.get("q", "").strip()
        search_type = normalise_search_type(request.args.get("type", "books"))
        page = normalise_page(request.args.get("page", 1))

        books = []
        users = []
        empty_query = not bool(query)

        if query:
            if search_type == "users":
                users = search_users(query, limit=10)
            else:
                books = search_books(
                   query,
                   open_library_search_func=search_open_library,
                   page=page,
                   limit=10
                )

        return render_template(
            "search-result.html",
            page=page,
            query=query,
            books=books,
            users=users,
            search_type=search_type,
            empty_query=empty_query
        )

    # Search Suggestions
    @app.route("/search-suggestions")
    def search_suggestions():
        query = request.args.get("q", "").strip()
        search_type = normalise_search_type(request.args.get("type", "books"))

        if not query:
            return jsonify([])

        if search_type == "users":
            users = search_users(query, limit=5)
            suggestions = [user_to_suggestion(user) for user in users]

            return jsonify(suggestions)
        
        suggestions = search_book_suggestions(
            query,
            open_library_search_func=search_open_library,
            limit=5,
        )

        return jsonify(suggestions)

    # Import book from Open Library API
    @app.route("/import-book")
    def import_book():
        openlibrary_id = normalize_openlibrary_id(request.args.get("olid"))
        title = request.args.get("title")
        author = request.args.get("author")
        cover_url = request.args.get("cover")
        publish_year = request.args.get("first_publish_year", type=int)
        if publish_year is None:
            publish_year = request.args.get("publish_year", type=int)
        edition_key = request.args.get("edition_key")

        if not title or not author:
            return redirect(url_for("search"))

        if openlibrary_id is not None:
            existing_book = Book.query.filter_by(
                openlibrary_id=openlibrary_id
            ).first()
        else:
            existing_book = Book.query.filter_by(
                title=title,
                author=author
            ).first()

        if existing_book:
            return redirect(
                url_for("book_detail", book_id=existing_book.id)
            )

        description = fetch_openlibrary_description(openlibrary_id)
        page_count = fetch_page_count(openlibrary_id, edition_key)

        new_book = Book(
            openlibrary_id=openlibrary_id,
            title=title,
            author=author,
            cover_url=cover_url,
            page_count=page_count,
            publish_year=publish_year,
            description=description
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect(
            url_for("book_detail", book_id=new_book.id)
        )
    
    # Get a users follower list
    @app.route("/user/<username>/followers")
    def get_followers(username):
        user = User.query.filter_by(username=username).first_or_404()

        followers = [
            {
                "username": follower.username,
                "avatar": follower.avatar
            }
            for follower in user.followers.all()
        ]

        return jsonify(followers)
    
    # Get a users following list
    @app.route("/user/<username>/following")
    def get_following(username):
        user = User.query.filter_by(username=username).first_or_404()

        following = [
            {
                "username": followed.username,
                "avatar": followed.avatar
            }
            for followed in user.following.all()
        ]

        return jsonify(following)
    
    # Follow other users
    @app.route("/follow/<int:user_id>", methods=["POST"])
    def follow(user_id):
        user = User.query.get_or_404(user_id)

        if user == current_user:
            return "", 400

        if not current_user.following.filter_by(id=user.id).first():
            current_user.following.append(user)
            db.session.commit()

        return jsonify({"status": "followed"})
    
    # Unfollow users
    @app.route("/unfollow/<int:user_id>", methods=["POST"])
    def unfollow(user_id):
        user = User.query.get_or_404(user_id)

        if current_user.following.filter_by(id=user.id).first():
            current_user.following.remove(user)
            db.session.commit()

        return jsonify({"status": "unfollowed"})