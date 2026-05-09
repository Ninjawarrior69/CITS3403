import os

from flask import session
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.models import Book


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

        return {
            "counts": counts,
            "profile_name": current_user.name,
            "profile_username": current_user.username,
            "profile_bio": current_user.bio,
            "profile_avatar": current_user.avatar,
            "favorite_books": favorite_books
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

        favorite_books = Book.query.filter(
            Book.id.in_(ids)
        ).all()

    return {
        "counts": counts,
        "profile_name": profile_name,
        "profile_username": profile_username,
        "profile_bio": profile_bio,
        "profile_avatar": profile_avatar,
        "favorite_books": favorite_books
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

        user.favorite_books.extend(
            books
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

    if avatar_file and avatar_file.filename:

        session["profile_avatar"] = save_avatar(
            avatar_file
        )