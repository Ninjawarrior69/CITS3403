from flask import Flask, render_template


def register_routes(app: Flask) -> None:

    @app.route("/")
    def home():
        trending_books = [
            {"id": 1, "title": "Book A", "author": "Author A"},
            {"id": 2, "title": "Book B", "author": "Author B"}
        ]

        most_read_books = [
            {
                "id": 1,
                "title": "Book A",
                "author": "Author A",
                "rating": 4.5,
                "reads": 100,
                "comments": 20
            }
        ]

        reviews = [
            {
                "username": "Reader1",
                "book_id": 1,
                "book_title": "Book A",
                "stars": 4,
                "text": "Great book!",
                "time": "2 hours ago"
            }
        ]

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

        book = {
            "id": book_id,
            "title": f"Book {book_id}",
            "author": "Matt Haig",
            "description": "This is a sample description.",
            "rating": 4.2
        }

        authors = {
            "Matt Haig": {
                "bio": "Matt Haig is a British author and journalist. He has written both fiction and non-fiction books, often exploring themes of mental health and philosophy.",
                "followers": 45200,
                "books": 18
            }
        }

        author = authors.get(book["author"], {})

        rating_summary = {
            "average": 4.2,
            "total": 1247,
            "distribution": {
                5: 55,
                4: 30,
                3: 11,
                2: 3,
                1: 1
            }
        }

        reviews = [
            {
                "username": "Reader",
                "stars": 4,
                "text": "Great book!",
                "time": "2 hours ago"
            },
            {
                "username": "Alice",
                "stars": 5,
                "text": "Loved it!",
                "time": "1 day ago"
            }
        ]

        return render_template(
            "book_detail.html",
            book=book,
            author=author,
            reviews=reviews,
            rating_summary=rating_summary
        )