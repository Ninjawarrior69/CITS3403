from uuid import uuid4

from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_login import current_user

from app.extensions import db
from app.models import Book, Comment, Rating, ShelfItem


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

    total = len(all_stars)

    if total == 0:
        return {
            "average": book.rating,
            "total": 0,
            "distribution": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0},
            "counts": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
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
        "counts": counts
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
		
		# Get all books, sorted by rating (trending)
		trending_books = Book.query.order_by(Book.rating.desc()).all()
		
		# Get most read books
		most_read_books = Book.query.order_by(Book.reads.desc()).all()
		
		# Get recent reviews
		comments = Comment.query.order_by(Comment.created_at.desc()).all()
		reviews = [format_review(comment) for comment in comments]
		
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
	
	@app.route("/book/<int:book_id>")
	def book_detail(book_id):
		book = Book.query.get_or_404(book_id)
		
		# Build rating summary
		rating_summary = build_rating_summary(book)
		
		# Get all reviews for this book
		comments = Comment.query.filter_by(book_id=book_id).all()
		reviews = [format_review(comment) for comment in comments]
		
		# Get current user's rating
		user_rating = 0
		if current_user.is_authenticated:
			rating = Rating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
		else:
			session_id = get_session_id()
			rating = Rating.query.filter_by(session_id=session_id, book_id=book_id).first()

		if rating:
			user_rating = rating.stars
		
		# Check current shelf status
		shelf_status = None

		if current_user.is_authenticated:
			shelf_item = ShelfItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
		else:
			session_id = get_session_id()
			shelf_item = ShelfItem.query.filter_by(session_id=session_id, book_id=book_id).first()
		
		if shelf_item:
			shelf_status = shelf_item.status
		
		author = None
		
		return render_template(
			"book_detail.html",
			book=book,
			author=author,
			rating_summary=rating_summary,
			reviews=reviews,
			user_rating=user_rating,
			shelf_status=shelf_status,
		)
	
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
					shelf_item= ShelfItem(
						user_id=current_user.id, 
						book_id=book_id, 
						status=status
					)
				else:
					shelf_item = ShelfItem(
						session_id=session_id, 
						book_id=book_id,
						status=status
					)
				
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
				rating -Rating(user_id=current_user.id, book_id=book_id, stars=stars, username=current_user.username)
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

			existing_rating = Rating.query.filter_by(
				user_id=current_user.id,
				book_id=book_id
			).first()

			if existing_rating:
				existing_rating.stars = stars
			else:
				rating = Rating(
					user_id=current_user.id,
					book_id=book_id,
					stars=stars,
					username=current_user.username
				)
				db.session.add(rating)

			comment = Comment(
				user_id=current_user.id,
				username=current_user.username,
				book_id=book_id,
				text=text,
				stars=stars
			)
		else:
			session_id = get_session_id()
			
			existing_rating = Rating.query.filter_by(
				session_id=session_id,
				book_id=book_id
			).first()

			if existing_rating:
				existing_rating.stars = stars
			else:
				rating =Rating(
					session_id=session_id,
					book_id=book_id,
					stars=stars
				)
				db.session.add(rating)

			comment = Comment(
				session_id=session_id,
				username="Anonymous",
				book_id=book_id,
				text=text,
				stars=stars
			)
		
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for("book_detail", book_id=book_id))
