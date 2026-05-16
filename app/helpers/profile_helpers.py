import os

from flask import session
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Book, Comment

# Save profile pic
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

# Profile data to display
def get_profile_data(get_user_shelf_counts):

    favorite_books = current_user.favorite_books

    counts = get_user_shelf_counts(current_user.id)

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

# Favourite books
def update_favorite_books(user, favorite_book_ids):

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

# Update profile
def update_profile(request, avatar_file):

    current_user.name = request.form.get("name", "").strip()
    current_user.username = request.form.get("username", "").strip().lower()
    current_user.bio = request.form.get("bio")
    current_user.email = request.form.get("email", "").strip().lower()

    if request.form.get("remove_avatar") == "1":
        current_user.avatar = None

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

# Get other user profiles
def get_public_profile_data(user, get_user_shelf_counts):

    counts = get_user_shelf_counts(user.id)

    favorite_books = user.favorite_books

    recent_reviews = (
        Comment.query
        .filter_by(user_id=user.id)
        .order_by(Comment.created_at.desc())
        .limit(2)
        .all()
    )

    is_own_profile = (
        current_user.is_authenticated
        and current_user.id == user.id
    )

    return {
        "counts": counts,
        "profile_name": user.name,
        "profile_username": user.username,
        "profile_bio": user.bio,
        "profile_email": user.email,
        "profile_avatar": user.avatar,
        "favorite_books": favorite_books,
        "recent_reviews": recent_reviews,
        "profile_user": user,
        "is_own_profile": is_own_profile
    }