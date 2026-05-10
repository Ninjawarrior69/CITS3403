from uuid import uuid4
from itertools import islice

from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import or_
from flask import jsonify

from app.extensions import db
from app.models import Book, Comment, Rating, ShelfItem
import requests

from app.helpers.profile_helpers import (
    save_avatar,
    get_profile_data,
	update_authenticated_profile,
	update_anonymous_profile
)

def chunked(iterable, size):
	it = iter(iterable)
	return iter(lambda: list(islice(it, size)),[])

def get_shelf_counts(session_id):
	return {
		"read": ShelfItem.query.filter_by(session_id=session_id, status="Read").count(),
		"currently_reading": ShelfItem.query.filter_by(session_id=session_id, status="Currently Reading").count(),
		"to_be_read": ShelfItem.query.filter_by(session_id=session_id, status="To Be Read").count(),
		"did_not_finish": ShelfItem.query.filter_by(session_id=session_id, status="Did Not Finish").count()
	}

def get_user_shelf_counts(user_id):

    return {
        "read": ShelfItem.query.filter_by(user_id=user_id, status="Read").count(),
        "currently_reading": ShelfItem.query.filter_by(user_id=user_id, status="Currently Reading").count(),
        "to_be_read": ShelfItem.query.filter_by(user_id=user_id, status="To Be Read").count(),
        "did_not_finish": ShelfItem.query.filter_by(user_id=user_id, status="Did Not Finish").count()
    }

def seed_books_if_empty():
    if Book.query.first():
        return

    books = [
        Book(
            title="The Midnight Library",
            author="Matt Haig",
            description="A novel about choices, regrets, and the different lives a person could have lived.",
			page_count=304,
			cover_url="https://m.media-amazon.com/images/I/71qsovx-x6L._AC_UF1000,1000_QL80_.jpg",
            rating=4.2,
            reads=1247
        ),
        Book(
            title="Atomic Habits",
            author="James Clear",
            description="A practical book about building good habits and breaking bad ones through small daily changes.",
			page_count=320,
			cover_url="https://m.media-amazon.com/images/I/81kg51XRc1L.jpg",
            rating=4.6,
            reads=2100
        ),
        Book(
            title="Project Hail Mary",
            author="Andy Weir",
            description="A science fiction story about survival, problem solving, and saving humanity.",
			page_count=496,
			cover_url="https://m.media-amazon.com/images/I/91ENQs2KLAL._AC_UF1000,1000_QL80_.jpg",
            rating=4.5,
            reads=1680
        ),
        Book(
            title="Normal People",
            author="Sally Rooney",
            description="A story about friendship, love, communication, and growing up.",
			page_count=288,
			cover_url="https://m.media-amazon.com/images/I/61nFGO425OL.jpg",
            rating=4.0,
            reads=980
        ),
        Book(
            title="Dune",
            author="Frank Herbert",
            description="A classic science fiction novel about politics, power, religion, and survival on a desert planet.",
			page_count=489,
			cover_url="https://m.media-amazon.com/images/I/71oO1E-XPuL.jpg",
            rating=4.4,
            reads=1900
        ),
        Book(
            title="Before the Coffee Gets Cold",
            author="Toshikazu Kawaguchi",
            description="A gentle story about time travel, memory, regret, and human connection.",
			page_count=208,
			cover_url="https://m.media-amazon.com/images/I/71kW0ESYl5L.jpg",
            rating=4.1,
            reads=870
        ),
		Book(
			title="Sunrise on the Reaping",
			author="Suzanne Collins",
			description="The newest book in The Hunger Games series",
			page_count=400,
			cover_url="https://m.media-amazon.com/images/I/81RUJzM+wvL._UF894,1000_QL80_.jpg",
			rating=4.6,
			reads=2300
		)
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
		"author": comment.book.author,
		"cover_url": comment.book.cover_url,
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

def search_open_library(query, page=1, limit=10):
	url = "https://openlibrary.org/search.json"

	params = {
		"q": query,
		"page": page,
		"limit": limit
	}

	response = requests.get(url, params=params)

	try:
		data = response.json()
	except requests.exceptions.JSONDecodeError:
		return []
	
	books = []

	for doc in data.get("docs", []):

		cover_id = doc.get("cover_i")
		edition_key = doc.get("edition_key", [])

		books.append({
			"title": doc.get("title", "Unknown Title"),
			"author": ", ".join(doc.get("author_name", ["Unknown"])),
			"cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None,
			"openlibrary_id": doc.get("key"),
			"edition_key": doc.get("edition_key", [None])[0] if doc.get("edition_key") else None,
			"publish_year": doc.get("first_publish_year")
		})
	return books


def fetch_openlibrary_description(olid):

    url = f"https://openlibrary.org{olid}.json"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()

    description = data.get("description")

    if isinstance(description, dict):
        return description.get("value")

    return description

def fetch_page_count(openlibrary_id, edition_key=None):
    if edition_key:
        url = f"https://openlibrary.org/books/{edition_key}.json"
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            if data.get("number_of_pages"):
                return data["number_of_pages"]

    if openlibrary_id:
        url = f"https://openlibrary.org{openlibrary_id}.json"
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()

            editions = data.get("covers")
            edition_keys = data.get("covers", [])

            if "latest_revision" in data:
                editions_url = f"https://openlibrary.org{openlibrary_id}/editions.json"
                r = requests.get(editions_url)

                if r.status_code == 200:
                    ed_data = r.json()
                    entries = ed_data.get("entries", [])

                    for e in entries:
                        if e.get("number_of_pages"):
                            return e["number_of_pages"]
    return None


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
	
	@app.route("/shelf/<int:item_id>/progress", methods=["POST"])
	def update_progress(item_id):
		item = ShelfItem.query.get_or_404(item_id)
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

	@app.route("/profile")
	@app.route("/profile.html")
	def profile():

		profile_data = get_profile_data(
			get_session_id,
			get_shelf_counts,
			get_user_shelf_counts
		)

		return render_template(
			"profile.html", 
			**profile_data
		)
      
	@app.route("/login")
	@app.route("/login.html")
	def login():
		return render_template("login.html")

	@app.route("/signup")
	@app.route("/signup.html")
	def signup():
		return render_template("signup.html")

	@app.route("/edit-profile", methods=["GET", "POST"])
	@app.route("/edit-profile.html", methods=["GET", "POST"])
	def edit_profile():

		if request.method == "POST":

			avatar_file = request.files.get("avatar")

			if current_user.is_authenticated:
				update_authenticated_profile(request, avatar_file)
			
			else:
				update_anonymous_profile(request, avatar_file)

			return redirect(url_for("profile"))
            
		profile_data = get_profile_data(
			get_session_id,
			get_shelf_counts,
			get_user_shelf_counts
		)
		
		return render_template(
			"edit-profile.html",
			**profile_data			
		)
	
	@app.route("/read")
	@app.route("/read.html")
	#@login_required
	def read():
		session_id = get_session_id() # for testing
		items = ShelfItem.query.filter_by(
			session_id = session_id, #user_id = current_user.id
			status = "Read"
		).all()
		shelf_rows = chunked(items,6)
		counts = get_shelf_counts(session_id)
		return render_template("read.html", shelf_rows=shelf_rows, counts=counts)
	
	@app.route("/currently-reading")
	@app.route("/currently-reading.html")
	#@login_required
	def currently_reading():
		session_id = get_session_id() # for testing
		items = ShelfItem.query.filter_by(
			session_id = session_id, #user_id = current_user.id
			status = "Currently Reading"
		).all()
		counts = get_shelf_counts(session_id)
		return render_template("currently-reading.html", items=items, counts=counts)
	
	@app.route("/to-be-read")
	@app.route("/to-be-read.html")
	#@login_required
	def to_be_read():
		session_id = get_session_id() # for testing
		items = ShelfItem.query.filter_by(
			session_id = session_id, #user_id = current_user.id
			status = "To Be Read"
		).all()
		shelf_rows = chunked(items,6)
		counts = get_shelf_counts(session_id)
		return render_template("to-be-read.html", shelf_rows=shelf_rows, counts=counts)
	
	@app.route("/did-not-finish")
	@app.route("/did-not-finish.html")
	#@login_required
	def did_not_finish():
		session_id = get_session_id() # for testing
		items = ShelfItem.query.filter_by(
			session_id = session_id, #user_id = current_user.id
			status = "Did Not Finish"
		).all()
		shelf_rows = chunked(items,6)
		counts = get_shelf_counts(session_id)
		return render_template("did-not-finish.html", shelf_rows=shelf_rows, counts=counts)
	
	@app.route("/my-reviews")
	@app.route("/my-reviews.html")
	#@login_required
	def my_reviews():

		if current_user.is_authenticated:
			comments = Comment.query.filter_by(
				user_id=current_user.id
			).order_by(Comment.created_at.desc()).all()

		else:
			session_id = get_session_id()

			comments = Comment.query.filter_by(
				session_id=session_id
			).order_by(Comment.created_at.desc()).all()

		reviews = [format_review(comment) for comment in comments]

		return render_template(
			"my-reviews.html",
			reviews=reviews
		)
	
	@app.route("/book/<int:book_id>")
	def book_detail(book_id):
		book = Book.query.get_or_404(book_id)

		viewed_books = session.get("viewed_books", [])

		if book_id not in viewed_books:
			book.reads += 1
			db.session.commit()

			viewed_books.append(book_id)
			session["viewed_books"] = viewed_books
		
		# Build rating summary
		rating_summary = build_rating_summary(book)
		
		# Get all reviews for this book
		comments = (
			Comment.query
			.filter_by(book_id=book_id)
			.order_by(Comment.created_at.desc())
			.all()
		)
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

		rating_summary = build_rating_summary(book)
		book.rating = rating_summary["average"]

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
					username=session.get("profile_username", "Anonymous"),
					book_id=book_id,
					stars=stars
				)
				db.session.add(rating)

			comment = Comment(
				session_id=session_id,
				username=session.get("profile_username", "Anonymous"),
				book_id=book_id,
				text=text,
				stars=stars
			)
		
		db.session.add(comment)
		db.session.commit()

		rating_summary = build_rating_summary(book)
		book.rating = rating_summary["average"]

		db.session.commit()
		
		return redirect(url_for("book_detail", book_id=book_id))
	
	@app.route("/search")
	def search():
		query = request.args.get("q", "").strip()

		try:
			page = int(request.args.get("page", 1))
		except ValueError:
			page = 1

		books = []
		empty_query = False

		if query:
			books = search_open_library(query, page=page)
		else:
			empty_query = True
		
		return render_template(
			"search-result.html",
			page=page,
			query=query,
			books=books,
			empty_query=empty_query
		)
	
	@app.route("/search-suggestions")
	def search_suggestions():
		query = request.args.get("q", "").strip()

		if not query:
			return jsonify([])
		
		books = Book.query.filter(
			or_(
				Book.title.ilike(f"%{query}%"),
				Book.author.ilike(f"%{query}%")
			)
		).limit(5).all()

		suggestions = []

		for book in books:
			suggestions.append({
				"id": book.id,
				"title": book.title,
				"author": book.author,
				"cover_url": book.cover_url
			})
		
		return jsonify(suggestions)
	
	@app.route("/import-book")
	def import_book():
		
		openlibrary_id = request.args.get("olid")
		title = request.args.get("title")
		author = request.args.get("author")
		cover_url = request.args.get("cover")
		publish_year = request.args.get("first_publish_year", type=int)
		edition_key = request.args.get("edition_key")
		description = fetch_openlibrary_description(openlibrary_id)

		page_count = fetch_page_count(openlibrary_id, edition_key)

		existing_book = Book.query.filter_by(
			openlibrary_id=openlibrary_id
		).first()

		if not title or not author:
			return redirect(url_for("search"))

		if existing_book:
			return redirect(
				url_for("book_detail", book_id=existing_book.id)
			)
		
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
