from sqlalchemy import or_

from app.models import Book, User


def normalise_search_type(search_type):
    search_type = (search_type or "books").strip().lower()

    if search_type not in ["books", "users"]:
        return "books"

    return search_type


def normalise_page(page_value):
    try:
        page = int(page_value)
    except (TypeError, ValueError):
        return 1

    return max(page, 1)


def search_users(query, limit=10):
    return (
        User.query.filter(
            or_(
                User.username.ilike(f"%{query}%"),
                User.name.ilike(f"%{query}%"),
            )
        )
        .order_by(User.username.asc())
        .limit(limit)
        .all()
    )


def user_to_suggestion(user):
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name or user.username,
        "avatar": user.avatar,
        "type": "user",
    }


def book_to_suggestion(book):
    return {
        "id": book.id,
        "openlibrary_id": getattr(book, "openlibrary_id", None),
        "title": book.title,
        "author": book.author,
        "cover_url": book.cover_url,
        "type": "book",
        "source": "local",
    }


def open_library_book_to_suggestion(book):
    if isinstance(book, dict):
        title = book.get("title", "")
        author = book.get("author", "")
        cover_url = book.get("cover_url", "")
        openlibrary_id = book.get("openlibrary_id")
    else:
        title = getattr(book, "title", "")
        author = getattr(book, "author", "")
        cover_url = getattr(book, "cover_url", "")
        openlibrary_id = getattr(book, "openlibrary_id", None)

    if not title:
        return None

    return {
        "id": None,
        "openlibrary_id": openlibrary_id,
        "title": title,
        "author": author or "Unknown author",
        "cover_url": cover_url,
        "type": "book",
        "source": "open_library",
    }


def get_book_key(title, author):
    return (
        (title or "").strip().lower(),
        (author or "").strip().lower(),
    )

def search_books(query, open_library_search_func=None, page=1, limit=10):
    if not query:
        return []

    results = []
    seen_books = set()

    local_books = (
        Book.query.filter(
            or_(
                Book.title.ilike(f"%{query}%"),
                Book.author.ilike(f"%{query}%"),
            )
        )
        .order_by(Book.title.asc())
        .limit(limit)
        .all()
    )

    for book in local_books:
        book_key = get_book_key(book.title, book.author)

        if book_key in seen_books:
            continue

        seen_books.add(book_key)

        results.append({
            "source": "local",
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "cover_url": book.cover_url,
            "openlibrary_id": book.openlibrary_id,
            "edition_key": None,
            "publish_year": book.publish_year,
        })

    if len(results) >= limit or open_library_search_func is None:
        return results

    try:
        open_library_books = open_library_search_func(
            query,
            page=page,
            limit=limit - len(results)
        )
    except Exception as error:
        print("Open Library search error:", error)
        open_library_books = []

    for book in open_library_books:
        if len(results) >= limit:
            break

        title = book.get("title")
        author = book.get("author")
        book_key = get_book_key(title, author)

        if book_key in seen_books:
            continue

        seen_books.add(book_key)

        book["source"] = "open_library"
        book["id"] = None
        results.append(book)

    return results

def search_book_suggestions(query, open_library_search_func=None, limit=5):
    suggestions = []
    seen_books = set()

    local_books = (
        Book.query.filter(
            or_(
                Book.title.ilike(f"%{query}%"),
                Book.author.ilike(f"%{query}%"),
            )
        )
        .order_by(Book.title.asc())
        .limit(limit)
        .all()
    )

    for book in local_books:
        book_key = get_book_key(book.title, book.author)

        if book_key in seen_books:
            continue

        seen_books.add(book_key)
        suggestions.append(book_to_suggestion(book))

    if len(suggestions) >= limit or open_library_search_func is None:
        return suggestions

    try:
        open_library_books = open_library_search_func(query, page=1)
    except Exception as error:
        print("Open Library suggestion error:", error)
        open_library_books = []

    for book in open_library_books:
        if len(suggestions) >= limit:
            break

        suggestion = open_library_book_to_suggestion(book)

        if not suggestion:
            continue

        book_key = get_book_key(suggestion["title"], suggestion["author"])

        if book_key in seen_books:
            continue

        seen_books.add(book_key)
        suggestions.append(suggestion)

    return suggestions
