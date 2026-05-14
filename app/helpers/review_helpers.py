from app.extensions import db
from app.models import Comment, Rating

# Create or update reviews
def create_or_update_review(book_id, stars, text, user=None, session_id=None, username="Anonymous"):
    """
    Create or update rating and review for one book.
    A logged-in user or anonymous session can only have one review per book.
    """

    if user:
        existing_rating = Rating.query.filter_by(
            user_id=user.id,
            book_id=book_id
        ).first()

        if existing_rating:
            existing_rating.stars = stars
            existing_rating.username = user.username
        else:
            rating = Rating(
                user_id=user.id,
                book_id=book_id,
                stars=stars,
                username=user.username
            )
            db.session.add(rating)

        existing_comment = Comment.query.filter_by(
            user_id=user.id,
            book_id=book_id
        ).first()

        if existing_comment:
            existing_comment.text = text
            existing_comment.stars = stars
            existing_comment.username = user.username
        else:
            comment = Comment(
                user_id=user.id,
                username=user.username,
                book_id=book_id,
                text=text,
                stars=stars
            )
            db.session.add(comment)

    else:
        existing_rating = Rating.query.filter_by(
            session_id=session_id,
            book_id=book_id
        ).first()

        if existing_rating:
            existing_rating.stars = stars
            existing_rating.username = username
        else:
            rating = Rating(
                session_id=session_id,
                book_id=book_id,
                stars=stars,
                username=username
            )
            db.session.add(rating)

        existing_comment = Comment.query.filter_by(
            session_id=session_id,
            book_id=book_id
        ).first()

        if existing_comment:
            existing_comment.text = text
            existing_comment.stars = stars
            existing_comment.username = username
        else:
            comment = Comment(
                session_id=session_id,
                username=username,
                book_id=book_id,
                text=text,
                stars=stars
            )
            db.session.add(comment)

    return existing_comment if "existing_comment" in locals() and existing_comment else comment