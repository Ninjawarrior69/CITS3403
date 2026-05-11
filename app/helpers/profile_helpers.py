import os

from flask import session
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.models import Book, Comment


def save_avatar(avatar_file):

    filename = secure_filename(
        avatar_file.filename
    )

    avatar_path = os.path.join(
        "app",
        "static",
        "uploads",
        "avatars",
        filename
    )

    avatar_file.save(avatar_path)

    return f"uploads/avatars/{filename}"


def get_profile_data(
    get_session_id,
    get_shelf_counts,
    get_user_shelf_counts
):

    favorite_books = []

    if current_user.is_authenticated:

        counts = get_user_shelf_counts(
            current_user.id
        )

        favorite_books = current_user.favorite_books

        recent_reviews = (
            Comment.query
            .filter_by(user_id=current_user.id)
            .order_by(Comment.created_at.desc())
            .limit(2)
            .all()
        )


        return {
            "counts": counts,
            "profile_name": current_user.name,
            "profile_username": current_user.username,
            "profile_bio": current_user.bio,
            "profile_email": current_user.email,
            "profile_avatar": current_user.avatar,
            "favorite_books": favorite_books,
            "recent_reviews": recent_reviews,
        }

    session_id = get_session_id()

    counts = get_shelf_counts(session_id)

    profile_name = session.get(
        "profile_name",
        "Name"
    )

    profile_username = session.get(
        "profile_username",
        "username"
    )

    profile_avatar = session.get(
        "profile_avatar"
    )

    profile_email = session.get(
        "profile_email",
        ""
    )

    profile_bio = session.get(
        "profile_bio",
        "An avid reader with interests in a range of genres."
    )

    favorite_book_ids = session.get(
        "favorite_books",
        ""
    )

    if favorite_book_ids:

        ids = [
            int(book_id)
            for book_id in favorite_book_ids.split(",")
            if book_id
        ]
        
        books = Book.query.filter(
            Book.id.in_(ids)
        ).all()

        favorite_books = sorted(
            books,
            key=lambda book: ids.index(book.id)
        )
    
    recent_reviews = (
        Comment.query
        .filter_by(session_id=session_id)
        .order_by(Comment.created_at.desc())
        .limit(2)
        .all()
    )

    return {
        "counts": counts,
        "profile_name": profile_name,
        "profile_username": profile_username,
        "profile_bio": profile_bio,
        "profile_email": profile_email,
        "profile_avatar": profile_avatar,
        "favorite_books": favorite_books,
        "recent_reviews": recent_reviews
    }

def update_favorite_books(
    user,
    favorite_book_ids
):

    user.favorite_books.clear()

    if favorite_book_ids:

        ids = [
            int(book_id)
            for book_id in favorite_book_ids.split(",")
            if book_id
        ]

        books = Book.query.filter(
            Book.id.in_(ids)
        ).all()

        sorted_books = sorted(
            books,
            key=lambda book: ids.index(book.id)
        )

        user.favorite_books.extend(
            sorted_books
        )


def update_authenticated_profile(
    request,
    avatar_file
):

    current_user.name = request.form.get("name")

    current_user.username = request.form.get(
        "username"
    )

    current_user.bio = request.form.get("bio")

    current_user.email = request.form.get("email")

    if request.form.get("remove_avatar") == "1":
        current_user["profile_avatar"] = None

    if avatar_file and avatar_file.filename:

        current_user.avatar = save_avatar(
            avatar_file
        )

    favorite_book_ids = request.form.get(
        "favorite_books",
        ""
    )

    update_favorite_books(
        current_user,
        favorite_book_ids
    )
    
    db.session.commit()


def update_anonymous_profile(
    request,
    avatar_file
):

    session["profile_name"] = request.form.get(
        "name"
    )

    session["profile_username"] = request.form.get(
        "username"
    )

    session["profile_bio"] = request.form.get(
        "bio"
    )

    session["profile_email"] = request.form.get(
        "email"
    )

    session["favorite_books"] = request.form.get(
        "favorite_books",
        ""
    )

    if request.form.get("remove_avatar") == "1":
        session["profile_avatar"] = None

    if avatar_file and avatar_file.filename:

        session["profile_avatar"] = save_avatar(
            avatar_file
        )