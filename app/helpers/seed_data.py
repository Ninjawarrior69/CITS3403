from app.extensions import db
from app.models import Book, Comment


STARTER_BOOKS = [
    {
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "description": "A novel about choices, regrets, and the different lives a person could have lived.",
        "page_count": 304,
        "cover_url": "https://m.media-amazon.com/images/I/71qsovx-x6L._AC_UF1000,1000_QL80_.jpg",
        "rating": 0,
        "reads": 0,
    },
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "description": "A science fiction story about survival, problem solving, and saving humanity.",
        "page_count": 496,
        "cover_url": "https://m.media-amazon.com/images/I/91ENQs2KLAL._AC_UF1000,1000_QL80_.jpg",
        "rating": 4.5,
        "reads": 1680,
    },
    {
        "title": "Normal People",
        "author": "Sally Rooney",
        "description": "A story about friendship, love, communication, and growing up.",
        "page_count": 288,
        "cover_url": "https://m.media-amazon.com/images/I/61nFGO425OL.jpg",
        "rating": 4.0,
        "reads": 980,
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "description": "A classic science fiction novel about politics, power, religion, and survival on a desert planet.",
        "page_count": 489,
        "cover_url": "https://m.media-amazon.com/images/I/71oO1E-XPuL.jpg",
        "rating": 4.4,
        "reads": 1900,
    },
    {
        "title": "Before the Coffee Gets Cold",
        "author": "Toshikazu Kawaguchi",
        "description": "A gentle story about time travel, memory, regret, and human connection.",
        "page_count": 208,
        "cover_url": "https://m.media-amazon.com/images/I/71kW0ESYl5L.jpg",
        "rating": 4.1,
        "reads": 870,
    },
    {
        "title": "Sunrise on the Reaping",
        "author": "Suzanne Collins",
        "description": "The newest book in The Hunger Games series.",
        "page_count": 400,
        "cover_url": "https://m.media-amazon.com/images/I/81RUJzM+wvL._UF894,1000_QL80_.jpg",
        "rating": 4.6,
        "reads": 2300,
    },
]


STARTER_COMMENTS = [
    {
        "book_title": "The Midnight Library",
        "username": "Reader1",
        "stars": 4,
        "text": "Great book! The idea was simple but really interesting.",
    },
    {
        "book_title": "The Midnight Library",
        "username": "Alice",
        "stars": 5,
        "text": "I loved the message of this book.",
    },
    {
        "book_title": "Project Hail Mary",
        "username": "Tom",
        "stars": 5,
        "text": "Very useful and easy to understand.",
    },
]


def seed_books_if_empty():
    if Book.query.first():
        return

    created_books = {}

    for book_data in STARTER_BOOKS:
        book = Book(**book_data)
        db.session.add(book)
        created_books[book.title] = book

    db.session.commit()

    comments = []

    for comment_data in STARTER_COMMENTS:
        book = created_books.get(comment_data["book_title"])

        if book:
            comments.append(
                Comment(
                    username=comment_data["username"],
                    book_id=book.id,
                    stars=comment_data["stars"],
                    text=comment_data["text"],
                )
            )

    db.session.add_all(comments)
    db.session.commit()